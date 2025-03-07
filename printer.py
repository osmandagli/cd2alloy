 
def print_ocl_constraints(constraints):
    print("\nOCL Constraints:")
    for constraint in constraints:
        print(f"  - Constraint: {constraint['name']} (ID: {constraint['id']})")
        print(f"    Expression: {constraint['expression']}")
        print(f"    Applies to: {constraint['applies_to']}")

# TODO: Modify print fucntion to print the new data structure
def print_classes(classes):
    print("\nUML Classes and Attributes:")
    for _, data in classes.items():
        print(f"  - Class: {data['name']}")
        if data["inherits"]:
            print(f"    Inherits from: {data['inherits']}")
        print("    Attributes:")
        for attr in data["attribute"]:
            print(f"      - {attr}")

def print_associations(associations):
    print("\nAssociations (Relationships):")
    for assoc_name, from_class, mult1, to_class, mult2 in associations:
        print(f"  - {from_class} ({mult1}) ---[{assoc_name}]--- ({mult2}) {to_class}")