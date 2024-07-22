import pandas as pd
from glob import glob
import os

def extract_sam(input_sam):
    output_txt = input_sam.replace('.sam', '.txt')

    with open(input_sam, "r") as f:
        with open(output_txt, "w") as of:
            for line in f:
                if line.startswith("@"):
                    continue
                else:
                    line = line.strip().split("\t")
                    if line[2] == "*":
                        continue
                    else:
                        of.write(line[2] + "\n")

class Sam2Tax:

    def __init__(self, file_path):
        self.file_path = file_path.replace("\\", "/").rstrip("/")
        self.process_sam_files()
        self.combined_df = self.process_txt_files()

    def process_sam_files(self):
        sam_files = glob(f"{self.file_path}/*.sam")
        for file in sam_files:
            extract_sam(file)

    def process_txt_files(self):
        files = glob(f"{self.file_path}/*.txt")
        dfs = []
        for file in files:
            file = file.replace("\\", "/")
            print(f"Processing file: {file}")
            df3 = pd.read_csv(file, header=None)
            df3.columns = ['taxonomy']
            df4 = df3['taxonomy'].value_counts().reset_index()
            df4.columns = ['taxonomy', file.split("/")[-1].replace(".txt", "")]
            df4.set_index('taxonomy', inplace=True)
            dfs.append(df4)
            os.remove(file)
        df_combined = pd.concat(dfs, axis=1, sort=True).fillna(0)
        df_combined['Total'] = df_combined.sum(axis=1).astype(int)
        df_combined['Taxonomy'] = df_combined.index
        df_combined['Taxonomy'] = df_combined['Taxonomy'].str.rstrip(';')
        df_tax = df_combined['Taxonomy'].str.split(';', expand=True)
        df_tax.columns = ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
        df_tax.fillna("Unknown", inplace=True)
        df_combined_2 = pd.concat([df_combined, df_tax], axis=1)

        return df_combined_2
