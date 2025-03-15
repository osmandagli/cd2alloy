class AssociationClass:
    def __init__(
        self,
        name,
        association_type,
        from_class,
        from_lower_mult,
        from_upper_mult,
        to_class,
        to_lower_mult,
        to_upper_mult,
    ):
        self.name = name
        self.association_type = association_type
        self.from_class = from_class
        self.from_lower_mult = from_lower_mult
        self.from_upper_mult = from_upper_mult
        self.to_class = to_class
        self.to_lower_mult = to_lower_mult
        self.to_upper_mult = to_upper_mult

    def __str__(self):
        return f"Association of type {self.association_type}({self.name}: {self.from_class}({self.from_lower_mult}..{self.from_upper_mult}) -> {self.to_class}({self.to_lower_mult}..{self.to_upper_mult}))"

    def __repr__(self):
        return str(self)
