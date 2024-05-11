import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Process a file to split into documents.")
    parser.add_argument("filename", type=str, help="The name of the file to process")
    args = parser.parse_args()

    filename = args.filename
    base_name = os.path.splitext(filename)[0]  # Retire l'extension du fichier
    if not os.path.exists(base_name):
        os.makedirs(base_name)  # Crée un répertoire du même nom que le fichier sans l'extension

    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    print("Splitting Doc...")
    separator = "\n\n\n\n"
    _docs = text.split(separator)
    docs = [doc for doc in _docs if doc.strip() and len(doc.strip()) >= 3]

    for index, doc in enumerate(docs):
        doc_filename = os.path.join(base_name, f"{index}.txt")
        with open(doc_filename, 'w', encoding='utf-8') as doc_file:
            doc_file.write(doc)
        print(f"Document {index} saved as '{doc_filename}'.")

if __name__ == "__main__":
    main()