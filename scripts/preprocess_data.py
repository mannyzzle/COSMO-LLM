# scripts/preprocess_data.py
import os
import json
import boto3
from transformers import AutoTokenizer

def download_data_from_s3(bucket_name, s3_prefix, local_dir="data"):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    os.makedirs(local_dir, exist_ok=True)
    for obj in bucket.objects.filter(Prefix=s3_prefix):
        if obj.key.endswith("/"):
            continue
        target = os.path.join(local_dir, os.path.basename(obj.key))
        print(f"Downloading {obj.key} to {target}")
        bucket.download_file(obj.key, target)

def preprocess_file(filepath, tokenizer):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    tokens = tokenizer(text, truncation=True, max_length=512)
    return tokens

def save_preprocessed_data(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Preprocessed data saved to {output_path}")

def main():
    # Configuration: update these values as needed
    s3_bucket = "my-cosmo-train-bucket"  # Replace with your S3 bucket name
    s3_prefix = "data/"
    local_data_dir = "data"
    output_dir = "preprocessed"
    os.makedirs(output_dir, exist_ok=True)
    
    # Download raw data from S3
    download_data_from_s3(s3_bucket, s3_prefix, local_dir=local_data_dir)
    
    # Load tokenizer (using MPT-30B tokenizer as example)
    tokenizer = AutoTokenizer.from_pretrained("mosaicml/mpt-30b")
    
    # Process each file in local_data_dir
    for filename in os.listdir(local_data_dir):
        filepath = os.path.join(local_data_dir, filename)
        print(f"Processing file: {filepath}")
        tokens = preprocess_file(filepath, tokenizer)
        output_path = os.path.join(output_dir, f"{filename}.json")
        save_preprocessed_data(tokens, output_path)
    
    print("Preprocessing complete.")

if __name__ == "__main__":
    main()
