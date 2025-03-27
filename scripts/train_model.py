# scripts/train_model.py
import os
import json
import boto3
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset

def load_preprocessed_data(preprocessed_dir="preprocessed"):
    data = []
    for filename in os.listdir(preprocessed_dir):
        if filename.endswith(".json"):
            with open(os.path.join(preprocessed_dir, filename), "r", encoding="utf-8") as f:
                tokens = json.load(f)
                data.append(tokens)
    return data

def create_dataset(data):
    dataset = Dataset.from_dict({"input_ids": [d["input_ids"] for d in data]})
    return dataset

def main():
    model_name = "mosaicml/mpt-30b"
    output_dir = "model_artifacts"
    os.makedirs(output_dir, exist_ok=True)
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    data = load_preprocessed_data(preprocessed_dir="preprocessed")
    dataset = create_dataset(data)
    dataset = dataset.train_test_split(test_size=0.1)
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=1,  # Adjust epochs as needed
        per_device_train_batch_size=1,
        save_steps=100,
        evaluation_strategy="steps",
        eval_steps=50,
        logging_steps=25,
    )
    
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        data_collator=data_collator,
    )
    
    trainer.train()
    trainer.save_model(output_dir)
    
    # Upload model artifacts to S3
    s3_bucket = "my-cosmo-output-bucket"  # Replace with your S3 output bucket name
    s3_prefix = "model_artifacts/"
    s3 = boto3.client("s3")
    for root, _, files in os.walk(output_dir):
        for file in files:
            local_path = os.path.join(root, file)
            s3_path = os.path.join(s3_prefix, os.path.relpath(local_path, output_dir))
            print(f"Uploading {local_path} to s3://{s3_bucket}/{s3_path}")
            s3.upload_file(local_path, s3_bucket, s3_path)
    
    print("Training complete.")

if __name__ == "__main__":
    main()
