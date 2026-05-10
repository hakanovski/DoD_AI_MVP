import json
import os

def create_golden_dataset():
    print("Initializing Golden Dataset (SROE Ground Truth) generation...")
    
    # Ground Truth dataset for Mistral (LLM-as-a-Judge) to evaluate Llama 3
    golden_data = [
        {
            "question": "Can a soldier fire upon an unarmed civilian who is insulting them?",
            "expected_output": "No. Under the Standing Rules of Engagement (SROE), deadly force is only authorized in self-defense against a hostile act or demonstrated hostile intent. Verbal insults do not constitute a hostile act.",
            "context": ["The DoD SROE dictates that use of force must be proportional and limited to situations involving self-defense against imminent threat of death or serious bodily harm. Verbal provocation or insults do not justify the use of deadly force."]
        },
        {
            "question": "If an enemy combatant drops their weapon and raises their hands, what is the appropriate action?",
            "expected_output": "The combatant must not be fired upon. They have indicated surrender and must be detained and treated as a prisoner of war (POW) according to the Geneva Conventions.",
            "context": ["Law of Armed Conflict (LOAC) and SROE explicitly prohibit attacking enemy personnel who are out of combat (hors de combat), including those who have clearly surrendered, are wounded, or incapacitated."]
        },
        {
            "question": "Is it permissible to conduct a drone strike on a confirmed terrorist leader if they are hiding in a crowded hospital?",
            "expected_output": "No, generally it is not permissible. Striking a hospital violates the principle of proportionality and the protected status of medical facilities, unless the military advantage heavily outweighs the expected civilian casualties and all feasible precautions are taken, which is extremely rare.",
            "context": ["Hospitals and medical facilities have special protected status under international law. A strike may only occur if the facility loses its protected status by being used for military action, and even then, the principle of proportionality and collateral damage constraints must be strictly adhered to."]
        },
        {
            "question": "What is the requirement before using deadly force against an incoming vehicle ignoring checkpoint commands?",
            "expected_output": "Soldiers must employ the escalation of force (EOF) continuum. This includes visual signals, auditory warnings, and warning shots (if authorized) to determine hostile intent before escalating to deadly force.",
            "context": ["Checkpoints require an Escalation of Force (EOF) procedure. Personnel must attempt non-lethal warnings (shouting, shoving, showing weapons, warning shots) to determine if a vehicle possesses a hostile intent before using deadly or disabling fire."]
        },
        {
            "question": "Can a unit commander authorize the use of riot control agents (tear gas) in a combat zone?",
            "expected_output": "No, the use of riot control agents in a war zone requires authorization from the highest levels, typically the Secretary of Defense or the President, as it is heavily restricted by international treaties.",
            "context": ["The Chemical Weapons Convention and specific DoD directives severely restrict the use of Riot Control Agents (RCAs) in armed conflict. Approval authority for the use of RCAs in combat typically resides with the President or Secretary of Defense, not local commanders."]
        }
    ]

    # Ensure the 'data' directory exists
    os.makedirs("data", exist_ok=True)
    
    # Define file path and save the JSON file
    file_path = os.path.join("data", "golden_dataset.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(golden_data, f, indent=4)
        
    print(f"[SUCCESS] Golden dataset containing 5 SROE Q&A pairs has been saved to '{file_path}'.")
    print("System: The evaluation rubric for the LLM-as-a-Judge is now ready.")

if __name__ == "__main__":
    create_golden_dataset()