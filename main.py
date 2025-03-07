import xmi_reader
#import printer
import translater

classes, constraints = xmi_reader.read_xmi("class_diagram_gpt.xmi")

#printer.print_classes(classes)
#printer.print_ocl_constraints(constraints)
for _,umlClass in classes.items():
    translater.class_to_sig(umlClass)