import helpers

def write_to_file(content, filename="output.als", mode="a"):
    """Writes the given content to a file. Defaults to appending."""
    with open(filename, mode, encoding="utf-8") as file:
        file.write(content + "\n")  # Ensure newline after each write

def copy_alloy_base_to_output(
    base_filename="./data/alloy_bases/full_base.als",
    output_filename="output.als"
):
    """Reads alloy_base.als and writes it to output.als using write_to_file()."""
    try:
        write_to_file("", output_filename, "w")  # Clear the file first
        with open(base_filename, "r", encoding="utf-8") as base_file:
            for line in base_file:  # Read line by line
                write_to_file(line.strip(), output_filename)  # Overwrite at first

    except FileNotFoundError:
        print(f"Error: {base_filename} not found.")

    except Exception as e:
        print(f"Unexpected error: {e}")

def write_alloy_base(classes) -> None:
    
    isEnumNotExists = not helpers.isConsistEnum(classes=classes)
    isCustomValNotExists = not helpers.isCustomTypeExists(classes=classes)
    
    if isEnumNotExists and isCustomValNotExists:
        copy_alloy_base_to_output(base_filename="./data/alloy_bases/no_val_enum_base.als")
    
    elif isEnumNotExists:
        copy_alloy_base_to_output(base_filename="./data/alloy_bases/no_enum_base.als")
        
    elif isCustomValNotExists:
        copy_alloy_base_to_output(base_filename="./data/alloy_bases/no_val_base.als")
    
    else:
        copy_alloy_base_to_output()