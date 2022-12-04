import csv


class CSVPrinter:
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self, tsv=True):
        with open(self.file_name) as f:
            if tsv:
                reader = csv.reader(f, delimiter="\t")
            else:
                reader = csv.reader(f)
            lines = [row for row in reader]
        return lines
