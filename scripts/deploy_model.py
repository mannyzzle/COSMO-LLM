# scripts/deploy_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer

def main():
    model_path = "model_artifacts"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    
    prompt = "List key factors affecting material fatigue in aerospace engineering."
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=128)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print("Deployed Model Response:")
    print(generated_text)
    
    # integrate into a REST API (using FastAPI) and containerize it for deployment on Kubernetes.

if __name__ == "__main__":
    main()
