class Couple:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return self.first.__str__() + ' ' + self.second.__str__()
