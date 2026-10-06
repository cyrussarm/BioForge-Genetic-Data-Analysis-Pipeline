# ----------------- loading input file --------------------
import os
import re
from logger import get_logger
from models.BioForgeExceptions import FastaFormatError, InvalidSequenceError

log = get_logger()

# بررسی بودن یا نبودن فایل- در صورت نبودن پیام خطا لاگ شده و برنامه متوقف خواهد شد
def validate_file_exist(filename):      
    if not os.path.exists(filename): 
        msg = "FASTA input file not found"      
        log.error(msg)
        raise FastaFormatError(msg)
    return True

def is_file_empty(filename):
    with open(filename) as f:
        f.seek(0)
        start = f.tell()
        f.seek(0,2)
        stop = f.tell()
        if start==stop:
            msg = "FASTA input file is empty"
            log.error(f"{msg}")
            raise FastaFormatError(msg)
        # برگرد به ابتدای فایل
        f.seek(0)

def parser(header, keys):
    add_to_file = True
    m = re.match((r"^>(\S+)\s*(.*)$"), header)  
    if m: 
        seq_id = m.group(1)
        seq_header = m.group(2)
        duplicated = False
        # ثبت آیدی تکراری در لاگ
        if seq_id in keys:
            log.warning(f"duplicated sequence ID found in FASTA file: {seq_id}")                
            duplicated = True        
            return duplicated, seq_id, seq_header         
        else: 
            keys.add(seq_id)            
            log.info(f"Sequence found: id : {seq_id} | header : {seq_header}")
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

    fasta = []
    keys = set()
    # بررسی بودن یا نبودن فایل ورودی
    validate_file_exist(filename) 

    # تشخیص فایل خالی
    is_file_empty(filename)

    _ = "" 
    seq_id = None
    seq_header = ""
    seq_is_invalid = False
    duplicated_no = 0
    invalid_no = 0
    header_found = False
    sequence_found = False
    seq_is_dupplicated = False
    
    with open(filename, "r", encoding="utf-8") as f:
        for line_no,line in enumerate(f):
            line = line.strip() 
               # نادیده گرفتن خطوط خالی و کامنت
            if not line or line.startswith("#"):
                continue
             # در سکوئنس حروف کوچک را هم اکی کند
            line_ = line.upper()
            if isheader(line):
                if header_found and not sequence_found:
                    msg = f"header without sequence: {seq_id}"
                    log.error(msg)
                    raise FastaFormatError(msg)  
                header_found = True
                
                # اگر به هدر رسیدی و دیدی سکوئنس خالی نشده ذخیره اش کن . یک سکوئنس کامل به لیست اضافه کن
                if _:
                    fasta.append({"id":seq_id, "description":seq_header, "sequence":_})
                _=""
                sequence_found = False
                
                res = parser(line, keys)   
                seq_is_dupplicated = res[0]              
                seq_id = res[1]
                seq_header = res[2]  
                if seq_is_dupplicated :
                    duplicated_no += 1                  
                              
            elif issequence(line_): 
                if not header_found:
                    msg = "sequence found before first header line"
                    log.error(f"{msg} {filename}")
                    raise FastaFormatError(msg)

                sequence_found = True

                if not seq_is_dupplicated and not seq_is_invalid:
                    # تا وقتی که پترن خط سکوئنس است خط را به مقدار قبلی سکوئنس اضافه کن
                     _ += line_     

            else:                  
                if not header_found:
                    # توقف در صورتی که قبل از اولید هدر متن وجود داشته باشد
                    msg = "sequence found before first header "
                    log.error(f"{msg} (line {line_no})")
                    raise FastaFormatError(msg)
                sequence_found = True
                if not seq_is_dupplicated and not seq_is_invalid:
                    seq_is_invalid = True
                    invalid_no += 1
                    _ = ""
                    log.error(f"skipped record (Invalid sequence): '{seq_id}' (line {line_no}): {line_} ")
        # بعد از آخرین خط اگر سکوئنس مونده سیوش کن
        if _ and not seq_is_invalid:
            fasta.append({"id":seq_id, "description":seq_header, "sequence":_})            
        elif header_found and not sequence_found:
            msg = f"header without sequence: {seq_id}"
            log.error(msg)
            raise FastaFormatError(msg)

    if not keys:
        msg = "no sequence in fasta file"
        log.error(f"{msg} {filename}")
        raise FastaFormatError(msg) 

    log.info(f"FASTA parsing finished: {len(fasta)} valid records, "
             f"{duplicated_no} duplicate IDs skipped, {invalid_no} invalid records")

    if not fasta:
        log.warning("No valid records found in FASTA file")    
    return fasta