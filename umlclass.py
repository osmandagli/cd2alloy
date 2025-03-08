class UMLClass:
    def __init__(self, class_id, name):
        self.class_id = class_id
        self.name = name
        self.attributes = []  # List of (attribute, type)
        self.inheritance = None  # Parent class name
        self.associations = []  # List of (assoc_name, from_class, from_mult, to_class, to_mult)
    
    def add_attribute(self, name, attr_type):
        self.attributes.append((name, attr_type))
    
    def set_inheritance(self, parent_name):
        self.inheritance = parent_name
    
    def add_association(self, assoc_name, from_class, from_mult, to_class, to_mult):
        self.associations.append((assoc_name, from_class, from_mult, to_class, to_mult))
        
    def print_associations(self):
        print(f"Associations for class {self.name}:")
        for assoc_name, from_class, from_mult, to_class, to_mult in self.associations:
            print(f"  {assoc_name}: {from_class} ({from_mult}) -> {to_class} ({to_mult})")
    