class Annotate:    
    def __init__(self,prefix="BFG_"):
        self.prefix = prefix
        self.counter = 0

    def annotate(self, ORFs): 
        for orf in ORFs:
            self.counter += 1  
            orf.id = f"{self.prefix}{self.counter:03d}"  
        return ORFs