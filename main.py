from fileLoaders.dataLoader import data_loader
from pathlib import Path

if __name__ =="__main__":
    abs_path = Path(__file__).parent   # مسیر پروژه 
    codon_data_path = Path(__file__).resolve().parent/"data"/"codon_table.txt"
    amino_data_path = Path(__file__).resolve().parent/"data"/"amino_weights.txt"      
    data_loader(codon_data_path,amino_data_path)
    
