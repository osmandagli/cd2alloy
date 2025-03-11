import xmi_reader
#from printer import print_associations
from translater import translater


classes, _= xmi_reader.read_xmi("association.xmi")

#printer.print_classes(classes)
#printer.print_ocl_constraints(constraints)
#print_associations(classes)

translater(classes)
