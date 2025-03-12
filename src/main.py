from src import read_xmi, translater


classes = read_xmi("./data/association.xmi")

# printer.print_classes(classes)
# printer.print_ocl_constraints(constraints)
# print_associations(classes)

translater(classes)
