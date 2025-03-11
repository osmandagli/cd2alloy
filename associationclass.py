class AssociationClass:
    def __init__(self, name, from_class, from_mult, to_class, to_mult):
        self.name = name
        self.from_class = from_class
        self.from_mult = from_mult
        self.to_class = to_class
        self.to_mult = to_mult

    def __str__(self):
        return f"Association({self.name}: {self.from_class}({self.from_mult}) -> {self.to_class}({self.to_mult}))"

    def __repr__(self):
        return str(self)
