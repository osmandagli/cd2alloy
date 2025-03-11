from umlclass import UMLClass
import re

created_classes = []

def create_attrs(uml_class: UMLClass, file) -> None:
    built_in_types = ["string", "int"]
    for _, attr_type in uml_class.attributes:
        if attr_type not in built_in_types and attr_type not in created_classes:
            created_classes.append(attr_type)
            file.write(f"sig {attr_type} {{}}\n")

def create_associations(uml_class: UMLClass, file) -> None:
    for association in uml_class.associations:
        multiplicity = get_association_type(association[4])

        if multiplicity == "lower_upper_set":
            lower, upper = association[4].split("..")
            uml_class.add_fact((association[0], lower, upper))

        file.write(f"  {association[0]}: {multiplicity} {association[3]}\n")

def create_constraints(uml_class: UMLClass, file) -> None:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    i = 0
    file.write("fact {\n")
    for fact in uml_class.facts:
        file.write(f"  all {alphabet[i]}: {uml_class.name} | #{alphabet[i]}.{fact[0]} >= {fact[1]} && #{alphabet[i]}.{fact[0]} =< {fact[2]}\n")
        i += 1
    file.write("}\n")

def get_association_type(value: str) -> str:
    association_multiplicity = {
        "0..1": "lone",
        "0..*": "set",
        "1": "one",
        "1..*": "some",
        r"\d+\.\.\d+" : "lower_upper_set"
    }
    if value in association_multiplicity:
        return association_multiplicity[value]

    # Check Regex
    for pattern, assoc_type in association_multiplicity.items():
        if re.match(pattern, value):
            return assoc_type
        
    return "set"

def translater(classes: dict[str, UMLClass], filename="output.alloy") -> None:
    with open(filename, "w") as file:
        for uml_class in classes.values():
            create_attrs(uml_class, file)

            if uml_class.inheritance is None:
                file.write(f"sig {uml_class.name} {{\n")
            else:
                file.write(f"sig {uml_class.name} extends {uml_class.inheritance} {{\n")

            for attr, attr_type in uml_class.attributes:
                file.write(f"  {attr}: one {attr_type}\n")

            create_associations(uml_class, file)
            
            file.write("}\n")

            if uml_class.facts:
                print(uml_class.facts)
                create_constraints(uml_class, file)
