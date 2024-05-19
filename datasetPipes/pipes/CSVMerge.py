from ..Atom import Atom
import csv
import os

class CSVMerge(Atom):
    def process(self):
        print(self.input)
        directory = self.params.get("directory")
        if directory is None:
            directory = self.input
        output_file = self.params.get("output")

        self.input = directory
        self.output = output_file
        if not directory or not output_file:
            self.fail("Directory and output file must be specified")
            return

        csv_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))

        if not csv_files:
            self.fail("No CSV files found in the directory and subdirectories.")
            return

        try:
            with open(output_file, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                header_written = False

                for file in csv_files:
                    with open(file, 'r') as infile:
                        reader = csv.reader(infile)
                        header = next(reader)

                        if not header_written:
                            writer.writerow(header)
                            header_written = True

                        for row in reader:
                            writer.writerow(row)
            
            self.success(f"File {output_file} created successfully!")
        except Exception as e:
            self.fail(str(e))
