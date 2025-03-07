import xmi_reader
#import printer
from translater import translater

classes, associations, _ = xmi_reader.read_xmi("plantuml_to_argouml.xmi")

#printer.print_classes(classes)
#printer.print_ocl_constraints(constraints)
#printer.print_associations(associations)

translater(classes, associations)