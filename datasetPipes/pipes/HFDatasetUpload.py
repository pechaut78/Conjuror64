import pandas as pd
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi, HfFolder
from ..Atom import Atom

class HFDatasetUpload(Atom):
    def process(self):
        input_csv = self.params.get('input')
        if(input_csv == None):
            input_csv = self.input
        hf_path = self.params.get('hf_path')
        token_file = self.params.get('token_file')
        self.input = input_csv

        if not input_csv or not hf_path or not token_file:
            self.fail("input_csv, hf_path, and token_file must be specified")
            return
        
        try:
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
            api.create_repo(repo_id=hf_path, exist_ok=True, repo_type='dataset')

            # Upload du dataset sur Hugging Face
            dataset_dict.push_to_hub(hf_path, token=token)

            self.success(f"Dataset uploaded to Hugging Face at {hf_path} successfully!")
        except Exception as e:
            self.fail(f"An unexpected error occurred - {str(e)}")
