from pathlib import Path

def write_report(sequences, output_path):    
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f'{"#"*40} \n')
        f.write("BioForge Report - G6 \n")
        f.write(f'{"#"*40} \n\n')
        for ind, seq in enumerate(sequences):
            f.write(f"{"="*40}\n")
            f.write(f"\nid = {seq.id}\n")
            f.write(f"description = {seq.description}\n")
            f.write(f"sequence = {seq.sequence}\n")
            f.write(f"complement = {seq.complement()}\n")
            f.write(f"reverse_complement = {seq.reverse_complement()}\n")
            f.write(f"GC content = {seq.gc_content()}\n")
            f.write(f"number of ORFs = {len(seq.orfs)}\n")
            compeletes = 0
            in_compeletes = 0
            for orf in seq.orfs:
                if orf.is_complete:
                    compeletes += 1
                else:
                    in_compeletes += 1
            f.write(f"number of compelete ORFs = {compeletes}\n")
            f.write(f"number of in_compelete ORFs = {in_compeletes}\n")
            f.write(f"======== list of ORFs (after applying filters) ======== \n")
            for ind, orf in enumerate(seq.orfs):
                f.write(f"ORF No. : {ind+1}\n")
                f.write(f"\tIs_compelete: {orf.is_complete}\n")
                f.write(f"\tORF codons: {orf.codons}\n") 
                f.write(f"\tID: {orf.id}\n") 
                f.write(f"\tStrand: {orf.strand}\n")
                f.write(f"\tframe: {orf.frame}\n")
                if orf.strand == "forward":
                    f.write(f"\tstart position (1-based): {orf.start_pos}\n")
                else:
                    f.write(f"\tstart position (1-based and respect to the sequence): {orf.start_pos}\n")
                if orf.protein is not None:
                    f.write(f"\tProtein's name: {orf.protein.amino_sequence}\n")
                    f.write(f"\tProtein's Molecular Weight: {orf.protein.molecular_weight:.3f}\n")
                    f.write(f"\tProtein's length: {len(orf.protein)} \n")
                else:
                    f.write("\tProtein's name: None\n")
                    f.write("\tProtein's Molecular Weight: None\n")
                    f.write(f"\tProtein's length: None \n")
                
