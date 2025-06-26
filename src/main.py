from xmi_reader import read_xmi
from translater import generate_alloy_translation

def main():
    classes = read_xmi("./data/cd.xmi")
    if not classes:
        print("No classes found in the XMI file.")
        return
    generate_alloy_translation(classes)


if __name__ == "__main__":
    main()
