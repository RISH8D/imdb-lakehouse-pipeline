import subprocess
import sys
import time

def run_script(script_name):
    print(f"\n{'='*50}")
    print(f"🚀 Starting Step: {script_name}")
    print(f"{'='*50}")
    
    start_time = time.time()
    
    try:
        # Run the script and stream the output to the console
        result = subprocess.run(
            [sys.executable, f"scripts/{script_name}"],
            check=True,
            text=True
        )
        
        elapsed_time = time.time() - start_time
        print(f"\n✅ Successfully completed {script_name} in {elapsed_time:.2f} seconds.")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error executing {script_name}. Pipeline failed!")
        sys.exit(1)

def main():
    print("🎬 Initializing IMDb Lakehouse to OLAP Pipeline...")
    
    pipeline_steps = [
        "download_data.py",   # Step 1: Ingest from Kaggle
        "etl_job.py",         # Step 2: Clean and partition in PySpark (Lake)
        "load_to_olap.py",    # Step 3: Load Parquet into ClickHouse (OLAP)
        "analytics.py"        # Step 4: Run benchmark queries
    ]
    
    for step in pipeline_steps:
        run_script(step)
        
    print("\n🎉 Pipeline Execution Completed Successfully!")

if __name__ == "__main__":
    main()
