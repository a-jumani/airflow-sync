# Sync Airflow DAGs and Plugins
An airflow dag to synchronize dags and plugins across instances / containers in your fleet.

## Usage:
Follows these steps:
1. Create two access points with separate folders on an NFS.
2. Mount these access points within your _webserver_, _worker_ and _scheduler_ instances / containers to:
    - `$AIRFLOW_HOME/dags/<some_folder>` for dags. Set `DAGS_ABSOLUTE_PATH` to this path within `sync-dags-plugins.py`.
    Note: do **NOT** use `$AIRFLOW_HOME/dags` instead as we do not want to reset this dag, i.e. `sync-dags-plugins.py`, as it executes.
    - `$AIRFLOW_HOME/plugins` or `$AIRFLOW_HOME/plugins/<some_other_folder>` for plugins. Set `PLUGINS_ABSOLUTE_PATH` to this path within `sync-dags-plugins.py`.
3. Whenever your trigger `update-dags` or `update-plugins` dag, provide your GitHub credentials in the configuration using syntax `{"git_user": "<username>", "git_password": "<password/access_token>"}`.
Note: using `Variables` instead of this method will also expose the credentials in web UI. The best method, according to my knowledge, is for read-only access credentials to be injected into the instance / container and using a (bash) script.
