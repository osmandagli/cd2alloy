from associationclass import AssociationClass
from typing import List


class UMLClass:
    def __init__(self, class_id: str, name: str):
        self.class_id: str = class_id
        self.name: str = name
        self.attributes: List[tuple] = []  # List of (attribute, type)
        self.inheritance: str | None = None  # Parent class name
        self.children: List[str] = [] # List of children class names
        self.associations: List[AssociationClass] = (
            []
        )  # List of AssociationClass instances
        self.facts: List[str] = []  # List of sig facts

    def add_attribute(self, name: str, attr_type: str):
        self.attributes.append((name, attr_type))

    def set_inheritance(self, parent_name: str):
        self.inheritance = parent_name
        
    def add_child(self, child_name: str):
        self.children.append(child_name)

    def add_association(
        self,
        assoc_name,
        from_class,
        from_mult: str,
        to_class: str,
        to_mult: str,
    ):
        self.associations.append(
            AssociationClass(assoc_name, from_class, from_mult, to_class, to_mult)
        )

    def add_fact(self, fact: str):
        self.facts.append(fact)

    def print_associations(self):
        print(f"Associations for class {self.name}:")
        for association in self.associations:
            print(f"  {association}")
