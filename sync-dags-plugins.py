import os


def run_command(cmd):
    """ Execute a shell command.

    Args:
        cmd command to run
    Exceptions:
        Exception if execution was not successful
    """
    # execute command
    result = os.system(cmd)

    # check error
    if result != 0:
        raise Exception(f"Error in executing {cmd}")
