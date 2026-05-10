import json
import os
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

def generate_student_answers():
    print("Initializing LangChain and Llama 3 (The Student)...")
    
    # 1. Initialize the local Llama 3 model via Ollama
    llm = Ollama(model="llama3")
    
    # 2. Create the strict prompt template (The Exam Rules)
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a strict military rules of engagement (SROE) expert.\n"
            "Based ONLY on the following context, answer the question accurately and concisely.\n"
            "If the answer is not in the context, state that you do not know.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )
    )
    
    # 3. Load the exam questions (Golden Dataset)
    input_file = os.path.join("data", "golden_dataset.json")
    if not os.path.exists(input_file):
        print(f"[ERROR] Cannot find '{input_file}'. Please run the golden dataset script first.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        exam_data = json.load(f)
        
    print(f"Loaded {len(exam_data)} questions. Starting the exam...")
    
    # 4. Process each question through Llama 3
    student_results = []
    
    for idx, item in enumerate(exam_data, 1):
        print(f"Processing Question {idx}/{len(exam_data)}...")
        
        # Format the prompt with context and question
        formatted_prompt = prompt_template.format(
            context=" ".join(item["context"]),
            question=item["question"]
        )
        
        # Get the answer from Llama 3
        actual_output = llm.invoke(formatted_prompt)
        
        # Save the result
        student_results.append({
            "question": item["question"],
            "expected_output": item["expected_output"],
            "context": item["context"],
            "actual_output": actual_output.strip() # The student's answer
        })
        
    # 5. Save the student's completed exam paper
    output_file = os.path.join("data", "student_answers.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(student_results, f, indent=4)
        
    print(f"[SUCCESS] Llama 3 has completed the exam! Answers saved to '{output_file}'.")
    print("System: Ready for Mistral (DeepEval) to grade the paper.")

if __name__ == "__main__":
    generate_student_answers()