import pandas as pd
import argparse
#import prettyprinter
from pprint import pprint

def main():
    parser = argparse.ArgumentParser(description="Load a CSV file into a DataFrame and check for loading issues.")
    parser.add_argument("input_csv", type=str, help="The input CSV file")
    args = parser.parse_args()

    input_csv = args.input_csv

    try:
        # Tentative de chargement du fichier CSV dans un DataFrame
        df = pd.read_csv(input_csv)
        print("OK")
        pprint(df.head(30))
    except pd.errors.ParserError as e:
        # Si une erreur de parsing se produit, extraire et afficher les informations sur la ligne problématique
        error_line = str(e).split('\n')[0]  # Extraire la première ligne du message d'erreur
        print(f"NOK: {error_line}")
    except Exception as e:
        # Gérer d'autres exceptions éventuelles
        print(f"NOK: An unexpected error occurred - {str(e)}")

if __name__ == "__main__":
    main()
