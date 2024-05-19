import pandas as pd
from ..Atom import Atom
import csv
import os

class CSVllamaFormat(Atom):
    def process(self):
        input_csv = self.params.get('input')
        if(input_csv == None):
            input_csv = self.input
        self.output = self.params.get('output')
        
        if not input_csv or not self.output:
            self.fail("Both input_csv and output_csv must be specified")
            return
        
        try:
            # Charger le fichier CSV
            df = pd.read_csv(input_csv)
            
            # Vérifier si les colonnes nécessaires sont présentes
            if 'question' not in df.columns or 'answer' not in df.columns:
                self.fail("The CSV file must contain 'question' and 'answer' columns")
                return
            
            # Créer une nouvelle colonne 'text' avec le format spécifié
            df['text'] = df.apply(lambda row: f"[INST]{row['question']}[/INST]{row['answer']}", axis=1)
            
            # Sauvegarder le nouveau fichier CSV avec seulement la colonne 'text'
            df[['text']].to_csv(self.output, index=False)
            
            self.success(f"File {self.output} created successfully!")
        except Exception as e:
            self.fail(str(e))