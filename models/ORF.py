class ORF:
    def __init__(self,sequence, strand, Frame, start_pos, Protein, is_complete):
        self.sequence = sequence
        self.strand = strand
        self.Frame = Frame
        self.start_pos = start_pos
        self.Protein = Protein
        self.is_complete = is_complete
        

    def __str__(self):
        return f"an ORF maked for sequence: {sequence}"


    

