class Sequence:
    def __init__(self,seq_id,description,sequence):
            self.id = seq_id
            self.description = description
            self.sequence = sequence.upper()
            if not self.validate():
                raise Exception ("InvalidSequenceError")

    def validate(self):
        valids = ("T", "A", "G", "C")
        for s in self.sequence:
            if not s in valids:
                return False
        return True               
    
    def complement(self):
        comps = {"A":"T", "T":"A", "C":"G", "G":"C"}
        res = ""
        for s in self.sequence:
            res += comps[s]
        return res        

    def reverse_complement(self):
        comp = self.complement()
        reverse = comp[::-1]
        return reverse

    def dna_to_rna(self):
        return self.sequence.replace("T", "U")
                
    def gc_content(self):
        g_cont = self.sequence.count("G")
        c_cont = self.sequence.count("C")
        total_len = len(self.sequence)
        if total_len==0:
            return None
        else:
            return (g_cont+c_cont)/total_len*100

    def __str__(self):
        return f"sequence id: {self.id} \n description: {self.description} \n sequence: {self.sequence}"
