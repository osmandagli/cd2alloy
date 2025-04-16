from math import isinf
import helpers
from src import write_to_file, write_alloy_base


def generate_alloy_translation(uml_classes):
    """Translates UML class structures into Alloy code."""
    
    write_alloy_base(classes=uml_classes)

    # Rule U1: Define Classes as Signatures
    write_to_file(
        "\n".join(
            [
                f"sig {uml_class.name} extends Obj {{}}"
                for uml_class in uml_classes.values()
                if uml_class.classType != "enum"
            ]
        )
    )

    # Rule U2 & Rule U3: Define Attributes & Associations
    attribute_signatures = []
    for uml_class in uml_classes.values():
        if uml_class.classType == "class":
            # Define Attributes as Signatures
            attribute_signatures.extend(
                [
                    f"private one sig {attr[0]} extends FName {{}}"
                    for attr in uml_class.attributes
                ]
            )
            # Define Associations as Signatures
            attribute_signatures.extend(
                [
                    f"private one sig {assoc.name} extends FName {{}}"
                    for assoc in uml_class.associations
                ]
            )
            # Define Data Types for Attributes
            attribute_signatures.extend(
                [
                    f"private one sig type_{attr[1]} extends Val {{}}"
                    for attr in uml_class.attributes
                    if attr[1] not in helpers.all_class_names(uml_classes)
                ]
            )

    write_to_file("\n".join(attribute_signatures))

    # Rule U4: Define Enum Values
    write_to_file(
        "\n".join(
            [
                f"private one sig enum_{uml_class.name}_{enum_value[0]} extends EnumVal {{}}"
                for uml_class in uml_classes.values()
                if uml_class.classType == "enum"
                for enum_value in uml_class.attributes
            ]
        )
    )

    # Rule F1: Define Class Subtypes
    for uml_class in uml_classes.values():
        if uml_class.classType == "enum":
            continue
        if uml_class.children:
            write_to_file(
                f"fun {uml_class.name}SubsCD: set Obj {{ {uml_class.name} + "
                + " + ".join(
                    [f" {uml_classes.get(child).name}" for child in uml_class.children]
                )
                + f" }}"
            )
        else:
            write_to_file(f"fun {uml_class.name}SubsCD: set Obj {{ {uml_class.name} }}")

    write_to_file("\n")

    for uml_class in uml_classes.values():
        if uml_class.classType == "enum":
            enumAttrs = [
                f"enum_{uml_class.name}_{attr[0]}" for attr in uml_class.attributes
            ]

            write_to_file(
                f"fun {uml_class.name}EnumCD: set EnumVal {{\n\t{"+\n\t".join(enumAttrs)} \n}}"
            )

    write_to_file("\n")

    # Rule F4: Define Composite Relationships
    write_to_file(
        "\n".join(
            [
                f"fun {association.to_class}CompFieldsCD:Obj->Obj {{\n   rel[{association.from_class}SubsCD, {association.name}]\n}}"
                for uml_class in uml_classes.values()
                for association in uml_class.associations
                if association.association_type == "composite"
            ]
        )
    )
    
    # Define the facts of empty classes
    
    write_to_file("fact {\n")
    for class_name in helpers.all_empty_classes(uml_classes):
        write_to_file(f"no {class_name}.get[FName]")
    write_to_file("}\n")
    
    write_to_file("pred cd {")

    # Rule P1: Define Object Attributes
    write_to_file(
        "\n".join(
            [
                f"ObjAttrib[{uml_class.name}, {attribute[0]}, "
                + (
                    f"{attribute[1]}EnumCD"
                    if attribute[1] in helpers.all_enum_classes(uml_classes)
                    else f"{attribute[1]}SubsCD"
                    if attribute[1] in helpers.all_classes_except_enums(uml_classes)
                    else f"type_{attribute[1]}"
                )
                + "]"
                for uml_class in uml_classes.values()
                if uml_class.classType == "class"
                for attribute in helpers.get_inherited_attributes(
                    uml_class, uml_classes
                )  # Use inherited attributes
            ]
        )
    )

    write_to_file("\n")

    # Rule P2: Define Object Field Names (Attributes + Associations)
    for uml_class in uml_classes.values():
        attribute_and_association_names = [attr[0] for attr in uml_class.attributes] + [
            assoc.name for assoc in uml_class.associations
        ]

        if uml_class.inheritance:
            parent_class = uml_classes.get(uml_class.inheritance)
            if parent_class:
                attribute_and_association_names.extend(
                    [attr[0] for attr in parent_class.attributes]
                )
                attribute_and_association_names.extend(
                    [assoc.name for assoc in parent_class.associations]
                )
            else:
                write_to_file(
                    f"Warning: Parent class '{uml_class.inheritance}' not found in class dictionary."
                )

        if attribute_and_association_names and uml_class.classType == "class":
            write_to_file(
                f"ObjFNames[{uml_class.name}, {' + '.join(attribute_and_association_names)}]"
            )

    write_to_file("\n")

    # Rule P4: Define Object Set
    write_to_file(
        f"Obj = {' + '.join([uml_class.name for uml_class in uml_classes.values() if uml_class.classType == 'class'])}"
    )

    write_to_file("\n")

    # Rule A2: Define Composite Relationships
    write_to_file(
        "\n".join(
            [
                f"Composition[{association.to_class}CompFieldsCD, {association.to_class}SubsCD]"
                for uml_class in uml_classes.values()
                for association in uml_class.associations
                if association.association_type == "composite"
            ]
        )
    )

    write_to_file("\n")

    # Rule A5 & A6: Define Multiplicity Constraints
    multiplicity_constraints = [
        (
            f"ObjLUAttrib[{association.from_class}SubsCD, {association.name}, {association.to_class}SubsCD, {association.to_lower_mult}, {association.to_upper_mult}]"
            if not isinf(association.to_upper_mult)
            else f"ObjLAttrib[{association.from_class}SubsCD, {association.name}, {association.to_class}SubsCD, {association.to_lower_mult}]"
        )
        for uml_class in uml_classes.values()
        for association in uml_class.associations
    ]

    multiplicity_constraints += [
        (
            f"ObjLU[{association.to_class}SubsCD, {association.name}, {association.from_class}SubsCD, {association.from_lower_mult}, {association.from_upper_mult}]"
            if not isinf(association.from_upper_mult)
            else f"ObjL[{association.to_class}SubsCD, {association.name}, {association.from_class}SubsCD, {association.from_lower_mult}]"
        )
        for uml_class in uml_classes.values()
        for association in uml_class.associations
    ]

    write_to_file("\n".join(multiplicity_constraints))

    write_to_file("}")

    write_to_file("run cd for 10")
