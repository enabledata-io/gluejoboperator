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
        script_location=f"s3://enabledata/jobs/test_job.py",
        s3_bucket="enabledata",
        iam_role_name="AWSGlueServiceRoleDefault",
        create_job_kwargs={"GlueVersion": "4.0", "NumberOfWorkers": 2, "WorkerType": "G.1X", "Timeout": 60},
        retry_limit=0,
        script_args={
                '--conf': "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions  \
                            --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog  \
                            --conf spark.sql.catalog.glue_catalog.warehouse=s3://b-data-{env}/warehouse/ \
                            --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog  \
                            --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO",
                '--datalake-formats': 'iceberg',
                '--additional-python-modules': 's3://enabledata/packages/etl-1.0-py3-none-any.whl'
            },
    )

    validate_something = EmptyOperator(task_id="mock_validation")

    submit_glue_job >> validate_something