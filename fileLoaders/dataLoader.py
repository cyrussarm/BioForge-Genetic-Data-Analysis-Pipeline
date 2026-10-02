import os
import re
from logger import get_logger
log = get_logger()

def data_loader(codonfile, aminofile):     
    codon_table = {} 
    amino_weights = {}
    
    if not os.path.exists(codonfile):
        log.error("Codon table file not found: %s", codonfile)
        raise FileNotFoundError("codon table file")

    if not os.path.exists(aminofile):
        log.error("Amino weights file not found: %s", aminofile)
        raise FileNotFoundError("amino weights file")

    with open(codonfile,"r", encoding="utf-8") as f:
        for i,line in enumerate(f):
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
                log.error("codon_table.txt line %d: bad format: %r", i + 1, line)
            else:
                codon = m.group(1)
                amino = m.group(2)
                if codon in codon_table:
                    log.warning("codon_table.txt line %d: duplicate codon %s", i + 1, codon)
                codon_table[codon]=amino

    with open(aminofile,"r", encoding="utf-8") as f:
        for i,line in enumerate(f):
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
                log.error("amino_weights.txt line %d: bad format: %r", i + 1, line)
            else:
                amino = m.group(1)
                weight = m.group(2)
                if amino in amino_weights:
                    log.warning("amino_weights.txt line %d: duplicate amino %s", i + 1, amino)
                amino_weights[amino]=weight

    return codon_table, amino_weights
