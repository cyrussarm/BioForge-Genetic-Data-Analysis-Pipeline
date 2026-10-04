from models.sequence import Sequence
from models.ORF import ORF

# input: sequence object
# output: [ORFها]
def ORF_detection(sequence_obj):
    start_codon = "AUG"
    stop_codon = ["UAA", "UAG", "UGA"]  

    sequenceRNA = sequence_obj.dna_to_rna(sequence_obj.sequence)
    RcomplementRNA = sequence_obj.reverse_complement()
    RcomplementRNA = sequence_obj.dna_to_rna(RcomplementRNA)

    strands = {"forward":sequenceRNA , "reverse":RcomplementRNA}
    frames = [0,1,2]
    ORFs = []

    for strand in strands:
        seq = strands[strand]         
        for frame in frames:
            start=False            
            codons_of_orf=[]
            start_pos = None
            i=frame

            while i<len(seq)-2:
                codon = seq[i:i+3]            
                if codon==start_codon and not start:
                    start = True                    
                    start_pos=i
                    codons_of_orf.append(codon)                    
                
                elif codon in stop_codon and start: 
                    is_complete=True
                    codons_of_orf.append(codon)
                    if strand=="reverse":
                        start_pos = len(sequence_obj.sequence)-(start_pos+len(codons_of_orf)*3)
                    orf = ORF(codons_of_orf, strand, frame, start_pos, None, is_complete)
                    ORFs.append(orf) 
                    start = False                  
                    codons_of_orf=[]
                elif start:
                    codons_of_orf.append(codon)                   
                    
                i+=3

            if start and codons_of_orf:
                if strand=="reverse":
                    start_pos = len(sequence_obj.sequence)-(start_pos+len(codons_of_orf)*3)
                orf = ORF(codons_of_orf, strand, frame, start_pos, None, False)
                ORFs.append(orf)

    return ORFs
        #     print(f"codon: {codon}. seq={seq}, seq1={sequenceRNA}")


    
    
    
