from logger import get_logger
from models.BioForgeExceptions import FilteringError
from abc import ABC, abstractmethod
                                      

log = get_logger()



class Filter(ABC):

    @abstractmethod
    def apply(self, orfs):
        pass

class LengthFilter(Filter):
    def __init__(self, min_length, max_length=None):
        self.validate(min_length, max_length)
        self.min_length = min_length
        self.max_length = max_length
       
    @staticmethod
    def validate(min_, max_):
        if min_ < 0:
            msg = "min_length cannot be negative"
            log.error(f"FilteringError: {msg}")
            raise FilteringError(msg)
        if max_ is not None and max_ < min_:
            msg = "max_length must be >= min_length"
            log.error(f"FilteringError: {msg}")
            raise FilteringError(msg)
        return True


    def apply(self, orfs):
        result = []
        for orf in orfs:
            if orf.protein is None:
                continue
            length = len(orf.protein)
            if length < self.min_length:
                continue
            if self.max_length is not None and length > self.max_length:
                continue
            result.append(orf)
        return result


class WeightFilter(Filter):
    def __init__(self, min_weight, max_weight=None):
        self.validate(min_weight, max_weight)
        self.min_weight = min_weight
        self.max_weight = max_weight
    
    @staticmethod
    def validate(min_, max_):
        if min_ < 0:
            msg = "min_weight cannot be negative"
            log.error(f"FilteringError: {msg}")
            raise FilteringError(msg)
        if max_ is not None and max_ < min_:
            msg = "max_weight must be >= min_weight"
            log.error(f"FilteringError: {msg}")
            raise FilteringError(msg)
        return True

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


class MotifFilter(Filter):
    def __init__(self, motif):
        if not motif:
            msg = "Motif cannot be empty"
            log.error(f"FilteringError: {msg}")
            raise FilteringError(msg)            
        self.motif = motif

    def apply(self, orfs):        
        result = []
        for orf in orfs:            
            for motif_ in orf.motifs:
                if motif_["sequence"] == self.motif:
                    result.append(orf)
                    break
        return result


def apply_filters(orfs, filters):
    if not orfs:
        result = []
        return result
    result = list(orfs)
    for filter_ in filters:
        result = filter_.apply(result)
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



