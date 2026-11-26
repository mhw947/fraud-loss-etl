from datetime import datetime, timedelta, timezone

from airflow.sdk import dag, task


@dag(
    dag_id="environment_smoke_test",
    description="Verify Airflow task execution and warehouse connectivity.",
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=2),
    tags=["setup"],
)
def environment_smoke_test():
    @task(retries=0, execution_timeout=timedelta(seconds=30))
    def check_warehouse():
        import psycopg2

        from airflow.sdk import BaseHook

        connection = BaseHook.get_connection("warehouse")

        with psycopg2.connect(
            host=connection.host,
            port=connection.port or 5432,
            dbname=connection.schema,
            user=connection.login,
            password=connection.password,
            connect_timeout=10,
        ) as database:
            with database.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()

        if result != (1,):
            raise RuntimeError(f"Unexpected database response: {result!r}")

        print("Warehouse connection verified: SELECT 1 returned 1.")

    check_warehouse()


environment_smoke_test()