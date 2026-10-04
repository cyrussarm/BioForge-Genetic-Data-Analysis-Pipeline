import os
import re
from logger import get_logger
log = get_logger()

from logger import get_logger
from models.BioForgeExceptions import DataFileError

log = get_logger()

def data_loader(codonfile, aminofile):     
    codon_table = {} 
    amino_weights = {}
    
    if not os.path.exists(codonfile):
        log.error("Codon table file not found: %s", codonfile)
        raise DataFileError("codon table file not found")

    if not os.path.exists(aminofile):
        log.error("Amino weights file not found: %s", aminofile)
        raise DataFileError("amino weights file not found")

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
            m = re.match(r"^([ACGU]{3})\s+(\S+)$",line) # یعنی خط با سه تا از کاراکترهای داخل کروشه شروع بشه + فاصله + یک استرینگ دیگر
            if not m:
                log.error("codon_table.txt line %d: bad format: %r", i + 1, line)
                raise DataFileError(f"codon_table.txt line {i+1}: bad format {line}")
            else:
                codon = m.group(1)
                amino = m.group(2)
                if codon in codon_table:
                    log.warning("codon_table.txt line %d: duplicate codon(ignored) %s", i + 1, codon)
                else:
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
            m = re.match(r"^([A-Z])\s+(\d+(?:\.\d+))$",line)  # پترن عوض شده چون فقط اعداد اعشاری را قبول میکرد
            
            if not m:
                log.error("amino_weights.txt line %d: bad format: %r", i + 1, line)
                raise DataFileError(f"amino_weights.txt line {i+1}: bad format {line}")
            else:
                amino = m.group(1)
                weight = float(m.group(2))
                if amino in amino_weights:
                    log.warning("amino_weights.txt line %d: duplicate amino(ignored) %s", i + 1, amino)
                else:
                    amino_weights[amino]=weight
    if not codon_table:
        log.error("codon_table.txt has no valid input")
        raise DataFileError("codon_table.txt has no valid input")
    if not amino_weights:
        log.error("amino_weights.txt has no valid input")
        raise DataFileError("amino_weights.txt has no valid input")
    return codon_table, amino_weights
