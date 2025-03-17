def malmisin(classes) -> list:
    classNames = []
    for umlClass in classes.values():
        classNames.append(umlClass.name)
    return classNames