predefined_types = ["Int", "String"]

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
            if(attribute[1] not in predefined_types):
                print(f"one sig type_{attribute[1]} extends Val {{}}")
                
    # Rule F1
    for umlClass in classes.values():
        print(f"fun {umlClass.name}SubsCD: set Obj {{ {umlClass.name} ", end="")
        if umlClass.children:
            for child in umlClass.children:
                print(f" + {child}", end="")
        print(" }")
        
    # Rule F4
    for umlClass in classes.values():
        for association in umlClass.associations:
            if(association.association_type == "composite"):
                print(f"fun {association.right}CompFieldsCD:Obj->Obj {{\n   rel[{association.left}SubsCD, {association.name}]\n}}")
        