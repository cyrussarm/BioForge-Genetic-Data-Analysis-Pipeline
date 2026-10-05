import os
import argparse
from pathlib import Path

from fileLoaders.dataLoader import data_loader
from fileLoaders.inputLoader import input_loader
from models.sequence import Sequence
from models.ORF import ORF
from models.annotation import Annotate

from utils.filtering import LengthFilter, WeightFilter, MotifFilter, apply_filters
from utils.ORF_detector import ORF_detection
from utils.translator import translator
from utils.writeReport import write_report 

from logger import setup_logging
from models.BioForgeExceptions import BioForgeError

def parse_args():
    parser = argparse.ArgumentParser(
        description ="BioForge - Genetic Data Analysis Pipeline"
    )    
    parser.add_argument("--input", type=Path, required=True, help="Path to input FASTA file")    
    parser.add_argument("--out", type=Path, required=True,  help="Output directory")    
    parser.add_argument("--min-length", type=int, required=True)  
    parser.add_argument("--min-weight", type=float, default=None,
                    help="Minimum molecular weight (optional)")
    parser.add_argument("--max-weight", type=float, default=None,
                    help="Maximum molecular weight (optional)")  
    parser.add_argument("--motif", action="append", default=None, help="optinal")
    return parser.parse_args()

def main():
    args = parse_args()

     # ساخت پوشه output
    args.out.mkdir(parents=True, exist_ok=True)    

    # path managment
    ROOT_DIR = os.path.abspath(os.curdir)    
    log_path = os.path.join(ROOT_DIR, "output")     
    codon_data_path = os.path.join(ROOT_DIR, "data", "codon_table.txt") 
    amino_data_path = os.path.join(ROOT_DIR, "data", "amino_weights.txt") 

    log = setup_logging(log_path)
    log.info("BioForge started") 

    try:
        # داده ها
        res = data_loader(codon_data_path,amino_data_path)
        codon_table = res[0]
        weight_table = res[1]
        log.info("Data files loaded")

        # لود فایل FASTA
        FASTA = input_loader(args.input) 
        log.info(f"FASTA file loaded: Number of recoreds = {len(FASTA)}")

         # لیست Motif 
        motifs = [] 
        if args.motif:
            motifs = args.motif 

        all_orfs = []

        all_seq_obj = []

        for record in FASTA:     

            # ساخت سکوئنس
            seq_obj = Sequence(record["id"], record["description"], record["sequence"])

            # جستجوی ORFها
            ORFs = ORF_detection(seq_obj) 
                        
            log.info(f"Found {len(ORFs)} ORFs in {seq_obj.id}")

            # traslation:            
            if ORFs:
                 for orf in ORFs:
                    translator(orf, codon_table, weight_table)

                    for motif_ in motifs:
                        orf.protein.motif_detector(motif_)

            # Filtering
            filters = [LengthFilter(min_length=args.min_length)]
            log.info(f"LengthFilter for min_length: {args.min_length}")
            
            if args.min_weight is not None or args.max_weight is not None:
                min_weight = args.min_weight
                if args.min_weight is None:
                    min_weight = 0
                filters.append(WeightFilter(min_weight=min_weight, max_weight=args.max_weight))
                if args.min_weight:
                    log.info(f"WeightFilter for min_weight: {args.min_weight}")
                if args.max_weight:
                    log.info(f"WeightFilter for max_weight: {args.max_weight}")

            if args.motif:
                for motif_ in args.motif:
                    filters.append(MotifFilter(motif_))
                log.info(f"MotifFilter for: {args.motif}")
            ORFs = apply_filters(ORFs, filters)

            # ذخیره ORFها در سکوئنس (برای گزارش)
            seq_obj.orfs = ORFs

            all_seq_obj.append(seq_obj)
            all_orfs.extend(ORFs)
            
        # annotation
        if all_orfs:
            Annotate().annotate(all_orfs)

        # Reporting
        report_path = args.out / "report.txt"
        write_report(all_seq_obj, report_path)
        log.info(f"Report saved to {report_path}")   

    except BioForgeError as e:
        log.error(f"BioForgeError: {e}")
        raise 
    except Exception as e:
        log.error(f"unexpected error: {e}", exc_info=True)
        raise BioForgeError(f"error: {e}")


if __name__ =="__main__":
    main()
    
 


   
     
    
