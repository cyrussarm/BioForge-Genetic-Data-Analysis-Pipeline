class BioForgeError(Exception):
    pass

class FastaFormatError(BioForgeError):   
    pass

class InvalidSequenceError(BioForgeError):
    pass

class DataFileError(BioForgeError):
    def __init__(self, msg=None, value=None):
        super().__init__(msg)
        self.msg = msg
        self.value=value

    def __str__(self):
        message = self.msg
        if message is None:
            message = "File not found"
        if self.value is not None:
            message += (f" | in line number = {self.value}")
        return message

class DataFileFormatError(BioForgeError):
    def __init__(self, msg=None, value=None):
        super().__init__(msg)
        self.msg = msg
        self.value=value

    def __str__(self):
        message = self.msg
        if message is None:
            message = "File format warning"
        if self.value is not None:
            message += (f" | in line number = {self.value}")
        return message
   

