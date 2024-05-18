import csv
import argparse

def main():
    parser = argparse.ArgumentParser(description="Append a string to the 'question' column in a CSV file.")
    parser.add_argument("input_csv", type=str, help="The input CSV file")
    parser.add_argument("string_to_append", type=str, help="The string to append to each 'question'")
    parser.add_argument("output_csv", type=str, help="The output CSV file")
    args = parser.parse_args()

    input_csv = args.input_csv
    string_to_append = args.string_to_append
    output_csv = args.output_csv

    with open(input_csv, 'r', newline='') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()

        for row in reader:
            if 'question' in row:
                row['question'] = string_to_append+row['question']
            writer.writerow(row)

    print(f"Fichier {output_csv} créé avec succès, avec la chaîne '{string_to_append}' ajoutée à chaque 'question'.")

if __name__ == "__main__":
    main()
