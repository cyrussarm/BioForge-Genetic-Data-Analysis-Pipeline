# ----------------- loading input file --------------------
import re
import os
from models.Exceptions import *
import logging
import logging_config

# بررسی بودن یا نبودن فایل- در صورت نبودن پیام خطا لاگ شده و برنامه متوقف خواهد شد
def validate_file_exist(filename, msg=None):  
    # print(os.path.exists(filename)) 
    # print(filename)      
    if not os.path.exists(filename):
        if msg is None:
            msg = "input file not found"
        logging.error(f"{msg} {filename}")
        raise DataFileError(msg=msg, value=filename)
    return True

def is_file_empty(filename):
    with open(filename) as f:
        f.seek(0)
        start = f.tell()
        f.seek(0,2)
        stop = f.tell()
        if start==stop:
            msg = "input file is empty"
            logging.error(f"{msg} {filename}")
            raise DataFileError(msg=msg, value=filename)
        # برگرد به ابتدای فایل
        f.seek(0)
    
fasta = []
keys = set()

def parser(header):
    add_to_file = True
    m = re.match((r"^>(\S+)\s*(.*)$"), header)  
    if m: 
        seq_id = m.group(1)
        seq_header = m.group(2)
        duplicated = False
        # ثبت آیدی تکراری در لاگ
        if seq_id in keys:
            logging.warning(f"duplicated sequence ID found in FASTA file: {seq_id}") 
            print(f"duplicated sequence ID found in FASTA file: {seq_id}")   
            duplicated = True        
            return duplicated, seq_id, seq_header         
        else: 
            keys.add(seq_id)            
            logging.info(f"Sequence found: \n id : {seq_id} \n header : {seq_header}")
            duplicated = False
            return duplicated, seq_id, seq_header

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
    # بررسی بودن یا نبودن فایل ورودی
    validate_file_exist(filename, msg=None) 

    # تشخیص فایل خالی
    is_file_empty(filename)

    _ = ""    
    header_found = False
    sequence_found = False
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip() 
             # در سکوئنس حروف کوچک را هم اکی کند
            line_ = line.upper()
            if isheader(line):
                if header_found and not sequence_found:
                    logging.warning(f"header without sequence found: {seq_id}")                
                header_found = True
                
                # اگر به هدر رسیدی و دیدی سکوئنس خالی نشده ذخیره اش کن . یک سکوئنس کامل به لیست اضافه کن
                if _:
                    fasta.append({"id":seq_id, "description":seq_header, "sequence":_})
                _=""
                sequence_found = False
                
                res = parser(line)   
                seq_is_dupplicated = res[0]              
                seq_id = res[1]
                seq_header = res[2]                 
                              
            elif issequence(line_): 
                if not header_found:
                    msg = "sequence found before first header line"
                    logging.error(f"{msg} {filename}")
                    raise DataFileError(msg=msg, value=filename)

                sequence_found = True

                if not seq_is_dupplicated:
                    # تا وقتی که پترن خط سکوئنس است خط را به مقدار قبلی سکوئنس اضافه کن
                     _ += line_     

            else:  
                if line_:
                    logging.warning(f"Ignored line: not a header neither a sequence: {line_}")                        
                continue
        # بعد از آخرین خط اگر سکوئنس مونده سیوش کن
        if _:
            fasta.append({"id":seq_id, "description":seq_header, "sequence":_})            
        elif header_found and not sequence_found:
            logging.warning(f"header without sequence found: {seq_id}")

    if not len(keys):
        msg = "no sequence in fasta file"
        logging.error(f"{msg} {filename}")
        raise DataFileError(msg=msg, value=filename)     
    return fasta
                
