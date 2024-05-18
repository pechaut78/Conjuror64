from ..Atom import Atom
class CSVMerge(Atom):
    def process(self):
        directory = self.params.get("directory")
        output_file = self.params.get("output")

        if not directory or not output_file:
            self.fail("Directory and output file must be specified")
            return

        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

        if not csv_files:
            self.fail("No CSV files found in the directory.")
            return

        try:
            with open(output_file, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                header_written = False

                for file in csv_files:
                    with open(os.path.join(directory, file), 'r') as infile:
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