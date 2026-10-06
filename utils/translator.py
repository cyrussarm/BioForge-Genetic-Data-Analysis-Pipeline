from models.protein import Protein
from logger import get_logger
log = get_logger()

def translator(orf_obj, codon_table, weight_table):
        amino_sequence = ""
        for codon in orf_obj.codons:
            
            # اگر codon در جدول نبود خطا ندهد
            amino_ = codon_table.get(codon,None)
            if amino_ is None:
                log.warning(f"unknown codon {codon}: skipped")
                continue
            if amino_ =="*":
                continue
            amino_sequence += amino_
        orf_obj.protein = Protein(amino_sequence, weight_table)
        return orf_obj
