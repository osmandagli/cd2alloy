import xml.etree.ElementTree as ET
from umlclass import UMLClass

def read_xmi(xmi_file):
    tree = ET.parse(xmi_file)
    root = tree.getroot()
        
    namespace = {
        'UML': 'href://org.omg/UML/1.3' 
    }
    
    classes = {}   # Dictionary to off umlclass objects
    
    # Find all classes
    for uml_class in root.findall('.//UML:Class', namespace):
        class_id = uml_class.get('xmi.id')
        class_name = uml_class.get('name', None)
        if class_name is None:
            continue
        
        classes[class_id] = UMLClass(class_id, class_name)

        # Extract attributes
        for attr in uml_class.findall('.//UML:Classifier.feature/UML:Attribute', namespace):
            attrWithType = attr.get('name', 'UnnamedAttribute')
            attr_name, attr_type = attrWithType.split(":")
            classes[class_id].add_attribute(attr_name.strip(), attr_type.strip())
            
    # Extract the inheritance
    for generalization in root.findall('.//UML:Generalization', namespace):
        child_id = generalization.find('.//UML:Generalization.child/UML:Class', namespace).get('xmi.idref')
        parent_id = generalization.find('.//UML:Generalization.parent/UML:Class', namespace).get('xmi.idref')

        if child_id in classes and parent_id in classes:
            classes[child_id].set_inheritance(classes[parent_id].name)

    for assoc in root.findall('.//UML:Association', namespace):
        assoc_name = assoc.get('name', 'UnnamedAssociation')
        ends = assoc.findall('.//UML:Association.connection/UML:AssociationEnd', namespace)

        if len(ends) == 2:
            end1_type = ends[0].get('type', 'Unknown')
            end2_type = ends[1].get('type', 'Unknown')
            end1_mult = ends[0].get('name', 'Unknown')
            end2_mult = ends[1].get('name', 'Unknown')

            from_class = classes.get(end1_type, None)
            to_class = classes.get(end2_type, None)
            
            if from_class:
                from_class.add_association(assoc_name, from_class.name, end1_mult, to_class.name if to_class else f"Unknown({end2_type})", end2_mult)
    
    # TODO: Extract constraints
    
    return classes, None