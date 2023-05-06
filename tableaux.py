import numpy 

class Tableaux:
    def __init__(self, dictionary=None):
        if dictionary == None:
            dictionary ={}
        self.map = {}
        for key, value in dictionary.items():
            self.map[key] = value
        self.max_row = max({x for x,y in self.map} | {0})
        self.max_column = max({y for x,y in self.map} | {0})

    def __getitem__(self,entry):
        return self.map.get(entry)
    
    def __repr__(self) -> str:
        pass
