import fileLoaders.dataLoader
codons, weights = fileLoaders.dataLoader.data_loader('codon_table.txt', 'amino_weights.txt')

def translator(orf):
    protein = ''
    for c in orf:
        if codons[c] == '*':
            break
        protein += codons[c]
    return protein