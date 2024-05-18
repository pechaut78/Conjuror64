import pandas as pd
import argparse
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi, HfFolder

def upload_csv_to_hf(input_csv, hf_path, token_file):
    # Lire le token depuis le fichier .token
    with open(token_file, 'r') as file:
        token = file.read().strip()

    # Charger le fichier CSV
    df = pd.read_csv(input_csv)

    # Convertir le DataFrame pandas en Dataset Hugging Face
    dataset = Dataset.from_pandas(df)

    # Créer un DatasetDict avec une seule partition
    dataset_dict = DatasetDict({'train': dataset})

    # Authentification avec le token d'accès
    HfFolder.save_token(token)
    api = HfApi()
    api.create_repo(repo_id=hf_path, exist_ok=True)

    # Upload du dataset sur Hugging Face
    dataset_dict.push_to_hub(hf_path, token=token)

def main():
    parser = argparse.ArgumentParser(description="Upload CSV to Hugging Face dataset")
    parser.add_argument('input_csv', type=str, help="Path to the input CSV file")
    parser.add_argument('hf_path', type=str, help="Hugging Face dataset path (e.g., username/dataset_name)")
    parser.add_argument('--token_file', type=str, required=True, help="Path to the file containing the Hugging Face API token")

    args = parser.parse_args()

    upload_csv_to_hf(args.input_csv, args.hf_path, args.token_file)

if __name__ == "__main__":
    main()
