import os
import re
from models.Exceptions import *
import logging
import logging_config

# بررسی بودن یا نبودن فایل- در صورت نبودن پیام خطا لاگ شده و برنامه متوقف خواهد شد
def validate_file_exist(filename, msg=None):  
    print(os.path.exists(filename)) 
    print(filename)      
    if not os.path.exists(filename):
        if msg is None:
            msg = "data file not found"
        logging.error(f"{msg} {filename}")
        raise DataFileError(msg=msg, value=filename)
    return True

# فایل های داده را میخواند و جدول کدون + جدول وزن آمینوها + کدونهای استاپ را برمیگرداند
# جدول کدن یک دیکشنری است
# جدول آمینو یک دیکشنری است
# کدونهای استاپ یک تاپل است
def data_loader(basePath):  
    # تعیین مسیر فایلها   
    codonfile = os.path.join(basePath, "data", "codon_table.txt")
    aminofile = os.path.join(basePath, "data", "amino_weights.txt")
    # ایجاد دو دیکشنری جهت ذخیره داده های خوانده شده
    codon_table = {} 
    amino_weights = {}
    # تاپل استاپ کدون ها
    stop_codons = ()
    # در صورتی که فایل وجود ندارد در لاگ ثبت کن، پیام خطا رایز کن و استاپ کن
    validate_file_exist(codonfile,"codon table file not found")  
    # فایل را بخوان
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
            m = re.match(r"^([ACGTU]{3})\s+(\S)$",line) # یعنی خط با سه تا از کاراکترهای داخل کروشه شروع بشه + فاصله + یک استرینگ دیگر
            if not m:
                logging.warning(f"codon format mot found in line {i+1}")
                print(f" WARNING: codon format mot found in line {i+1}")
            else:
                codon = m.group(1)
                amino = m.group(2)
                if codon in codon_table:
                    logging.warning(f"duplicated codon if file found : {codon}")
                    print(f"WARNING: duplicated codon if file found : {codon}")
                codon_table[codon]=amino
                if amino=="*":                    
                    stop_codons += (codon,)

# فایل مربوط به وزن آمینوها را بخوان
    validate_file_exist(aminofile,"amino weights file not found")  
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
            # چک کردن فرمت خط و چاپ پیام وارنینگ در صورت لزوم
            if not m:
                logging.warning(f"amino format mot found in line {i+1}")
                print(f" WARNING: amino format not found in line {i+1}")
            else:
            # تفکیک گروه های الگو
                amino = m.group(1)
                weight = m.group(2)
                if amino in amino_weights:
                    logging.warning(f"duplicated amino if amino_weights file found : {amino}")
                    print(f"WARNING: duplicated amino if amino_weights file found : {amino}")
                amino_weights[amino]=weight

    return codon_table, amino_weights, stop_codons
        


    







    
    

