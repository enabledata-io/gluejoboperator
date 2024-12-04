from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="test_dag",
    start_date=datetime(2024, 11, 28),
    schedule="@daily",
    dagrun_timeout=timedelta(minutes=60),
    catchup=False,
    max_active_runs=1,
) as dag:

    submit_glue_job = GlueJobOperator(
        task_id="submit_glue_job",
        job_name="test_job",
        script_location=f"s3://enabledata/scripts/job.py",
        s3_bucket="enabledata",
        iam_role_name="AWSGlueServiceRoleDefault",
        create_job_kwargs={"GlueVersion": "4.0", "NumberOfWorkers": 2, "WorkerType": "G.1X", "Timeout": 60},
        retry_limit=0,
    )

    validate_something = EmptyOperator(task_id="mock_validation")

    submit_glue_job >> validate_something