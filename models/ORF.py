class ORF:     
    def __init__(self, codons, strand, frame, start_pos, protein, is_complete, source_id=None):
        self.codons = codons
        self.strand = strand
        self.frame = frame
        self.start_pos = start_pos
        self.is_complete = is_complete 
        self.protein = None      # protein is an object         
        self.id = None  
        self.source_id = source_id # آیدی اولیه  

    def __str__(self):
        return (
                f"codons={self.codons},\n"
                f"strand={self.strand},\n"
                f"frame={self.frame},\n"
                f"start={self.start_pos},\n"
                f"complete={self.is_complete},\n"                            
                f"id={self.id}"
                )

    

