import xml.etree.ElementTree as ET

def read_xmi(xmi_file):
    tree = ET.parse(xmi_file)
    root = tree.getroot()
    
    namespace = {
        'xmi': 'http://www.omg.org/XMI',
        'uml': 'http://www.omg.org/spec/UML/20090901',
        'ocl': 'http://www.omg.org/spec/OCL/20090901'
    }
    
    elements = {}  # Stores {id: name} mapping
    classes = {}   # Stores class details {id: {"name": class_name, "attributes": [], "inherits": None}}

    # Find all classes
    for uml_class in root.findall('.//uml:Class', namespace):
        class_id = uml_class.get('{http://www.omg.org/XMI}id')
        class_name = uml_class.get('name', 'UnnamedClass')
        classes[class_id] = {"name": class_name, "attribute": [], "attribute_type": [], "inherits": None}
        elements[class_id] = class_name  # Store class for lookup

        # Extract attributes
        for attr in uml_class.findall('.//uml:Property', namespace):
            attr_id = attr.get('{http://www.omg.org/XMI}id')
            attr_name = attr.get('name', 'UnnamedAttribute')
            attr_type = attr.get('type', 'UnknownType')
            classes[class_id]["attribute"].append(f"{attr_name}")
            classes[class_id]["attribute_type"].append(f"{attr_type}")
            elements[attr_id] = f"{class_name}.{attr_name}"  # Store attribu   
             
        # Extract inheritance relationships
        for generalization in root.findall('.//uml:Generalization', namespace):
            #child_id = generalization.get('specific')  # Subclass ID
            parent_id = generalization.get('general')  # Superclass ID
            #if child_id in classes and parent_id in classes:
            classes[class_id]["inherits"] = classes[parent_id]["name"]
    
    constraints = []
    for constraint in root.findall('.//uml:Constraint', namespace):
        constraint_id = constraint.get('{http://www.omg.org/XMI}id')
        constraint_name = constraint.get('name', 'UnnamedConstraint')
    
        # Extract OCL Expression
        expression_element = constraint.find('.//ocl:Expression', namespace)
        expression = expression_element.text if expression_element is not None else "No Expression"
    
        # Extract constrained element reference
        constrained_element = constraint.find('.//uml:ConstrainedElement', namespace)
        constrained_id = constrained_element.get('{http://www.omg.org/XMI}idref') if constrained_element is not None else "Unknown"
    
        # Lookup the name using stored ID mappings
        applies_to = elements.get(constrained_id, f"Unknown({constrained_id})")
    
        constraints.append({
            "id": constraint_id,
            "name": constraint_name,
            "expression": expression,
            "applies_to": applies_to
        })

    return classes, constraints