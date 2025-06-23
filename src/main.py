from xmi_reader import read_xmi
from translater import generate_alloy_translation

def main():
    classes = read_xmi("/WORKSPACE/uml2alloy/data/association.xmi")
    
    for class_value in classes.values():
        for association in class_value.associations:
            print(f"type is: {association.association_type}")

        

    generate_alloy_translation(classes)


if __name__ == "__main__":
    main()
