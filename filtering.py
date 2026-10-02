
class LengthFilter:

    def __init__(self, min_length=0, max_length=None):
        if min_length < 0:
            raise ValueError("min_length cannot be negative")

        if max_length is not None and max_length < min_length:
            raise ValueError("max_length must be >= min_length")

        self.min_length = min_length
        self.max_length = max_length

    def apply(self, orfs):
        result = []

        for orf in orfs:
            length = len(orf.protein)

            if length < self.min_length:
                continue

            if self.max_length is not None:
                if length > self.max_length:
                    continue

            result.append(orf)

        return result


class WeightFilter:

    def __init__(self, min_weight=0, max_weight=None):
        if min_weight < 0:
            raise ValueError("min_weight cannot be negative")

        if max_weight is not None and max_weight < min_weight:
            raise ValueError("max_weight must be >= min_weight")

        self.min_weight = min_weight
        self.max_weight = max_weight

    def apply(self, orfs):
        result = []

        for orf in orfs:
            weight = orf.molecular_weight

            if weight is None:
                continue

            if weight < self.min_weight:
                continue

            if self.max_weight is not None:
                if weight > self.max_weight:
                    continue

            result.append(orf)

        return result


class MotifFilter:

    def __init__(self, motif):
        if not motif:
            raise ValueError("Motif cannot be empty")

        self.motif = motif

    def apply(self, orfs):
        result = []

        for orf in orfs:
            for found_motif in orf.motifs:
                if found_motif["sequence"] == self.motif:
                    result.append(orf)
                    break

        return result


def filter_orfs(
    orfs,
    min_length=0,
    max_length=None,
    min_weight=None,
    max_weight=None,
    motif=None
):
   

    result = list(orfs)
    
    length_filter = LengthFilter(min_length, max_length)
    result = length_filter.apply(result)

    if min_weight is not None or max_weight is not None:
        weight_filter = WeightFilter(
            min_weight=0 if min_weight is None else min_weight,
            max_weight=max_weight
        )
        result = weight_filter.apply(result)

    if motif is not None:
        motif_filter = MotifFilter(motif)
        result = motif_filter.apply(result)

    return result