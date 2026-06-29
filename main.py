import os
import subprocess
import sys
import time
import logging

# Dynamically set JAVA_HOME for PySpark using Mac Homebrew's OpenJDK 17
try:
    java_home_path = subprocess.check_output(['brew', '--prefix', 'openjdk@17'], text=True).strip()
    os.environ["JAVA_HOME"] = f"{java_home_path}/libexec/openjdk.jdk/Contents/Home"
except Exception:
    pass # Let Spark fallback to default if brew is not available

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def run_script(script_name):
    logger.info(f"Starting step: {script_name}")
    start_time = time.time()
    
    try:
        subprocess.run(
            [sys.executable, f"scripts/{script_name}"],
            check=True,
            text=True
        )
        elapsed_time = time.time() - start_time
        logger.info(f"Successfully completed {script_name} in {elapsed_time:.2f}s")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing {script_name}. Pipeline failed.")
        sys.exit(1)

def main():
    logger.info("Initializing IMDb Lakehouse to OLAP Pipeline")
    
    pipeline_steps = [
        "download_data.py",
        "etl_job.py",
        "load_to_olap.py",
        "analytics.py"
    ]
    
    for step in pipeline_steps:
        run_script(step)
        
    logger.info("Pipeline execution completed successfully")

if __name__ == "__main__":
    main()
