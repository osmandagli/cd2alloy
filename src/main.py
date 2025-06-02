from src.xmi_reader import read_xmi
from src.translater import generate_alloy_translation

def main():
    classes = read_xmi("/WORKSPACE/uml2alloy/data/association.xmi")
    
    for uml_class in classes.values():
        print(uml_class.classType)

    generate_alloy_translation(classes)


if __name__ == "__main__":
    main()
