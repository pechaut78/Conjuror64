import pandas as pd
import argparse

def format_csv(input_csv, output_csv):
    # Charger le fichier CSV
    df = pd.read_csv(input_csv)
    
    # Vérifier si les colonnes nécessaires sont présentes
    if 'question' not in df.columns or 'answer' not in df.columns:
        raise ValueError("Le fichier CSV doit contenir les colonnes 'question' et 'answer'")
    
    # Créer une nouvelle colonne 'text' avec le format spécifié
    df['text'] = df.apply(lambda row: f"[INST]{row['question']}[/INST]{row['answer']}", axis=1)
    
    # Sauvegarder le nouveau fichier CSV avec seulement la colonne 'text'
    df[['text']].to_csv(output_csv, index=False)

def main():
    parser = argparse.ArgumentParser(description="Format CSV with decorated text column")
    parser.add_argument('input_csv', type=str, help="Path to the input CSV file")
    parser.add_argument('output_csv', type=str, help="Path to the output CSV file")

    args = parser.parse_args()

    format_csv(args.input_csv, args.output_csv)

if __name__ == "__main__":
    main()
