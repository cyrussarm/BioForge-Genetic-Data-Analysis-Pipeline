import os
import re

from fileLoaders.dataLoader import data_loader
from fileLoaders.inputLoader import input_loader
from models.sequence import Sequence
from models.ORF import ORF
from utils.ORF_detector import ORF_detection

if __name__ =="__main__":
    
     # مسیر پروژه 
    abs_path = os.getcwd()   

    # خواندن داده ها از مسیر data    
    res = data_loader(abs_path)
    CODONS = res[0]       # دیکشنری کدنها
    WEIGHTS = res[1]      # دیکشنری وزنها
    stop_codons = res[2]  # تاپل استاپ کدنها

    # خواندن فایل فستا    
    input_FASTA_file = os.path.join(abs_path, "input", "sample.fasta")
    FASTA = input_loader(input_FASTA_file)
    print(FASTA)

# این قسمت باید برای همه رکوردهای فایل ورودی تکرار شود
#  مثال برای ساختن یک sequence
    s1 = Sequence(FASTA[0]["id"], FASTA[0]["description"], FASTA[0]["sequence"])
    complement = s1.reverse_complement()
   
# استخراج لیست ORF های این sequence
    ORF_detection(s1.sequence, complement, stop_codons)
 


   
     
    
