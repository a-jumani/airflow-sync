# Sync Airflow DAGs and Plugins
An airflow dag to synchronize dags and plugins across instances / containers in your fleet.

### Usage:
Follows these steps:

1. Create two access points with separate folders on an NFS.

2. Mount these access points within your _webserver_, _worker_ and _scheduler_ instances / containers to:
    - `$AIRFLOW_HOME/dags/<some_folder>` for dags. Create a `Variable` named `DAGS_ABSOLUTE_PATH` set to this path before executing `update-dags` dag.
    Note: do **NOT** use `$AIRFLOW_HOME/dags` instead as we do not want to reset `sync-dags-plugins.py` as `update-dags` executes.
    - `$AIRFLOW_HOME/plugins` or `$AIRFLOW_HOME/plugins/<some_folder>` for plugins. Create a `Variable` named `PLUGINS_ABSOLUTE_PATH` set to this path before executing `update-plugins`.

3. Create `Variable`'s named `DAGS_GITHUB_REPO` and `PLUGINS_GITHUB_REPO` and store paths to respective repositories in them, e.g. `github.com/example-repo.git`.

4. Whenever your trigger `update-dags` or `update-plugins` dag, provide your GitHub credentials in the configuration using syntax `{"git_user": "<username>", "git_password": "<password/access_token>"}`.
Note: using `Variables` instead of this method will also expose the credentials in web UI. The best method, according to my knowledge, is for read-only access credentials to be injected into the instance / container and using a (bash) script.

### Tips:
1. Import operators using syntax `operator.my_operator` (as explained [here](https://www.astronomer.io/guides/airflow-importing-custom-hooks-operators/)) to avoid having to restart _webserver_ and _scheduler_ for updated/new operators to take effect.
