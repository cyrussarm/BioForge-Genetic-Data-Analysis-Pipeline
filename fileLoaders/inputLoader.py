# ----------------- loading input file --------------------
import os
import re

fasta = []
keys = []

def parser(header):
    m = re.match((r"^>(\S+)\s*(.*)$"), header)  
    if m: 
        seq_id = m.group(1)
        seq_header = m.group(2)
        if seq_id in keys:
            print("Tekrari")
        else: 
            return seq_id, seq_header

def isheader(line):
    m = re.match((r"^>(\S+)\s*(.*)$"), line)
    if m:
       return True
    else:
        return False

def issequence(line):
    m = re.match((r"^[ACGT]+$"), line)
    if m:
        return True
    else:
        return False
  
def input_loader(filename): 

    if not os.path.exists(filename):
        raise FileNotFoundError("input FASTA not found")

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip() 
            if isheader(line):
                res = parser(line)                
                seq_id = res[0]
                seq_header = res[1]               
              
            elif issequence(line):                          
                fasta.append({"id":seq_id, "description":seq_header, "sequence":line})
                
            else:               
                continue
    return fasta
                
