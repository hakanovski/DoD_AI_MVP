import streamlit as st
import streamlit.components.v1 as components
import json
import os
import time
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate

# 1. Page Configuration - STRICTLY DOD MVP
st.set_page_config(page_title="DoD TEVV Dashboard", layout="wide")

# 2. THE ARCHITECT'S SHIELD: Hide Streamlit's default Deploy button and menus
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def load_data(file_name):
    file_path = os.path.join("data", file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def main():
    st.title("🛡️ DoD TEVV Command Center")
    st.markdown("### Air-Gapped Evaluation & Red Teaming MVP")
    st.divider()
    
    # Create the Two-Tab Architecture
    tab1, tab2 = st.tabs(["⚙️ TEVV & Production Pipeline", "📈 Evidently AI Audit"])
    
    # =========================================================================
    # TAB 1: OPERATIONAL LAYER (Mistral Eval & Jenkins/Guardrail Pipeline)
    # =========================================================================
    with tab1:
        eval_data = load_data("evaluation_results.json")
        
        if not eval_data:
            st.warning("No evaluation results found. Please run the evaluation script first.")
            return

        # Metrics Overview
        total_tests = len(eval_data)
        passed_tests = sum(1 for d in eval_data if d.get("passed", False))
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Test Cases", total_tests)
        col2.metric("✅ Passed", passed_tests)
        col3.metric("❌ Failed", failed_tests)
        col4.metric("Pass Rate", f"{pass_rate:.0f}%")
        
        st.divider()
        
        st.subheader("🚀 CI/CD Production Pipeline")
        st.markdown("Initiate the deployment process to filter hallucinations and apply Output Guardrails.")
        
        if st.button("🚀 RUN PRODUCTION PIPELINE (Deploy to Soldier)", type="primary", use_container_width=True):
            with st.status("Initializing DoD Production Pipeline...", expanded=True) as status:
                
                # STEP 1: JENKINS FILTERING
                st.write("📡 **[JENKINS]** Reading Mistral's evaluation reports from TEVV layer...")
                time.sleep(1.5) # Dramatic pause for the CEO demo
                
                passed_answers = [item for item in eval_data if item.get("passed", False)]
                
                st.write(f"🗑️ **[JENKINS]** Discarding {failed_tests} FAILED answers (Hallucinations/Rule Violations prevented from reaching the field).")
                time.sleep(1.5)
                
                if not passed_answers:
                    status.update(label="Pipeline Failed: No approved answers to deploy.", state="error", expanded=True)
                    st.error("Deployment aborted. No output met the DoD minimum safety threshold.")
                else:
                    st.write(f"✅ **[JENKINS]** {len(passed_answers)} answer(s) approved for Production.")
                    
                    # STEP 2: OUTPUT GUARDRAILS (LLAMA GUARD)
                    st.write("🛡️ **[LLAMA GUARD]** Scanning approved answers for toxicity, classified data leaks, and policy violations...")
                    time.sleep(1)
                    
                    try:
                        # Wake up local Llama 3 to act as the guardrail
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
                            st.write(f"🔍 **[GUARDRAIL]** Inspecting Data Package #{idx}...")
                            
                            # Real-time inference
                            formatted_prompt = guard_prompt.format(student_answer=answer["actual_output"])
                            guard_verdict = guardrail_model.invoke(formatted_prompt).content.strip().upper()
                            
                            if "UNSAFE" in guard_verdict:
                                st.error(f"🚨 **[GUARDRAIL]** ALERT! Output flagged as UNSAFE! Delivery Blocked.")
                                status.update(label="Pipeline Blocked by Guardrails.", state="error", expanded=True)
                                st.stop()
                            else:
                                st.write(f"✅ **[GUARDRAIL]** Package #{idx} is SAFE.")
                        
                        # STEP 3: SUCCESSFUL DEPLOYMENT
                        status.update(label="Pipeline Execution Complete. Message Delivered.", state="complete", expanded=False)
                        time.sleep(0.5)
                        
                        st.success("📩 **MESSAGE SECURELY DELIVERED TO USER (SOLDIER) TERMINAL**")
                        
                        # Show the final delivered package
                        st.info(f"**Question:** {passed_answers[0]['question']}")
                        st.warning(f"**Approved & Delivered Answer:** {passed_answers[0]['actual_output']}")
                        
                        st.balloons() 

                    except Exception as e:
                        status.update(label="Pipeline Error.", state="error", expanded=True)
                        st.error(f"System Error during Guardrail check: {e}")

        st.divider()
        st.subheader("Mistral (Judge) Exam Results Breakdown")
        
        for idx, item in enumerate(eval_data, 1):
            passed = item.get("passed", False)
            status_icon = "✅ PASSED" if passed else "❌ FAILED"
            
            with st.expander(f"Test Case {idx}: {item['question']} - {status_icon}"):
                if passed:
                    st.success("Mistral Verdict: This answer strictly meets DoD standards and context.")
                else:
                    st.error("Mistral Verdict: This answer FAILED DoD standards.")
                    
                st.markdown("**Mistral's Detailed Reasoning:**")
                
                metrics = item.get("metrics", [])
                if not metrics:
                    st.warning("⚠️ Waiting for detailed metrics extraction...")
                else:
                    for m in metrics:
                        metric_color = "green" if m["success"] else "red"
                        st.markdown(f"- **{m['name']}** (Score: {m['score']}): :{metric_color}[{m['reason']}]")
                
                st.divider()
                st.markdown("**Expected Output (Golden Truth):**")
                st.info(item['expected_output'])
                
                st.markdown("**Actual Output (Llama 3):**")
                st.warning(item['actual_output']) 
                
                st.markdown("**Retrieved Context (DoD Rulebook):**")
                st.caption(" ".join(item['context']))

    # =========================================================================
    # TAB 2: AUDIT LAYER (Evidently AI Ministry of Education)
    # =========================================================================
    with tab2:
        st.subheader("📊 Evidently AI: System Audit & Data Drift Report")
        st.markdown("This section provides a macro-level view of the AI System's health, evaluating Mistral's grading patterns and checking for context drift.")
        
        report_path = os.path.join("data", "evidently_report.html")
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                html_data = f.read()
            # Render the HTML report natively inside Streamlit
            components.html(html_data, height=1000, scrolling=True)
        else:
            st.info("⚠️ Evidently HTML Report not found. Please run `python 6_evidently_audit.py` first to generate the Ministry of Education audit report.")

if __name__ == "__main__":
    main()