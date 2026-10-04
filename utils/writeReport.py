def write_report(orfs, output_path):
    from pathlib import Path
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for orf in orfs:
            f.write(f"ID: {orf.id}\n")            
            f.write(f"Strand: {orf.strand}\n")
            f.write(f"Frame: {orf.frame}\n")
            f.write(f"Start Position: {orf.start_pos}\n")
            
            if orf.protein is not None:
                f.write(f"Protein: {orf.protein.amino_sequence}\n")
                f.write(f"Molecular Weight: {orf.protein.molecular_weight:.3f}\n")
            else:
                f.write("Protein: None\n")
                f.write("Molecular Weight: None\n")
            
            if orf.is_complete:
                f.write("Status: Complete\n")
            else:
                f.write("Status: Incomplete\n")
            
            # Motifs
                f.write("-------- THIS PART WILL BE COMPLETED _________")
                
            
            f.write("------------------------------" + "\n")