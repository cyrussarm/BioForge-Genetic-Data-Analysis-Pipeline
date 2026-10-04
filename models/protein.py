from logger import get_logger
log = get_logger()

class Protein:
    def __init__(self, amino_sequence, weight_table):         
        self.amino_sequence = amino_sequence
        self.molecular_weight = self.calc_weight(amino_sequence, weight_table)
        self.motifs = []
       
    @staticmethod   
    def calc_weight(amino_sequence, weight_table):
        # protein_weight = sum(residue_weights) + 18.015
        MW_ = 18.015
        for amino in amino_sequence:            
            # اگر codon در جدول نبود خطا ندهد
            MW_ += weight_table.get(amino,0)            
        return MW_    
    
    def motif_detector(self, motif_):
        if not motif_:
            return []        
        target_string = self.amino_sequence
        motif_positions = []            
        start = 0
        while True:
            m = target_string.find(motif_, start)
            if m == -1:
                break
            motif_positions.append(m)
            start = m + len(motif_)  
        for pos in motif_positions:
               self.motifs.append({"sequence": motif_, "position": pos})
        return motif_positions 

    def __len__(self):
        return(len(self.amino_sequence))   

    def __str__(self):
        return f"Protein(name={self.amino_sequence}, MW = {self.molecular_weight})"  
    
      
