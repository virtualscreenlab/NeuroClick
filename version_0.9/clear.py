import os


def delete_extra_files():
    files = ['good_azides.txt', 'good_alkynes.txt', 'output.txt', 'output.csv', 'azides_log.txt', 'alkynes_log.txt',
             'parameters_log.txt', 'products_log.txt']
    for i in range(len(files)):
        try:
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), files[i])
            os.remove(path)
        except FileNotFoundError:
            pass
