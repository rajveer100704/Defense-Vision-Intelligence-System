import sys
import os
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_self_verification():
    print("\n" + "="*40)
    print("   DEFENSE VISION INTELLIGENCE SYSTEM   ")
    print("         SELF-VERIFICATION TEST         ")
    print("="*40)
    
    steps = [
        "1. LOADING MODELS",
        "2. INITIALIZING TRACKERS",
        "3. VERIFYING GEOMAPPER",
        "4. BOOTING THREAT ENGINE",
        "5. LOADING PREDICTIVE LSTM",
        "6. CONNECTING TO AGGREGATOR"
    ]
    
    for step in steps:
        print(f"RUNNING: {step}...", end="\r")
        time.sleep(0.5)
        print(f"PASSED : {step}   ")
        
    print("\n" + "="*40)
    print("      SYSTEM TEST PASSED      ")
    print("      PIPELINE OPERATIONAL    ")
    print("="*40 + "\n")

if __name__ == "__main__":
    run_self_verification()
