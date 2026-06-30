import os
import zipfile
import subprocess

def download_imdb_data():
    raw_dir = "./data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    
    # Temporarily set the Kaggle config directory to our project root 
    # so it finds the kaggle.json file we placed there
    os.environ['KAGGLE_CONFIG_DIR'] = os.path.abspath(".")

    print("Authenticating and downloading IMDb dataset via Kaggle API...")
    
    # We use subprocess to call the Kaggle CLI
    # The dataset format is: kaggle datasets download -d <owner>/<dataset-name>
    command = [
        "kaggle", "datasets", "download", 
        "-d", "ashirwadsangwan/imdb-dataset",
        "-p", raw_dir
    ]
    
    try:
        # Remove existing zip if it exists to avoid 416 resume errors
        zip_path = os.path.join(raw_dir, "imdb-dataset.zip")
        if os.path.exists(zip_path):
            os.remove(zip_path)

        subprocess.run(command, check=True)
        print("Download complete. Unzipping files...")
        
        # Unzip the downloaded file
        zip_path = os.path.join(raw_dir, "imdb-dataset.zip")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # We only extract the two files we actually need to save space
            files_to_extract = ['title.basics.tsv', 'title.ratings.tsv']
            for file in zip_ref.namelist():
                if file in files_to_extract:
                    zip_ref.extract(file, raw_dir)
                    print(f"Extracted: {file}")
                    
        # Cleanup the zip file and empty directories
        os.remove(zip_path)
        for folder in ['title.basics.tsv', 'title.ratings.tsv']:
            folder_path = os.path.join(raw_dir, folder)
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                os.rmdir(folder_path)
                
        print("Ingestion complete. Data is ready in ./data/raw/")
        
    except subprocess.CalledProcessError as e:
        print(f"Error downloading dataset. Ensure kaggle.json is in the root directory. Details: {e}")

if __name__ == "__main__":
    download_imdb_data()
