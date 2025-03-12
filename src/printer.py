def print_associations(classes):
    print("\nAssociations (Relationships):")
    for umlclass in classes.values():
        umlclass.print_associations()