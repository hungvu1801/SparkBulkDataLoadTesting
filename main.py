import sys
import uuid

from pyspark.sql.functions import struct, col, to_json

from lib import ConfigLoader, Utils, DataLoader, Transformation
from lib.logger import Log4j

if __name__ == "__main__":
  if len(sys.argv) <3:
    print("Usage: sbdl {local, qa, prod} {load_date} : Arguments are missing.")
    sys.exit(-1)

  job_run_env = sys.argv[1].upper()
  load_date = sys.argv[2]
  job_run_id = f"SBDL-{uuid.uuid4()}"

  print(f"Initializing SBDL Job in {job_run_env} . Job ID: {job_run_id}")
  conf = ConfigLoader.get_config(job_run_env)
  enable_hive = True if conf["enable.hive"] == "true" else False
  hive_db = conf["hive.database"]

  print("Creating Spark Session...")
  spark = Utils.get_spark_session(job_run_env)