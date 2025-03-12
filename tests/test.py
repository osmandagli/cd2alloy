import jpype
import jpype.imports

def run_alloy():
    try:
        jpype.startJVM(classpath=["org.alloytools.alloy.dist.jar"])
    except OSError as e:
        print(e)

    from edu.mit.csail.sdg.parser import CompUtil
    from edu.mit.csail.sdg.alloy4 import A4Reporter
    from edu.mit.csail.sdg.translator import A4Options, TranslateAlloyToKodkod

    # Read the Alloy model from the file
    with open("output.alloy", "r") as file:
        src = file.read()

    rep = A4Reporter()

    # Parse the Alloy model
    world = CompUtil.parseEverything_fromString(rep, src)

    # Get all commands from the parsed model
    commands = world.getAllCommands()
    assert commands.size() > 0  # Ensure there is at least one command to execute
    cmd = commands.get(0)  # Take the first command

    # Set up Alloy solver options
    opt = A4Options()
    opt.solver = A4Options.SatSolver.SAT4J

    # Execute the Alloy command
    solution = TranslateAlloyToKodkod.execute_command(rep, world.getAllSigs(), cmd, opt)

    # Print the result
    print(solution)
