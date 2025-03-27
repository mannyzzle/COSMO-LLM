# scripts/evaluate_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def main():
    model_path = "model_artifacts"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=128)
    prompt = "Explain the principles of thermodynamics and their applications in material science."
    output = generator(prompt, num_return_sequences=1)
    
    print("Evaluation Output:")
    print(output)

if __name__ == "__main__":
    main()
