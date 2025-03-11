import xml.etree.ElementTree as ET
from umlclass import UMLClass
from associationclass import AssociationClass


def read_xmi(xmi_file):
    tree = ET.parse(xmi_file)
    root = tree.getroot()

    namespace = {"UML": "href://org.omg/UML/1.3"}

    classes = {}  # Dictionary to hold UMLClass objects

    # Find all UML classes
    for uml_class in root.findall(".//UML:Class", namespace):
        class_id = uml_class.get("xmi.id")
        class_name = uml_class.get("name", None)
        if class_name is None:
            continue

        classes[class_id] = UMLClass(class_id, class_name)

        # Extract attributes
        for attr in uml_class.findall(
            ".//UML:Classifier.feature/UML:Attribute", namespace
        ):
            attr_with_type = attr.get("name", "UnnamedAttribute")
            if ":" in attr_with_type:
                attr_name, attr_type = map(str.strip, attr_with_type.split(":", 1))
            else:
                attr_name, attr_type = attr_with_type.strip(), "Unknown"

            classes[class_id].add_attribute(attr_name, attr_type)

    # Extract inheritance relationships
    for generalization in root.findall(".//UML:Generalization", namespace):
        child_id = generalization.find(
            ".//UML:Generalization.child/UML:Class", namespace
        ).get("xmi.idref")
        parent_id = generalization.find(
            ".//UML:Generalization.parent/UML:Class", namespace
        ).get("xmi.idref")

        if child_id in classes and parent_id in classes:
            classes[child_id].set_inheritance(classes[parent_id].name)

    # Extract associations and store them as AssociationClass instances
    for assoc in root.findall(".//UML:Association", namespace):
        assoc_name = assoc.get("name", "UnnamedAssociation")
        ends = assoc.findall(
            ".//UML:Association.connection/UML:AssociationEnd", namespace
        )

        if len(ends) == 2:
            end1_type = ends[0].get("type", "Unknown")
            end2_type = ends[1].get("type", "Unknown")
            end1_mult = ends[0].get("name", "*")  # Default to "*" if missing
            end2_mult = ends[1].get("name", "*")  # Default to "*" if missing

            from_class = classes.get(end1_type, None)
            to_class = classes.get(end2_type, None)

            if from_class and to_class:
                association = AssociationClass(
                    assoc_name, from_class.name, end1_mult, to_class.name, end2_mult
                )
                from_class.associations.append(association)
            
    
    return classes
