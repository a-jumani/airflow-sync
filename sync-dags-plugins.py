from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from os.path import isdir
from shutil import rmtree
import logging
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

    # clean up absolute_path
    if isdir(absolute_path):
        rmtree(absolute_path)

    # clone repo_name at absolute_path
    run_command("git clone --recurse-submodules https://{}:{}@{} {}"
                .format(git_user, git_pswd, path_to_repo, absolute_path))

    logging.info(f"Successfully updated {path_to_repo} at {absolute_path}")


default_args = {
    "owner": "a-jumani",
    "start_date": datetime(2020, 5, 12),
    "depends_on_past": False,                   # no past dependence
    "retries": 0,                               # no retries
    "concurrency": 1,                           # dag instances not concurrent
    "catchup": False                            # catchup is off
}


# update dags: clean DAGS_ABSOLUTE_PATH and clone DAGS_GITHUB_REPO into it
with DAG(
    "update-dags",
    default_args=default_args,
    description="Update dags from github. Run this dag in isolation.",
    schedule_interval=None,
) as dag1:

    dummy_task = DummyOperator(
        task_id="dummy_task",
        dag=dag1,
    )

    update_dags = PythonOperator(
        task_id="update_dags",
        dag=dag1,
        python_callable=update_repo,
        op_kwargs={
            "absolute_path": "{{  var.value.DAGS_ABSOLUTE_PATH }}",
            "git_user": "{{ dag_run.conf['git_user'] }}",
            "git_pswd": "{{ dag_run.conf['git_password'] }}",
            "path_to_repo": "{{ var.value.DAGS_GITHUB_REPO }}",
        }
    )

    dummy_task >> update_dags


# update plugins: clean PLUGINS_ABSOLUTE_PATH and clone PLUGINS_GITHUB_REPO
# into it
with DAG(
    "update-plugins",
    default_args=default_args,
    description="Update plugins from github. Run this dag in isolation.",
    schedule_interval=None,
) as dag2:

    dummy_task = DummyOperator(
        task_id="dummy_task",
        dag=dag2,
    )

    update_plugins = PythonOperator(
        task_id="update_plugins",
        dag=dag2,
        python_callable=update_repo,
        op_kwargs={
            "absolute_path": "{{ var.value.PLUGINS_ABSOLUTE_PATH }}",
            "git_user": "{{ dag_run.conf['git_user'] }}",
            "git_pswd": "{{ dag_run.conf['git_password'] }}",
            "path_to_repo": "{{ var.value.PLUGINS_GITHUB_REPO }}",
        }
    )

    dummy_task >> update_plugins
