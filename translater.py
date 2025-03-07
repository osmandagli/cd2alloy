def class_to_sig(umlClass):
    
    builtInTypes = ["String", "Integer"]
    
    createAttrs(umlClass)
    
    if umlClass['inherits'] is not None:
        print(f"sig {umlClass['name']} extends {umlClass['inherits']} {{")
    else:
        print(f"sig {umlClass['name']}: {{")
        
    for attr, attr_type in zip(umlClass["attribute"], umlClass["attribute_type"]):
        print(f"  {attr}: one {attr_type}")
        
    print("}")
    
def createAttrs(umlClass) -> None:
    builtInTypes = ["String", "Integer", "Float"]
    for attr_type in umlClass["attribute_type"]:
        if attr_type not in builtInTypes:
            print(f"sig {attr_type} {{}}")