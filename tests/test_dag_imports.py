from pathlib import Path

from airflow.models import DagBag


def test_smoke_dag_loads():
    dags_folder = Path(__file__).resolve().parents[1] / "dags"
    dag_bag = DagBag(
        dag_folder=str(dags_folder),
        include_examples=False,
    )

    assert not dag_bag.import_errors, dag_bag.import_errors

    dag = dag_bag.get_dag("environment_smoke_test")
    assert dag is not None
    assert dag.schedule is None
    assert dag.catchup is False
    assert set(dag.task_ids) == {"check_warehouse"}