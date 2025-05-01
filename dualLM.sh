#!/bin/bash


conda activate dl_step1

# Set up environment variables
export OPENAI_API_KEY="your-openai-api-key-here"


# Example commits (these are example commit hashes, replace with real ones)
COMMITS="ff2047fb755d d1e7fd6462ca f4020438fab0 2c1f6951a8a8 79dc7e3f1cd3"
#COMMITS="9d7a0577c9db35c4cc52db90bc415ea248446472"
#COMMITS="79dc7e3f1cd3"
# Set up paths
DATASET_NAME="test_dataset"
REPO_DIR="./repos/linux"           # Path to Linux kernel repository
DATA_DIR="./data"                  # Path to store data
SUMMARY_FILE="./data/summary.txt"  # Path for summary output

# Create necessary directories
mkdir -p ./data/results

# Run the main script
python3 ./codes/step1.py \
    --commits $COMMITS \
    --name "$DATA_SET_NAME" \
    --repo-dir "$REPO_DIR" \
    --summary-file "$SUMMARY_FILE" \
    --out-file1 "./data/results/step1.txt" \
    --out-file2 "./data/results/step2.txt" \
    --data-dir "./data/"

conda deactivate

conda activate dl_step2

cd codes
./eval_given_step1.sh 0
./eval_given_step2.sh 0

conda deactivate

conda activate dl_step1

cd ../

python3 ./codes/final.py \
    --step1-out-file "./data/results/step1_res.txt" \
    --step2-out-file "./data/results/step2_res.txt" \
    --not-reliable "./data/results/not_reliable.txt"





