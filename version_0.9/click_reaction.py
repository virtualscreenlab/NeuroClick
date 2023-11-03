from time_functions import time_format

import csv
import pandas as pd
import time
from PyQt5 import QtGui
from rdkit import Chem
from rdkit.Chem import Lipinski as Lipinksy
from rdkit.Chem import rdChemReactions, rdMolDescriptors

RXN_1_4 = rdChemReactions.ReactionFromSmarts(
    '[#6:6][N:1]=[N:2]=[N:3].[#6:7][C:4]#[C:5]>>[#6:6][N:1]([N:2]=[N:3]1)[C:5]=[C:4]1[#6:7]')
RXN_1_5 = rdChemReactions.ReactionFromSmarts(
    '[#6:6][N:1]=[N:2]=[N:3].[#6:7][C:4]#[C:5]>>[#6:6][N:1]1[N:2]=[N:3][C:4]=[C:5]1[#6:7]')
RXN_BOTH = rdChemReactions.ReactionFromSmarts(
    '[#6:6][N:1]=[N:2]=[N:3].[C:4]#[C:5]>>[#6:6][N:1]1[N:2]=[N:3][C:4]=[C:5]1')
INNER_BOND_PATTERN = Chem.MolFromSmarts('[#6][C]#[C][#6]')


def check_Clark(molecule, threshold, dict_row):
    logP = Lipinksy.rdMolDescriptors.CalcCrippenDescriptors(molecule)[0]
    tpsa = rdMolDescriptors.CalcTPSA(molecule)
    logBB = round(0.152 * logP - 0.0148 * tpsa + 0.139, 2)
    dict_row['logBB_Clark'] = logBB
    return logBB >= threshold


def check_Rishton(molecule, threshold, dict_row):
    logP = Lipinksy.rdMolDescriptors.CalcCrippenDescriptors(molecule)[0]
    tpsa = rdMolDescriptors.CalcTPSA(molecule)
    logBB = round(0.155 * logP - 0.01 * tpsa + 0.164, 2)
    dict_row['logBB_Rishton'] = logBB
    return logBB >= threshold


def check_Lipinsky(molecule, Lipinsky_selected, dict_row):
    donors = Lipinksy.NumHDonors(molecule)
    if Lipinsky_selected['donors']:
        dict_row['donors'] = donors
    acceptors = Lipinksy.NumHAcceptors(molecule)
    if Lipinsky_selected['acceptors']:
        dict_row['acceptors'] = acceptors
    weight = round(Lipinksy.rdMolDescriptors.CalcExactMolWt(molecule), 3)
    if Lipinsky_selected['weight']:
        dict_row['weight'] = weight
    logP = round(Lipinksy.rdMolDescriptors.CalcCrippenDescriptors(molecule)[0], 3)
    if Lipinsky_selected['logP']:
        dict_row['logP'] = logP

    return bool(((donors <= 5) or not Lipinsky_selected['donors']) and (
            (acceptors <= 10) or not Lipinsky_selected['acceptors']) \
                and ((weight < 500) or not Lipinsky_selected['weight']) \
                and ((logP <= 5) or not Lipinsky_selected[
        'logP']))


def get_reaction_products(azides, alkynes, isomers, inner_alkyne_specification, Lipinsky_selected, logBB_model,
                          threshold, calc_window):
    start_time = time.time()
    calc_window.show_log('Starting library generation...\n')

    if isomers not in ['1_4', '1_5', 'both']:
        raise Exception(f'Invalid isomers configuration: {isomers}')
    if inner_alkyne_specification not in ['ignore', 'both']:
        raise Exception(f'Invalid internal alkynes handling specification: {inner_alkyne_specification}')
    if logBB_model != 'Clark' and logBB_model != 'Rishton':
        raise Exception(f'Invalid logBB calculation model: {logBB_model}')

    good_products = {}
    total_products = []
    inner_alkynes = 0
    Lipinsky_fail = 0
    logBB_fail = 0
    all_candidates = 0
    errors = 0
    isomers_1_4 = 0
    isomers_1_5 = 0

    for azide in azides:
        for alkyne in alkynes:
            all_candidates += 1
            calc_window.progress_bar.setValue(round((all_candidates) / (len(azides) * len(alkynes)) * 100))
            reactants = (Chem.MolFromSmiles(azide), Chem.MolFromSmiles(alkyne))
            try:
                if reactants[1].HasSubstructMatch(INNER_BOND_PATTERN) and inner_alkyne_specification == 'ignore':
                    continue
                elif reactants[1].HasSubstructMatch(INNER_BOND_PATTERN) and inner_alkyne_specification == 'both':
                    prom_products = RXN_BOTH.RunReactants(reactants)
                    inner_alkynes += 1
                elif isomers == '1_4':
                    prom_products = RXN_1_4.RunReactants(reactants)
                    isomers_1_4 += 1
                elif isomers == '1_5':
                    prom_products = RXN_1_5.RunReactants(reactants)
                    isomers_1_5 += 1
                else:
                    prom_products = RXN_BOTH.RunReactants(reactants)
                    isomers_1_4 += 1
                    isomers_1_5 += 1
            except Exception:
                calc_window.show_log(f'Warning: troubles generating molecule from {azide} and {alkyne}')
                errors += 1
                continue

            prom_products = [Chem.MolToSmiles(mol[0]) for mol in prom_products]
            prom_products = [product.replace('[N+]', 'N').replace('[N-]', 'N') for product in prom_products]

            for product in prom_products:
                dict_row = {'donors': '-', 'acceptors': '-', 'weight': '-', 'logP': '-', 'logBB_Clark': '-',
                            'logBB_Rishton': '-'}
                try:
                    if check_Lipinsky(Chem.MolFromSmiles(product), Lipinsky_selected, dict_row):
                        if logBB_model == 'Clark':
                            logBB_Clark = check_Clark(Chem.MolFromSmiles(product), threshold, dict_row)
                            if logBB_Clark:
                                good_products[product] = dict_row
                            else:
                                logBB_fail += 1
                        else:
                            logBB_Rishton = check_Rishton(Chem.MolFromSmiles(product), threshold, dict_row)
                            if logBB_Rishton:
                                good_products[product] = dict_row
                            else:
                                logBB_fail += 1
                    else:
                        Lipinsky_fail += 1
                    total_products.append(product)
                except Exception:
                    calc_window.show_log(f'Warning: troubles generating molecule from {azide} and {alkyne}')
                    errors += 1
                    continue
        calc_window.log.moveCursor(QtGui.QTextCursor.End)

    end_time = time.time()
    hours, minutes, seconds = time_format(start_time, end_time)

    calc_window.show_log('\n\n')
    calc_window.show_log('====\n')
    calc_window.show_log('Finished library generation!\n')
    calc_window.show_log(f'Time: {hours:02}:{minutes:02}:{seconds:02}\n')

    calc_window.show_log(
        f'{len(total_products)} compounds were generated from {len(alkynes)} alkynes and '
        f'{len(azides)} azides '
        f'({round(len(total_products) / (len(total_products) + errors + 0.00001) * 100, 2)}% of maximum possible)\n')
    calc_window.show_log(f'{isomers_1_4} 1,4-isomers and {isomers_1_5} 1,5-isomers\n')
    if inner_alkynes != 0:
        calc_window.show_log(
            f'Warning: {inner_alkynes * 2} molecules of {len(total_products)} were generated from internal alkynes and '
            f'could not be assigned 1,4/1,5 isomery\n')
    calc_window.show_log(f'Failed to construct {errors} molecules\n')
    calc_window.show_log(
        f'{len(good_products) + logBB_fail} molecules passed Lipinsky filter '
        f'({round((len(good_products) + logBB_fail) / len(total_products) * 100, 2)}% of generated,'
        f' {round((len(good_products) + logBB_fail) / (len(total_products) + errors + 0.00001) * 100, 2)}% '
        f'of maximum possible)\n')
    calc_window.show_log(
        f'{len(good_products)} molecules passed logBB  filter '
        f'({round(len(good_products) / len(total_products) * 100, 2)}% of generated, '
        f'{round(len(good_products) / (len(good_products) + logBB_fail) * 100, 2)}% of Lipinsky filtered, '
        f'{round(len(good_products) / (len(total_products) + errors + 0.00001) * 100, 2)}% of maximum possible)')
    calc_window.activate_next()
    return good_products


def clear_csv_file(Lipinsky_selected, logBB_model):
    f = pd.read_csv('output.csv')
    if not Lipinsky_selected['donors']:
        del f['H-donors']
    if not Lipinsky_selected['acceptors']:
        del f['H-acceptors']
    if not Lipinsky_selected['weight']:
        del f['molecular_weight']
    if not Lipinsky_selected['logP']:
        del f['logP']
    if logBB_model != 'Clark':
        del f['logBB_Clark']
    if logBB_model != 'Rishton':
        del f['logBB_Rishton']
    f.to_csv('output.csv', index=False)


def reaction(isomers, inner_alkyne_specification, Lipinsky_selected, logBB_model, threshold, saving_format,
             calc_window):
    azides = ''.join(open('good_azides.txt')).split()
    if not azides:
        calc_window.show_log('Invalid azides configuration was entered. Unable to continue')
        return

    alkynes = ''.join(open('good_alkynes.txt')).split()
    if not alkynes:
        calc_window.show_log('Invalid alkynes configuration was entered. Unable to continue')
        return

    reaction_products = get_reaction_products(azides, alkynes, isomers, inner_alkyne_specification, Lipinsky_selected,
                                              logBB_model, threshold, calc_window)

    if saving_format == 'csv':
        with open('output.csv', 'w', newline='') as csvfile:
            fieldnames = ['molecule', 'H-donors', 'H-acceptors', 'molecular_weight', 'logP', 'logBB_Clark',
                          'logBB_Rishton']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for key, value in reaction_products.items():
                writer.writerow({'molecule': key, 'H-donors': value['donors'], 'H-acceptors': value['acceptors'],
                                 'molecular_weight': value['weight'], 'logP': value['logP'],
                                 'logBB_Clark': value['logBB_Clark'], 'logBB_Rishton': value['logBB_Rishton']})
            csvfile.close()

        clear_csv_file(Lipinsky_selected, logBB_model)
    else:
        with open('output.txt', 'w') as f:
            for mol in reaction_products.keys():
                f.write(f'{mol}\n')
