from umlclass import UMLClass

def create_attrs(uml_class: UMLClass) -> None:
    built_in_types = ["String", "Integer", "Float"]
    for _, attr_type in uml_class.attributes:
        if attr_type not in built_in_types:
            print(f"sig {attr_type} {{}}")

def translater(classes: dict[str, UMLClass]) -> None:
    for uml_class in classes.values():
        create_attrs(uml_class)
        
        if uml_class.inheritance is None:
            print(f"sig {uml_class.name} {{")
        else:
            print(f"sig {uml_class.name} extends {uml_class.inheritance} {{")
        
        for attr, attr_type in uml_class.attributes:
            print(f"  {attr}: one {attr_type}")
        
        print("}")