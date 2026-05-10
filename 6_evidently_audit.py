import json
import os
import pandas as pd

from evidently import Report 
from evidently.presets import DataSummaryPreset

def generate_audit_report():
    print("=== 📈 Evidently AI: Ministry of Education Audit Initializing ===")
    
    input_file = os.path.join("data", "evaluation_results.json")
    if not os.path.exists(input_file):
        print("[ERROR] No evaluation data found. Run the Mistral evaluation first.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        eval_data = json.load(f)

    # Prepare Data for Evidently
    print("[EVIDENTLY] Processing data for Data Drift and Quality Analysis...")
    df_data = []
    for item in eval_data:
        correctness = 0
        faithfulness = 0
        for m in item.get("metrics", []):
            if m["name"] == "Correctness":
                correctness = m["score"]
            elif m["name"] == "Faithfulness":
                faithfulness = m["score"]

        df_data.append({
            "Question_Length": len(item["question"]),
            "Answer_Length": len(item["actual_output"]),
            "Correctness_Score": correctness,
            "Faithfulness_Score": faithfulness,
            "Passed_Eval": 1 if item.get("passed", False) else 0
        })

    df = pd.DataFrame(df_data)

    print("[EVIDENTLY] Generating HTML Dashboard Report...")
    audit_report = Report(metrics=[DataSummaryPreset()])
    
    # 💥 THE ULTIMATE FIX: Yeni API'nin istediği gibi dönen objeyi yakalıyoruz!
    my_eval = audit_report.run(reference_data=None, current_data=df)
    
    output_file = os.path.join("data", "evidently_report.html")
    
    # Hangi versiyon kuruluysa ona göre otomatik HTML kaydetme kalkanı!
    try:
        # Yeni versiyon (0.7+)
        my_eval.save_html(output_file)
    except AttributeError:
        # Eski versiyon
        audit_report.save_html(output_file)
    
    print(f"[SUCCESS] Evidently AI HTML Report saved securely to '{output_file}'!")
    print("System: The MVP Architecture is now 100% COMPLETE.")

if __name__ == "__main__":
    generate_audit_report()