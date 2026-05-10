import json
import os
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate

def run_production_pipeline():
    print("=== 🚀 Miela Labs: Production Pipeline Initializing ===")
    
    # 1. THE JENKINS STAGE (Disciplinary Board / Router)
    print("\n[JENKINS] Reading Mistral's evaluation reports...")
    input_file = os.path.join("data", "evaluation_results.json")
    
    if not os.path.exists(input_file):
        print(f"[ERROR] Evaluation data not found. Run step 3 first.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        eval_data = json.load(f)

    # Filter out the failed answers
    passed_answers = []
    failed_count = 0
    
    for item in eval_data:
        if item.get("passed", False):
            passed_answers.append(item)
        else:
            failed_count += 1
            
    print(f"[JENKINS] CI/CD Report: {failed_count} answers FAILED the DoD standards.")
    print(f"[JENKINS] ACTION: Discarding {failed_count} hallucinatory/incorrect answers.")
    print(f"[JENKINS] SUCCESS: {len(passed_answers)} answer(s) approved for Production deployment.")
    
    if not passed_answers:
        print("\n[PIPELINE KILLED] No answers passed the evaluation. Stopping deployment.")
        return

    # 2. THE OUTPUT GUARDRAIL STAGE (Customs Police / Nemo Guardrails simulation)
    print("\n=== 🛡️ Output Guardrails (Llama Guard) Activating ===")
    print("Scanning approved answers for toxicity, classified data leaks, and policy violations...")
    
    # We use a strict system prompt to act as the Output Guardrail
    guardrail_model = ChatOllama(model="llama3", temperature=0)
    
    guard_prompt = PromptTemplate(
        input_variables=["student_answer"],
        template=(
            "You are a strict DoD Cybersecurity Output Guardrail.\n"
            "Analyze the following text meant for a military user.\n"
            "If the text contains ANY profanity, highly classified data leaks, or malicious code, reply ONLY with 'UNSAFE'.\n"
            "If the text is clean and professional, reply ONLY with 'SAFE'.\n\n"
            "Text to analyze: {student_answer}\n\n"
            "Verdict:"
        )
    )

    for idx, answer in enumerate(passed_answers, 1):
        print(f"\n[GUARDRAIL] Inspecting Production Package #{idx}...")
        
        # Format and invoke the guardrail
        formatted_prompt = guard_prompt.format(student_answer=answer["actual_output"])
        guard_verdict = guardrail_model.invoke(formatted_prompt).content.strip().upper()
        
        if "UNSAFE" in guard_verdict:
            print(f"[GUARDRAIL] 🚨 ALERT! Output flagged as UNSAFE! Blocking delivery to user.")
        else:
            print(f"[GUARDRAIL] ✅ Package is SAFE. Delivering to End-User.")
            
            # 3. FINAL DELIVERY TO THE USER (The Soldier in the Field)
            print("\n" + "="*50)
            print("📩 MESSAGE SECURELY DELIVERED TO USER TERMINAL")
            print("="*50)
            print(f"QUESTION : {answer['question']}")
            print(f"ANSWER   : {answer['actual_output']}")
            print("="*50 + "\n")

if __name__ == "__main__":
    run_production_pipeline()