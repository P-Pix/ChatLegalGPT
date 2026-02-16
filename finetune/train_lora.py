"""Entraînement LoRA (SFT) avec TRL.

Exemple:
python train_lora.py \
  --model mistralai/Mistral-7B-Instruct-v0.3 \
  --dataset ../datasets/sft_train.jsonl \
  --out_dir ../models/chatlegalgpt-lora \
  --epochs 1 \
  --batch_size 1 \
  --grad_accum 8

Notes:
- Le dataset doit contenir: instruction, context, output (JSONL).
- On entraîne le modèle à produire une réponse structurée, avec citations.
"""

import argparse, os
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig
from trl import SFTTrainer
from transformers import TrainingArguments

def format_example(example):
    system = (
        "Tu es ChatLegalGPT, assistant d'information juridique sur le droit français. "
        "Tu dois répondre en français, avec des citations [SOURCE 1] etc., et refuser si le contexte ne suffit pas."
    )
    prompt = (
        f"<s>[SYSTEM]\n{system}\n[/SYSTEM]\n"
        f"[USER]\nQuestion: {example['instruction']}\n\n"
        f"Contexte (extraits officiels):\n{example['context']}\n[/USER]\n"
        f"[ASSISTANT]\n{example['output']}\n[/ASSISTANT]</s>"
    )
    return prompt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--dataset", required=True, help="JSONL avec instruction/context/output")
    p.add_argument("--out_dir", required=True)
    p.add_argument("--epochs", type=int, default=1)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--batch_size", type=int, default=1)
    p.add_argument("--grad_accum", type=int, default=8)
    p.add_argument("--max_seq_len", type=int, default=2048)
    args = p.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    ds = load_dataset("json", data_files=args.dataset, split="train")

    tokenizer = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        device_map="auto",
        torch_dtype="auto"
    )

    lora = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
    )

    training_args = TrainingArguments(
        output_dir=args.out_dir,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        logging_steps=10,
        save_steps=200,
        save_total_limit=2,
        fp16=True,
        bf16=False,
        optim="paged_adamw_8bit",
        report_to="none"
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=ds,
        peft_config=lora,
        max_seq_length=args.max_seq_len,
        formatting_func=format_example,
        args=training_args
    )

    trainer.train()
    trainer.model.save_pretrained(args.out_dir)
    tokenizer.save_pretrained(args.out_dir)

    print("OK: saved LoRA adapter to", args.out_dir)

if __name__ == "__main__":
    main()
