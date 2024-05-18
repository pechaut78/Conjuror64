import subprocess
import json
import argparse

def run_script(script_name, params):
    try:
        # Construire la commande avec les paramètres
        cmd = ['python', script_name] + params
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Afficher la sortie du script
        print(result.stdout)
        print(result.stderr)
        
        # Vérifier le code de retour
        if result.returncode != 0:
            print(f"Erreur lors de l'exécution de {script_name}")
            return False
        return True
    except Exception as e:
        print(f"Exception lors de l'exécution de {script_name}: {e}")
        return False

def main():
    # Configurer argparse pour lire les arguments de la ligne de commande
    parser = argparse.ArgumentParser(description="Exécuter une série de scripts définis dans un fichier JSON")
    parser.add_argument("config_file", type=str, help="Nom du fichier JSON de configuration")
    
    args = parser.parse_args()
    
    # Lire la configuration à partir du fichier JSON
    with open(args.config_file) as config_file:
        config = json.load(config_file)
    
    # Exécuter les scripts selon la configuration
    for script in config["scripts"]:
        if not run_script(script["name"], script["params"]):
            print(f"Arrêt du pipeline à cause de l'échec de {script['name']}")
            break

if __name__ == "__main__":
    main()