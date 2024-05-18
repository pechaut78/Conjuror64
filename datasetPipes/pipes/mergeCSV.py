import os
import csv
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Merge all .csv files in a given directory into one CSV file.")
    parser.add_argument("directory", type=str, help="The directory to process")
    parser.add_argument("output", type=str, help="outputname")
    args = parser.parse_args()

    # Chemin du répertoire contenant les fichiers CSV
    directory = args.directory

    # Nom du fichier CSV de sortie
    output_file =args.output

    # Liste des fichiers CSV du répertoire
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the directory.")
        return 1

    # Ouvrir le fichier de sortie en écriture
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Écrire l'en-tête du fichier de sortie
        header_written = False

        # Parcourir les fichiers CSV du répertoire
        for file in csv_files:
            with open(os.path.join(directory, file), 'r') as infile:
                reader = csv.reader(infile)
                
                # Lire l'en-tête
                header = next(reader)

                # Écrire l'en-tête si ce n'est pas déjà fait
                if not header_written:
                    writer.writerow(header)
                    header_written = True

                # Écrire les lignes du fichier CSV
                for row in reader:
                    writer.writerow(row)

    print(f"Fichier {output_file} créé avec succès !")
    return 0

if __name__ == "__main__":
     sys.exit(main())
