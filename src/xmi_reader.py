import xml.etree.ElementTree as ET
from src.models import UMLClass
from src.models import AssociationClass
import re
from math import inf

def match_regex(input : str, regex_dict : dict[str, str]):
    for pattern, value in regex_dict.items():
        if re.search(pattern, input):
            return value
    return "No match found"

def lower_upper_bound(type : str, mult : str) -> tuple[int, int]:
    
    if(mult == "*"):
        lower_bound = 0
        upper_bound = inf
        
    elif(type == "one"):
        lower_bound = 1
        upper_bound = 1
    
    elif(type == "lone"):
        lower_bound = 0
        upper_bound = 1
    
    elif(type == "set" or type == "lower_set"):
        lower_bound = int(mult.split("..")[0])
        upper_bound = inf
    
    elif(type == "lower_upper_set"):
        lower_bound, upper_bound = map(int, mult.split(".."))
    
    return lower_bound, upper_bound

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

        if uml_class.findall(
            ".//UML:Classifier.feature/UML:Attribute", namespace
        ):
        # Extract attributes
            for attr in uml_class.findall(
            ".//UML:Classifier.feature/UML:Attribute", namespace
        ):
                attr_with_type = attr.get("name", "UnnamedAttribute")
                if ":" in attr_with_type:
                    if classes[class_id].get_class_type() is None:
                        classes[class_id].classType = "class"
                    attr_name, attr_type = map(str.strip, attr_with_type.split(":", 1))
                else:
                    if classes[class_id].get_class_type() is None:
                        classes[class_id].classType = "enum"
                    attr_name, attr_type = attr_with_type, "enum"

                if attr_type == "int":
                    attr_type = "Int"
                elif attr_type == "string":
                    attr_type = "String"

                classes[class_id].add_attribute(attr_name, attr_type)
        else:
            classes[class_id].classType = "class"
        
    # Extract inheritance relationships
    for generalization in root.findall(".//UML:Generalization", namespace):
        child_id = generalization.find(
            ".//UML:Generalization.child/UML:Class", namespace
        ).get("xmi.idref")
        parent_id = generalization.find(
            ".//UML:Generalization.parent/UML:Class", namespace
        ).get("xmi.idref")

        if child_id in classes and parent_id in classes:
            classes[child_id].set_inheritance(parent_id)
            classes[parent_id].add_child(child_id)

    # Extract associations and store them as AssociationClass instances
    for assoc in root.findall(".//UML:Association", namespace):
        assoc_name = assoc.get("name", "UnnamedAssociation")
        ends = assoc.findall(
            ".//UML:Association.connection/UML:AssociationEnd", namespace
        )
        
        multipicty = {
            r"^1$" : "one",
            r"^0..1$" : "lone",
            r"^\d+\.\.\d+$" : "lower_upper_set",
            r"^\d+\.\.\*$" : "lower_set",
            r"^\*$" : "set"
        }

        if len(ends) == 2:
            assoc_type = (
                ends[0].get("aggregation") or ends[1].get("aggregation") or "default"
            )
            end1_type = ends[0].get("type", "Unknown")
            end2_type = ends[1].get("type", "Unknown")

            from_class = classes.get(end1_type, None)
            to_class = classes.get(end2_type, None)

            end1_mult = ends[0].get("name")  # Default to "*" if missing
            end2_mult = ends[1].get("name")  # Default to "*" if missing
            
            if(end1_mult is None or end2_mult is None):
                print(f"Please give numbers to all sides of associations")
                exit(1)
            
            regex_match = match_regex(end1_mult, multipicty)
            if regex_match is None:
                print(f"Please enter something correct")
                exit(1)
            
            from_lower_mult, from_upper_mult = lower_upper_bound(regex_match, end1_mult)
            
            to_lower_mult, to_upper_mult = lower_upper_bound(match_regex(end2_mult, multipicty), end2_mult)
                                                             
            association = AssociationClass(
                assoc_name,
                assoc_type,
                from_class.name,
                from_lower_mult,
                from_upper_mult,
                to_class.name,
                to_lower_mult,
                to_upper_mult,
            )
            from_class.associations.append(association)
            
    return classes
