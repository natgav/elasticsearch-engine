import subprocess

#NOTE: the elasticsearch instance must be running using the following command:
# /opt/homebrew/opt/elasticsearch-full/bin/elasticsearch

project_files = [
    #"data_loading.py",
    #"data_preprocessing.py", #Won't run the loading and preprocessing since we already did that and saved it into the csv files
    "es_setup.py",
    "es_indexing.py",
    "es_search.py",
    "clustering.py",
    "semantic_search.py",
    "evaluation.py"
]

def run_project_files(files):
    for file in files:
        print(f"Running {file}...")
        try:
            subprocess.run(["python3", file], check=True)
            print(f"{file} executed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while executing {file}: {e}\n")
            break

if __name__ == "__main__":
    run_project_files(project_files)
