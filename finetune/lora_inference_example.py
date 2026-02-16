"""Exemple de chargement d'un adaptateur LoRA pour l'inférence.

Usage:
python lora_inference_example.py --base mistralai/Mistral-7B-Instruct-v0.3 --lora ../models/chatlegalgpt-lora
"""

import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True)
    p.add_argument("--lora", required=True)
    args = p.parse_args()

    tok = AutoTokenizer.from_pretrained(args.base)
    model = AutoModelForCausalLM.from_pretrained(args.base, device_map="auto", torch_dtype="auto")
    model = PeftModel.from_pretrained(model, args.lora)

    prompt = "Explique brièvement la différence entre un décret et une loi."
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    out = model.generate(**inputs, max_new_tokens=200, temperature=0.2, top_p=0.9)
    print(tok.decode(out[0], skip_special_tokens=True))

if __name__ == "__main__":
    main()
