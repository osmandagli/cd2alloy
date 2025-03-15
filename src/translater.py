from math import isinf

def translater(classes):
    # Rule U1
    for umlClass in classes.values():
        print(f"sig {umlClass.name} extends Obj {{}}")

    # Rule U2
    for umlClass in classes.values():
        for attribute in umlClass.attributes:
            print(f"one sig {attribute[0]} extends FName {{}}")
        for association in umlClass.associations:
            print(f"one sig {association.name} extends FName {{}}")

    # Rule U3
    for umlClass in classes.values():
        for attribute in umlClass.attributes:
            print(f"one sig type_{attribute[1]} extends Val {{}}")

    # Rule F1
    for umlClass in classes.values():
        print(f"fun {umlClass.name}SubsCD: set Obj {{ {umlClass.name}", end="")
        if umlClass.children:
            for child in umlClass.children:
                print(f" + {classes.get(child).name}", end="")
        print(" }")

    # Rule F4
    for umlClass in classes.values():
        for association in umlClass.associations:
            if association.association_type == "composite":
                print(
                    f"fun {association.to_class}CompFieldsCD:Obj->Obj {{\n   rel[{association.from_class}SubsCD, {association.name}]\n}}"
                )

    print("run {")
    # Rule P1
    for umlClass in classes.values():
        for attribute in umlClass.attributes:
            print(f"ObjAttrib[{umlClass.name}, {attribute[0]}, type_{attribute[1]}]")
        if umlClass.inheritance:
            parent_id = umlClass.inheritance
            parent = classes.get(parent_id)
            if parent:
                for attribute in parent.attributes:
                    print(
                        f"ObjAttrib[{umlClass.name}, {attribute[0]}, type_{attribute[1]}]"
                    )
            else:
                print(
                    f"Warning: Parent class '{parent_id}' not found in classes dictionary."
                )

    # Rule P2
    for umlClass in classes.values():
        attributes_and_associations = []

        # Add class attributes
        for attribute in umlClass.attributes:
            attributes_and_associations.append(attribute[0])

        # Add class associations
        for association in umlClass.associations:
            attributes_and_associations.append(association.name)

        # Add parent class attributes
        if umlClass.inheritance:
            parent_id = umlClass.inheritance
            parent = classes.get(parent_id)
            if parent:
                for attribute in parent.attributes:
                    attributes_and_associations.append(attribute[0])
                for association in parent.associations:
                    attributes_and_associations.append(association.name)
            else:
                print(
                    f"Warning: Parent class '{parent_id}' not found in classes dictionary."
                )

        if attributes_and_associations:
            # Join all attributes with '+'
            attributes_and_associations_str = " + ".join(attributes_and_associations)

            print(f"ObjFNames[{umlClass.name}, {attributes_and_associations_str}]")

    # Rule P3 now no abstract class is used so passed

    # Rule P4
    print(f"Obj = ", end="")
    class_names = []
    for umlClass in classes.values():
        class_names.append(umlClass.name)

    print(" + ".join(class_names))

    # Rule A1 now no bidirectional association is used so passed

    # Rule A2

    for umlClass in classes.values():
        for association in umlClass.associations:
            if association.association_type == "composite":
                print(
                    f"Composition[{association.to_class}CompFieldsCD, {association.to_class}SubsCD]"
                )

    # Rule A3 and A4 not implemented due to not having right to left association

    # Rule A5

    for umlClass in classes.values():
        for association in umlClass.associations:
            if(not isinf(association.to_upper_mult)):
                print(f"ObjLUAttrib[{association.from_class}SubsCD, {association.name}, {association.to_class}SubsCD, {association.to_lower_mult}, {association.to_upper_mult}]")
            else:
                print(f"ObjLAttrib[{association.from_class}SubsCD, {association.name}, {association.to_class}SubsCD, {association.to_lower_mult}]")
    
    # Rule A6
         
    for umlClass in classes.values():
        for association in umlClass.associations:
            if(not isinf(association.from_upper_mult)):
                print(f"ObjLU[{association.to_class}SubsCD, {association.name}, {association.from_class}SubsCD, {association.from_lower_mult}, {association.from_upper_mult}]")
            else:
                print(f"ObjL[{association.to_class}SubsCD, {association.name}, {association.from_class}SubsCD, {association.from_lower_mult}]")

    print("}")
