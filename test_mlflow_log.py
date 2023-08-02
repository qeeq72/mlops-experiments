import mlflow
import os

MLFLOW_PORT = os.environ['MLFLOW_PORT']

mlflow.set_tracking_uri(f"http://localhost:{MLFLOW_PORT}")

mlflow.end_run()
with mlflow.start_run():
    mlflow.log_artifact(__file__)