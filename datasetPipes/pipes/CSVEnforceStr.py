import pandas as pd
import csv
from ..Atom import Atom


def clean_cell(cell):
    # Nettoyer les guillemets supplémentaires et les espaces indésirables
    if pd.notna(cell):  # Vérifier que la cellule n'est pas NaN
        cell = cell.strip()
    return cell

class CSVEnforceStr(Atom):
    def process(self):
        input_csv = self.params.get('input')
        if(input_csv == None):
            input_csv = self.input
        self.output = input_csv
        output_csv = self.params.get('output')
        
        if not input_csv or not output_csv:
            self.fail("output must be specified")
            return
        
        try:
            # Lire le fichier CSV dans un DataFrame
            df = pd.read_csv(input_csv, dtype=str, header=None)

            # Appliquer la fonction de nettoyage à chaque cellule du DataFrame
            df = df.applymap(clean_cell)

            # Écrire le DataFrame nettoyé dans un nouveau fichier CSV
            df.to_csv(output_csv, index=False, header=False, quoting=csv.QUOTE_MINIMAL)

            self.success(f"File {output_csv} cleaned successfully!")
        except Exception as e:
            self.fail(f"An unexpected error occurred - {str(e)}")