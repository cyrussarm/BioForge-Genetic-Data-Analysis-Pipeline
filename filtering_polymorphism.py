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
            if self.max_length is not None and length > self.max_length:
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
            if self.max_weight is not None and weight > self.max_weight:
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


def apply_filters(orfs, filters):
    result = list(orfs)
    for current_filter in filters:
        result = current_filter.apply(result)
    return result


def filter_orfs(
    orfs,
    min_length=0,
    max_length=None,
    min_weight=None,
    max_weight=None,
    motif=None,
):
    filters = [LengthFilter(min_length, max_length)]

    if min_weight is not None or max_weight is not None:
        filters.append(
            WeightFilter(
                min_weight=0 if min_weight is None else min_weight,
                max_weight=max_weight,
            )
        )

    if motif is not None:
        filters.append(MotifFilter(motif))

    return apply_filters(orfs, filters)


if __name__ == "__main__":
    print("filtering.py loaded successfully")
