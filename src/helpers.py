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