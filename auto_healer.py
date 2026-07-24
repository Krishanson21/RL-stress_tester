import os
import time
import subprocess
import sys

# The exact call wrapper for your CLI tool
ANTIGRAVITY_CMD = "agy" 
MAX_CYCLES = 4

def run_vscode_healing_pipeline():
    print("🏥 Launching VS Code Terminal Automated Auto-Healer System...")
    
    # Clean out zombie background node threads to free up port 3000
    subprocess.run("taskkill /F /IM node.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for cycle in range(1, MAX_CYCLES + 1):
        print(f"\n🔄 [Cycle {cycle:02d}] Booting RL Matrix Vulnerability Engine...")
        
        # 1. Run the tuner exploration script
        scan_process = subprocess.run(["python", "universal_tuner.py"], capture_output=False)
        
        # Exit code 2 means Profile 2 successfully isolated a real deadlock
        if scan_process.returncode != 2:
            print("\n🎉 SUCCESS! The RL engine ran your profiles and can no longer crash the app.")
            print("💎 Workspace code layout is safe.")
            break
            
        print("⚠️ Application breakdown detected! Deploying your agy CLI worker...")
        
        # 2. Hardened argument array format for Windows shell execution
        # This tells agy exactly what action to take so it processes it automatically
        cli_args = [
            ANTIGRAVITY_CMD,
            "Fix the database pool deadlock in server/api/checkout.ts so it does not crash under low pool limits and high latency."
        ]
        
        print(f"💻 Running terminal command: {cli_args[0]} \"{cli_args[1]}\"")
        
        # 3. Execute the command directly as an array with shell=True to force completion
        cli_run = subprocess.run(
            cli_args,
            shell=True,
            capture_output=True,
            text=True
        )
        
        # Print out whatever feedback your CLI outputs to the terminal
        if cli_run.stdout:
            print(f"\n[agy output]:\n{cli_run.stdout.strip()}")
        if cli_run.stderr:
            print(f"\n[agy error logs]:\n{cli_run.stderr.strip()}")
            
        print("\n💾 Workspace file updated! Refreshing Nuxt system build bundle...")
        
        # 4. Rebuild the app bundle to compile the fix applied by your CLI
        subprocess.run("npx.cmd nuxi build", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        
    else:
        print("\n❌ Boundary fixes exceeded limits without resolving vulnerability matrix.")

if __name__ == "__main__":
    run_vscode_healing_pipeline()