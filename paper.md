---
title: 'NeuroClick: Software for Mimicking the Click Reaction to Generate Drug-like Molecules Permeating the Blood-Brain Barrier'
tags:
  - Python
  - cheminformatics
  - drug discovery
  - click chemistry
  - blood-brain barrier
authors:
  - name: Anastasiia M. Isakova
    orcid: 0000-0000-0000-0000
    affiliation: "1"
  - name: Ekaterina V. Skorb
    orcid: 0000-0000-0000-0000
    affiliation: "1"
  - name: Sergey Shityakov
    corresponding: true
    affiliation: "1"
affiliations:
 - name: Laboratory of Cheminformatics, Infochemistry Scientific Center, ITMO University, Saint Petersburg, Russian Federation
   index: 1
date: 2024
bibliography: paper.bib

---

# Summary

NeuroClick is a software tool designed for the in silico execution of azide‒alkyne cycloaddition reactions, commonly known as click reactions. Developed by the Laboratory of Cheminformatics at ITMO University, this graphical user interface (GUI) application aims to expedite the drug discovery process by generating libraries of 1,2,3-triazole compounds. NeuroClick enables users to input reagent SMILES strings, rapidly generating and screening extensive combinatorial libraries at a pace of 10,000 molecules per minute.

The software applies stringent criteria to ensure the relevance and accuracy of the generated compounds, excluding molecules without azide groups or those with multiple reactive functional groups to maintain dataset integrity. NeuroClick incorporates advanced filtering options based on Lipinski's rule of five and blood‒brain barrier (BBB) permeability predictors, allowing researchers to identify drug-like molecules with potential central nervous system (CNS) activity. The software's high-throughput and user-friendly interface significantly enhances the efficiency of early-stage drug development by facilitating the exploration of vast chemical spaces and identifying promising lead compounds for further development.

# Statement of need

NeuroClick was created to provide researchers with an efficient tool for conducting virtual screening through in silico click chemistry. Traditional methods of manually preprocessing reagents and performing combinatorial chemistry are time-consuming and resource-intensive. NeuroClick addresses these challenges by automating the process, allowing for the rapid generation and screening of potential drug candidates. The software's integration of Lipinski's rule of five and BBB permeability predictions ensures that the generated compounds are both drug-like and capable of permeating the blood-brain barrier, which is crucial for the development of CNS-active drugs.

# Features

- **Rapid Library Generation**: Generate combinatorial libraries at a rate of 10,000 molecules per minute.
- **Advanced Filtering**: Apply Lipinski's rule of five and BBB permeability predictions to identify viable drug candidates.
- **User-Friendly Interface**: The intuitive GUI allows for easy input and processing of SMILES strings.
- **Detailed Logs and Visualization**: Track the progress of your screening process and visualize the generated compounds.

# Mathematics

The calculation of logBB can be performed via the Clark or Rishton model:

$$
\text{logBB}_{\text{Clark}} =  0.152 \cdot \text{ClogP} – 0.0148 \cdot \text{TPSA} + 0.139
$$

$$
\text{logBB}_{\text{Rishton}}= 0.155 \cdot \text{ClogP} – 0.01 \cdot \text{TPSA} + 0.164
$$

# Figures

![The versatile regioselectivity of the azide‒alkyne cycloaddition aka click reaction.\label{fig:reaction}](figure.png)

# References

References to be included from the `paper.bib` file.
