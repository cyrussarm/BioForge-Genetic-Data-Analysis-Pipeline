from pathlib import Path

from fileLoaders.dataLoader import data_loader
from fileLoaders.inputLoader import input_loader
from models.sequence import Sequence
from models.ORF import ORF
from utils.ORF_detector import ORF_detection
from logger import setup_logging
from fileLoaders.dataLoader import data_loader


if __name__ =="__main__":
    abs_path = Path(__file__).parent   # مسیر پروژه 
    codon_data_path = Path(__file__).resolve().parent/"data"/"codon_table.txt"
    amino_data_path = Path(__file__).resolve().parent/"data"/"amino_weights.txt"      
    log = setup_logging(abs_path / "output")
    log.info("BioForge started")
    res = data_loader(codon_data_path,amino_data_path)
    CODONS = res[0]
    WEIGHTS = res[1]

    input_FASTA_path = Path(__file__).resolve().parent/"input"/"sample.fasta"
    FASTA = input_loader(input_FASTA_path)
    print(FASTA)

# این قسمت باید برای همه رکوردهای فایل ورودی تکرار شود
#  مثال برای ساختن یک sequence
    s1 = Sequence(FASTA[0]["id"], FASTA[0]["description"], FASTA[0]["sequence"])
    complement = s1.reverse_complement()
   
# استخراج لیست ORF های این sequence
    ORF_detection(s1.sequence,complement)
 


   
     
    
