from src import read_xmi, translater


def main():
    classes = read_xmi("/WORKSPACE/uml2alloy/data/association.xmi")

    translater(classes)


if __name__ == "__main__":
    main()
