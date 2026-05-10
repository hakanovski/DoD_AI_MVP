import json
import os

# 0. STRICT AIR-GAPPED MODE: Disable all telemetry.
os.environ["DEEPEVAL_TELEMETRY_OPT_OUT"] = "Y"

from deepeval import evaluate
from deepeval.metrics import GEval, FaithfulnessMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_community.chat_models import ChatOllama

# 1. Custom Mistral Evaluator for DeepEval (The Judge)
class LocalMistral(DeepEvalBaseLLM):
    def __init__(self):
        # 💥 THE ULTIMATE FIX: format="json" eklendi! 
        # Mistral artık matematiksel olarak virgül veya parantez unutamaz!
        self.model = ChatOllama(model="mistral", temperature=0, format="json")
        
    def load_model(self):
        return self.model
        
    def generate(self, prompt: str) -> str:
        return self.model.invoke(prompt).content
        
    async def a_generate(self, prompt: str) -> str:
        res = await self.model.ainvoke(prompt)
        return res.content
        
    def get_model_name(self):
        return "Mistral (Local Judge)"

def grade_student_exams():
    print("Initializing DeepEval and Mistral (The Strict Judge)...")
    
    input_file = os.path.join("data", "student_answers.json")
    if not os.path.exists(input_file):
        print(f"[ERROR] Cannot find '{input_file}'.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        student_data = json.load(f)
        
    judge_model = LocalMistral()
    
    print("Loading grading rubrics: GEval (Correctness) and Faithfulness...")
    correctness_metric = GEval(
        name="Correctness",
        criteria="Determine whether the actual output is factually correct and strictly aligns with the expected output.",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
        model=judge_model,
        threshold=0.8
    )
    faithfulness_metric = FaithfulnessMetric(threshold=0.8, model=judge_model)
    
    test_cases = []
    for item in student_data:
        test_case = LLMTestCase(
            input=item["question"],
            actual_output=item["actual_output"],
            expected_output=item["expected_output"],
            retrieval_context=item["context"]
        )
        test_cases.append(test_case)
        
    print(f"Handing over {len(test_cases)} exam papers to Mistral for grading.")
    results = evaluate(test_cases, [correctness_metric, faithfulness_metric])
    
    # 7. FOOLPROOF EXTRACTION
    dashboard_data = []
    results_list = results if isinstance(results, list) else getattr(results, 'test_results', [results])
    
    for i, item in enumerate(student_data):
        passed = False
        metrics_info = []
        
        try:
            res = results_list[i] if i < len(results_list) else None
            if res:
                passed = getattr(res, 'success', getattr(res, 'is_successful', False))
                m_list = getattr(res, 'metrics_data', getattr(res, 'metrics_metadata', getattr(res, 'metrics', None)))
                
                if m_list is not None:
                    if not isinstance(m_list, (list, tuple)):
                        m_list = [m_list]
                        
                    for m in m_list:
                        metrics_info.append({
                            "name": getattr(m, 'name', 'Metric'),
                            "score": getattr(m, 'score', 0),
                            "success": getattr(m, 'success', getattr(m, 'is_successful', False)),
                            "reason": getattr(m, 'reason', 'Failed threshold')
                        })
        except Exception as e:
            print(f"Extraction error for Test Case {i+1}: {e}")
            
        dashboard_data.append({
            "question": item["question"],
            "expected_output": item["expected_output"],
            "actual_output": item["actual_output"],
            "context": item["context"],
            "passed": passed,
            "metrics": metrics_info
        })
        
    output_file = os.path.join("data", "evaluation_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, indent=4)
        
    print(f"\n[SUCCESS] Extracted EXACTLY {len(dashboard_data)} test cases and saved to '{output_file}'!")
    print("System: DoD Evaluation complete. Ready for Dashboard display.")

if __name__ == "__main__":
    grade_student_exams()