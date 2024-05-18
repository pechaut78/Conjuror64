import pandas as pd
import argparse
import csv

def clean_cell(cell):
    # Nettoyer les guillemets supplémentaires et les espaces indésirables
    if pd.notna(cell):  # Vérifier que la cellule n'est pas NaN
        cell = cell.strip()
       
    return cell

def clean_csv(input_csv, output_csv):
    try:
        # Lire le fichier CSV dans un DataFrame
        df = pd.read_csv(input_csv, dtype=str, header=None)

        # Appliquer la fonction de nettoyage à chaque cellule du DataFrame
        df = df.applymap(clean_cell)

        # Écrire le DataFrame nettoyé dans un nouveau fichier CSV
        df.to_csv(output_csv, index=False, header=False, quoting=csv.QUOTE_MINIMAL)

        print("OK")
    except Exception as e:
        print(f"NOK: An unexpected error occurred - {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Clean a CSV file and ensure all entries are in the correct format.")
    parser.add_argument("input_csv", type=str, help="The input CSV file")
    parser.add_argument("output_csv", type=str, help="The output CSV file")
    args = parser.parse_args()

    clean_csv(args.input_csv, args.output_csv)

if __name__ == "__main__":
    main()
