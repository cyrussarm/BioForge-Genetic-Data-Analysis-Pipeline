# ----------------- loading input file --------------------
import os
import re
from logger import get_logger
log = get_logger()

fasta = []
keys = []

def parser(header , line_no):
    m = re.match((r"^>(\S+)\s*(.*)$"), header)  
    seq_id = m.group(1)
    seq_header = m.group(2)
    if seq_id in keys:
        log.warning("Line %d: duplicate ID '%s'", line_no, seq_id)
        # هشدار برای تکراری بودن آیدی
    else: 
            keys.append(seq_id)
    return seq_id, seq_header

def isheader(line):
    m = re.match((r"^>(\S+)\s*(.*)$"), line)
    if m:
       return True
    else:
        return False

def issequence(line):
    m = re.match((r"^[ACGT]+$"), line.upper()) # حروف کوچیک هم پذیرفته میشوند
    if m:
        return True
    else:
        return False
  
def input_loader(filename): 

    if not os.path.exists(filename):
        log.error("Input FASTA not found: %s", filename) # اگر فایل فستا نباشد روی لاگ به این صورت اخطار می دهد
        raise FileNotFoundError("input FASTA not found")

    seq_id = None
    seq_header = None
    has_seq = False
    header_line = 0

    with open(filename, "r", encoding="utf-8") as f:
        n = 0
        for line in f :
            n += 1
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if isheader(line):
                if seq_id is not None and not has_seq:
                    log.error("Header without sequence: '%s'", seq_id)
                seq_id, seq_header = parser(line, n)
                header_line = n
                has_seq = False

            elif seq_id is None:
                log.error("Line %d: sequence before the first header", n)

            elif issequence(line):
                fasta.append({"id":seq_id, "description":seq_header, "sequence":line})
                has_seq = True

            else:
                log.error("Line %d: invalid sequence in '%s': %r", n, seq_id, line)

    if seq_id is not None and not has_seq:
        log.error("line %d :Header without sequence: '%s'",header_line, seq_id)
    if not fasta:
        log.error("No valid records found in %s", filename)
    return fasta