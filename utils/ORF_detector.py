def find_reading_frames(seq):    
    RF_list = []
    
    start = [0,1,2]
    for k in start:  
        RF = ""      
        pos = []
        for i in range(start[k],len(seq),3):
            pos.append(i)   
        if k>0:
            str_= seq[:pos[0]] + "|" 
            RF += str_ 
        for i in range(len(pos)-1):            
            str_ = seq[pos[i]:pos[i+1]] + "|"
            RF += str_
        str_ = seq[pos[-1]:]
        RF += str_
        RF_list.append((start[k],RF))
    return RF_list  

# input: sequence
# output: [ORFها]
def ORF_detection(sequence, complement, stop_codon):
    start_codon = "AUG"       
    forward = find_reading_frames(sequence)
    reveres = find_reading_frames(complement)

    for elem in forward:
        codons = elem[1].split("|")
        print(codons)
    for elem in reveres:
        codons = elem[1].split("|")
        print(codons)
    


    
    strand = "Forward"
    Frame = 0
    start_pose = 1
    Protein = None
    is_complete = True
