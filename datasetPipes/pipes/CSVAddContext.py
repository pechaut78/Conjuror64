import pandas as pd
import csv
from ..Atom import Atom

class CSVAddContext(Atom):
    def process(self):
        input_csv = self.params.get('input')
        if(input_csv == None):
            input_csv = self.input
        string_to_append = self.params.get('context')
        output_csv = self.params.get('output')
        self.input = input_csv
        
        if not input_csv or not string_to_append or not output_csv:
            self.fail("input, context, and output must be specified")
            return
        
        try:
            rows = []
            with open(input_csv, 'r', newline='') as infile:
                reader = csv.DictReader(infile)
                fieldnames = reader.fieldnames
                for row in reader:
                    if 'question' in row:
                        row['question'] = string_to_append + row['question']
                    rows.append(row)

            # Écrire le contenu modifié dans le fichier de sortie
            with open(output_csv, 'w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)

            self.success(f"File {output_csv} created successfully, with the string '{string_to_append}' appended to each 'question'.")
        except Exception as e:
            self.fail(f"An unexpected error occurred - {str(e)}")