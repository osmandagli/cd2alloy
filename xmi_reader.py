import xml.etree.ElementTree as ET
from umlclass import UMLClass
from associationclass import AssociationClass


def read_xmi(xmi_file) -> dict[str, UMLClass]:
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
                
            if attr_type == "int":
                attr_type = "Int"
            elif attr_type == "string":
                attr_type = "String"

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
            classes[parent_id].add_child(classes[child_id].name)
            print(f"Childs of {classes[parent_id].name}: {classes[parent_id].children}")

    # Extract associations and store them as AssociationClass instances
    for assoc in root.findall(".//UML:Association", namespace):
        assoc_name = assoc.get("name", "UnnamedAssociation")
        ends = assoc.findall(
            ".//UML:Association.connection/UML:AssociationEnd", namespace
        )
        

        if len(ends) == 2:
            assoc_type = (
                ends[0].get("aggregation") or
                ends[1].get("aggregation") or
                "default"
            )
            end1_type = ends[0].get("type", "Unknown")
            end2_type = ends[1].get("type", "Unknown")
            end1_mult = ends[0].get("name", "*")  # Default to "*" if missing
            end2_mult = ends[1].get("name", "*")  # Default to "*" if missing

            from_class = classes.get(end1_type, None)
            to_class = classes.get(end2_type, None)

            # Identify composite (whole-part) association
            left = None  # Whole (composite side)
            right = None  # Part (contained object)

            if assoc_type == "composite":
                if ends[0].get("aggregation") == "composite":
                    left = from_class.name  # Whole
                    right = to_class.name   # Part
                elif ends[1].get("aggregation") == "composite":
                    left = to_class.name  # Whole
                    right = from_class.name  # Part

            
            if from_class and to_class:
                association = AssociationClass(
                    assoc_name, assoc_type, from_class.name, end1_mult, to_class.name, end2_mult, left, right
                )
                from_class.associations.append(association)
                print(f"Association: {association}")

    return classes
