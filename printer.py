def print_ocl_constraints(constraints):
    print("\nOCL Constraints:")
    for constraint in constraints:
        print(f"  - Constraint: {constraint['name']} (ID: {constraint['id']})")
        print(f"    Expression: {constraint['expression']}")
        print(f"    Applies to: {constraint['applies_to']}")

def print_classes(classes):
    print("\nUML Classes and Attributes:")
    for _, data in classes.items():
        print(f"  - Class: {data['name']}")
        if data["inherits"]:
            print(f"    Inherits from: {data['inherits']}")
        print("    Attributes:")
        for attr in data["attribute"]:
            print(f"      - {attr}")