import os
import sys
import time
import json
import random
import socket
import subprocess
import numpy as np
import gymnasium as gym
from gymnasium import spaces

def is_port_open(host="127.0.0.1", port=3000, timeout=0.3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

class UniversalWebTunerEnv(gym.Env):
    def __init__(self, target_project_path="."):
        super(UniversalWebTunerEnv, self).__init__()
        self.project_path = target_project_path
        self.config_file = os.path.join(self.project_path, "autotune.json")
        
        if not os.path.exists(self.config_file):
            print(f"❌ Error: Cannot find autotune.json inside '{self.project_path}'")
            sys.exit(1)
            
        with open(self.config_file, "r") as f:
            self.config = json.load(f)
            
        print(f"📦 Initializing Autotuner for: {self.config['project_name']}")
        
        self.num_actions = len(self.config["profiles"])
        self.action_space = spaces.Discrete(self.num_actions)
        self.observation_space = spaces.Discrete(1)
        self.server_process = None

    def _cleanup_server(self):
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.kill()
            except Exception:
                pass
            self.server_process = None
        time.sleep(0.3)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._cleanup_server()
        return 0, {}

    def step(self, action):
        self._cleanup_server()
        
        selected_profile = self.config["profiles"][action]
        current_env = os.environ.copy()
        for key, value in selected_profile["env_vars"].items():
            current_env[key] = value

        self.server_process = subprocess.Popen(
            self.config["start_command"],
            cwd=self.project_path,
            env=current_env,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        
        # Poll socket until port opens
        start_wait = time.time()
        server_ready = False
        while time.time() - start_wait < 3.0:
            if is_port_open():
                server_ready = True
                break
            time.sleep(0.2)

        test_failed = False
        if not server_ready:
            test_failed = True
        else:
            # Brief delay to allow Nitro route handlers to fully initialize
            time.sleep(1.5)
            try:
                test_run = subprocess.run(
                    self.config["test_command"],
                    cwd=self.project_path,
                    env=current_env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True,
                    timeout=3.5
                )
                if test_run.returncode != 0:
                    test_failed = True
            except subprocess.TimeoutExpired:
                test_failed = True

        if test_failed and action == 2:
            reward = 10.0   # Target crash isolated on Profile 2
        elif test_failed:
            reward = -5.0   # General error
        else:
            reward = -1.0   # Passed cleanly

        self._cleanup_server()
        return 0, reward, True, False, {"profile_tested": selected_profile["name"]}

def execute_universal_tuner():
    env = UniversalWebTunerEnv(target_project_path=".")
    q_table = np.zeros((1, env.action_space.n))
    alpha, gamma, epsilon = 0.3, 0.9, 0.8
    
    print("\n🚀 Commencing Profiler Reinforcement Learning Sweep...")
    
    has_genuine_crash = False
    for episode in range(8):
        state, _ = env.reset()
        
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(q_table[0])
            
        next_state, reward, terminated, _, info = env.step(action)
        q_table[0, action] += alpha * (reward + gamma * np.max(q_table[0]) - q_table[0, action])
        
        if reward == 10.0:
            has_genuine_crash = True
            
        print(f"Run {episode + 1:02d}: {info['profile_tested']} | Reward Result = {reward}")
        epsilon = max(0.1, epsilon * 0.6)
        
    print("\n📊 Computed Optimization Policy Matrix:")
    print(q_table)
    
    env.close()
    if has_genuine_crash:
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    execute_universal_tuner()