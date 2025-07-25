import random


class Code:
    def __init__(self):
        pass
    
    @staticmethod
    def make_code() -> int:
        code = random.randint(100000, 999999)
        return code


code_manager = Code()

