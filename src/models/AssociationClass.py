class AssociationClass:
    def __init__(
        self,
        name,
        association_type,
        from_class,
        from_mult,
        to_class,
        to_mult,
        left=None,
        right=None,
    ):
        self.name = name
        self.association_type = association_type
        self.from_class = from_class
        self.from_mult = from_mult
        self.to_class = to_class
        self.to_mult = to_mult
        self.left = left
        self.right = right

    def __str__(self):
        return f"Association of type {self.association_type}({self.name}: {self.from_class}({self.from_mult}) -> {self.to_class}({self.to_mult}))"

    def __repr__(self):
        return str(self)
