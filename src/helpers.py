from src.models.UMLClass import UMLClass

def all_class_names(classes) -> list:
    classNames = []
    for umlClass in classes.values():
        classNames.append(umlClass.name)
    return classNames

def get_inherited_attributes(uml_class, uml_classes):
    """ Recursively collect attributes from parent classes. """
    inherited_attributes = set(uml_class.attributes)  # Start with the class's own attributes

    if uml_class.inheritance and uml_class.inheritance in uml_classes:
        parent_class = uml_classes[uml_class.inheritance]
        inherited_attributes.update(get_inherited_attributes(parent_class, uml_classes))  # Recursive call

    return inherited_attributes

def all_enum_classes(classes) -> list:
    enumClasses = []
    for umlClass in classes.values():
        if umlClass.classType == "enum":
            enumClasses.append(umlClass.name)
    return enumClasses

def all_classes_except_enums(classes) -> list:
    straightClasses = []
    for umlClass in classes.values():
        if umlClass.classType == "enum":
            continue
        straightClasses.append(umlClass.name)
    
    return straightClasses

def all_empty_classes(classes : list[UMLClass]) -> list:
    emptyClasses = []
    for umlClass in classes.values():
        if umlClass.classType == "enum":
            continue
        if umlClass.inheritance:
            parent = classes[umlClass.inheritance]
            if not parent.associations:
                emptyClasses.append(umlClass.name)    
                continue 
            else:
                continue
        if not umlClass.associations and not umlClass.attributes:
            emptyClasses.append(umlClass.name)
    
    return emptyClasses

def isConsistEnum(classes) -> bool:
    
    for umlClass in classes.values():
        if umlClass.classType == "enum":
            return True
    return False

def isCustomTypeExists(classes) -> bool:
    
    allClasses = all_class_names(classes=classes)
    
    for umlClass in classes.values():
        if umlClass.classType == "enum":
            continue
        for attribute in umlClass.attributes:
            if attribute[1] not in allClasses:
                return True
    
    return False