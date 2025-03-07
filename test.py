import xml.etree.ElementTree as ET

# Load XMI file
tree = ET.parse("plantuml_to_argouml.xmi")  # Update filename if needed
root = tree.getroot()

# Define namespace (not using explicit prefixes in PlantUML XMI)
namespace = {'UML': 'href://org.omg/UML/1.3'}

# Step 1: Extract Classes and Attributes
classes = {}
for uml_class in root.findall('.//UML:Class', namespace):
    class_id = uml_class.get('xmi.id')
    class_name = uml_class.get('name', 'UnnamedClass')
    classes[class_id] = {"name": class_name, "attributes": []}

    # Extract attributes
    for attr in uml_class.findall('.//UML:Classifier.feature/UML:Attribute', namespace):
        attr_name = attr.get('name', 'UnnamedAttribute')
        classes[class_id]["attributes"].append(attr_name)

# Step 2: Extract Generalization (Inheritance)
generalizations = []
for generalization in root.findall('.//UML:Generalization', namespace):
    child_id = generalization.find('.//UML:Generalization.child/UML:Class', namespace).get('xmi.idref')
    parent_id = generalization.find('.//UML:Generalization.parent/UML:Class', namespace).get('xmi.idref')
    
    if child_id in classes and parent_id in classes:
        generalizations.append((classes[child_id]["name"], classes[parent_id]["name"]))

# Step 3: Extract Associations
associations = []
for assoc in root.findall('.//UML:Association', namespace):
    assoc_name = assoc.get('name', 'UnnamedAssociation')
    ends = assoc.findall('.//UML:Association.connection/UML:AssociationEnd', namespace)

    if len(ends) == 2:
        end1_type = ends[0].get('type', 'Unknown')
        end2_type = ends[1].get('type', 'Unknown')
        end1_mult = ends[0].get('name', 'Unknown')
        end2_mult = ends[1].get('name', 'Unknown')

        class1 = classes.get(end1_type, {}).get("name", f"Unknown({end1_type})")
        class2 = classes.get(end2_type, {}).get("name", f"Unknown({end2_type})")

        associations.append((assoc_name, class1, end1_mult, class2, end2_mult))

# Print Results
print("\nUML Classes and Attributes:")
for class_id, data in classes.items():
    print(f"  - Class: {data['name']}")
    print(f"    Attributes: {', '.join(data['attributes']) if data['attributes'] else 'None'}")

print("\nGeneralizations (Inheritance):")
for child, parent in generalizations:
    print(f"  - {child} inherits from {parent}")

print("\nAssociations (Relationships):")
for assoc_name, class1, mult1, class2, mult2 in associations:
    print(f"  - {class1} ({mult1}) ---[{assoc_name}]--- ({mult2}) {class2}")
