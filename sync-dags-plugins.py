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


def update_repo(absolute_path, git_user, git_pswd, path_to_repo):
    """ Update a repo by removing contents of absolute_path and
    cloning https://github.com/path_to_repo into it. That is,
    merge conflicts are avoided since git pull isn't used.

    Args:
        absolute_path   absolute path to folder containing the repository files
        git_user        git username for access to private repo
        git_pswd        git password for access to private repo
        path_to_repo    path relative to https://github.com/
    Preconditions:
        name of hidden files directly under absolute_path have prefix .git*
    Exceptions:
        Exception if absolute_path doesn't begin with '/'
    """
    # detect or fix formatting issues in absolute_path
    if absolute_path[0] != '/':
        raise Exception("Arg format error: absolute_path must begin with /")
    if absolute_path[-1] != '/':
        absolute_path += '/'

    # clean up non-hidden files and all directories at absolute_path
    run_command(f"rm -rf {absolute_path}*")

    # clean up hidden git files
    run_command(f"rm -rf {absolute_path}.git*")

    # clone repo_name at absolute_path
    run_command(f"git clone https://{git_user}:{git_pswd}@github.com/{path_to_repo} {absolute_path}")

    print(f"Successfully updated {path_to_repo} at {absolute_path}")
