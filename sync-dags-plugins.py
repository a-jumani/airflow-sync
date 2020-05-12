import subprocess


def run_command(cmd):
    """ Execute a shell command.

    Args:
        cmd command to run
    Exceptions:
        Exception if execution was not successful
    """
    # execute command
    result = subprocess.run(
        [cmd],
        capture_output=True,
        shell=True,
    )

    # check error
    if result.returncode != 0:
        raise Exception(f"Error in execution: {result.stderr.decode()}")
