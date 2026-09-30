import os
import re

def data_loader(codonfile, aminofile):
    """ loading codon_table and amino_weights """   
    codon_table = {} 
    amino_weights = {}
    
    if not os.path.exists(codonfile):
        raise FileNotFoundError("codon table file")

    if not os.path.exists(aminofile):
        raise FileNotFoundError("amino weights file")

    with open(codonfile,"r", encoding="utf-8") as f:
        for i,line in enumerate(f,start=1):
            line = line.strip()            
            # رد کردن خط خالی
            if not line:
                continue   
            # رد کردن کامنت های اول فایل
            if line.startswith("#"):
                continue
            # چک پترن خط
            m = re.match(r"^([ACGTU]{3})\s+(\S+)$",line) # یعنی خط با سه تا از کاراکترهای داخل کروشه شروع بشه + فاصله + یک استرینگ دیگر
            if not m:
                print(f" WARNING: codon format mot found in line {i}")
            else:
                codon = m.group(1)
                amino = m.group(2)
                if codon in codon_table:
                    print(f"WARNING: duplicated codon if file found : {codon}")
                codon_table[codon]=amino

    with open(aminofile,"r", encoding="utf-8") as f:
        for i,line in enumerate(f,start=1):
            line = line.strip()            
            # رد کردن خط خالی
            if not line:
                continue   
            # رد کردن کامنت های اول فایل
            if line.startswith("#"):
                continue
            # چک پترن خط
            m = re.match(r"^([A-Z])\s+(\d+\.\d+)$",line) 
            if not m:
                print(f" WARNING: amino format not found in line {i}")
            else:
                amino = m.group(1)
                weight = m.group(2)
                if amino in amino_weights:
                    print(f"WARNING: duplicated amino if amino_weights file found : {amino}")
                amino_weights[amino]=weight
                
              
        print(amino_weights)






    
    

