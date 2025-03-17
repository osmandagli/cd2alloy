from src import read_xmi, generate_alloy_translation


def main():
    classes = read_xmi("/WORKSPACE/uml2alloy/data/association.xmi")

    generate_alloy_translation(classes)


if __name__ == "__main__":
    main()
