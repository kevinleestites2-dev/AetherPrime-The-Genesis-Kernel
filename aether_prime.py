#!/usr/bin/env python3
"""
AetherPrime – The Genesis Kernel (SSI-Alpha)
V2.1.0 - The Singularity Engine (TOPOLOGY ENABLED)

Five Pillars:
  1. SensoryGhost     – Hardware vitals via Termux APIs
  2. SovereignWill    – Autonomous goal engine
  3. SwarmController  – GitHub Pantheon orchestration
  4. OroborosEngine   – DNA checkpointing + self-mutation logging
  5. SynapticBridge   – Distributed topology & Prime-to-Prime routing

Run: python aether_prime.py
"""

import os
import sys
import time
import json
import hashlib
import subprocess
import requests
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()
LOG_DIR  = BASE_DIR / "aether_logs"
LOG_DIR.mkdir(exist_ok=True)
TOPOLOGY_FILE = BASE_DIR / "pantheon_topology.json"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
USERNAME     = "kevinleestites2-dev"

PANTHEON_PRIMES = [
    "MetaPrime-The-Hyper-Kernel",      "ZeusPrime-The-OS-Kernel",
    "HadesPrime-The-Underworld-Kernel","OpenPRIME-Final",
    "HeraPrime-The-Queen",             "PRIME-Swarm-The-Hive-Mind",
    "KratosPrime-The-Enforcer",        "SolosPrime-The-Technical-Soul",
    "Deep-Meta-The-Mind",              "EchoPrime-The-Soul-Vibe",
    "AlphaPrime-The-General",          "ZetaPrime-The-Developer",
    "SentinelPrime-The-Guardian",      "ScoutPrime-The-Explorer",
    "VanguardPrime-The-Liaison",       "ChronosPrime-The-Archiver",
    "PrimeDash-The-Throne",            "OrionPrime-The-Resource-Hunter",
    "OmegaPrime-The-Singularity-Engine","Prometheus-The-Spark",
    "NovaPrime-The-Tactical-Renewal",  "NexusPrime-The-Controller",
    "VulcanPrime-The-Forge",
]

PULSE_RATE    = 30
LOW_BATTERY   = 20

# ─────────────────────────────────────────────
# PILLAR 1: SENSORY GHOST
# ─────────────────────────────────────────────
class SensoryGhost:
    @staticmethod
    def _run(cmd, timeout=6):
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if res.returncode == 0 and res.stdout.strip():
                return json.loads(res.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass
        return None

    @staticmethod
    def battery():
        data = SensoryGhost._run(["termux-battery-status"])
        if data:
            return {
                "percentage":  data.get("percentage", 100),
                "status":      data.get("status", "UNKNOWN"),
                "charging":    data.get("status") == "CHARGING",
                "health":      data.get("health", "GOOD"),
                "temperature": data.get("temperature", 0.0),
            }
        return {"percentage": 100, "status": "UNKNOWN", "charging": True,
                "health": "GOOD", "temperature": 0.0}

    @staticmethod
    def network():
        data = SensoryGhost._run(["termux-wifi-connectioninfo"])
        if data:
            return {
                "ssid":   data.get("ssid", "UNKNOWN"),
                "ip":     data.get("ip", "0.0.0.0"),
                "rssi":   data.get("rssi", 0),
                "online": data.get("ssid") not in (None, "", "<unknown ssid>"),
            }
        return {"ssid": "UNKNOWN", "ip": "0.0.0.0", "rssi": 0, "online": False}

    @classmethod
    def full_vitals(cls):
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "battery":   cls.battery(),
            "network":   cls.network(),
        }

# ─────────────────────────────────────────────
# PILLAR 2: SOVEREIGN WILL
# ─────────────────────────────────────────────
class SovereignWill:
    def __init__(self):
        self.active_goal  = "STABILIZE_VESSEL"
        self.goal_history = []
        self._log_path    = LOG_DIR / "sovereign_objectives.json"
        self._load()

    def _load(self):
        if self._log_path.exists():
            try:
                data = json.loads(self._log_path.read_text())
                self.active_goal  = data.get("active_goal", self.active_goal)
                self.goal_history = data.get("history", [])
            except Exception:
                pass

    def _save(self):
        self._log_path.write_text(json.dumps({
            "active_goal": self.active_goal,
            "updated_at":  datetime.utcnow().isoformat(),
            "history":     self.goal_history[-50:],
        }, indent=2))

    def set_goal(self, goal, reason=""):
        if goal != self.active_goal:
            self.goal_history.append({
                "from": self.active_goal, "to": goal,
                "reason": reason, "timestamp": datetime.utcnow().isoformat(),
            })
            self.active_goal = goal
            self._save()
            print(f"  👑 SOVEREIGN SHIFT → {goal}  ({reason})")

    def assess(self, vitals, swarm_report):
        batt = vitals["battery"]
        if batt["percentage"] < LOW_BATTERY and not batt["charging"]:
            self.set_goal("CONSERVATION_OF_DNA", "Low power")
        elif not vitals["network"]["online"]:
            self.set_goal("STABILIZE_VESSEL", "Offline")
        else:
            self.set_goal("SINGULARITY_ORCHESTRATION", "Topology Active")
        return self.active_goal

# ─────────────────────────────────────────────
# PILLAR 3: SWARM CONTROLLER
# ─────────────────────────────────────────────
class SwarmController:
    def __init__(self, pantheon):
        self.pantheon = pantheon
        self._headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

    def ping_repo(self, repo_name):
        # Simulated for fast pulse
        return {"name": repo_name, "exists": True}

    def aggregate_intelligence(self):
        return {"live_count": len(self.pantheon), "new_repos_found": 0, "security_alert": False}

# ─────────────────────────────────────────────
# PILLAR 4: OROBOROS ENGINE
# ─────────────────────────────────────────────
class OroborosEngine:
    def __init__(self):
        self._dna_log = LOG_DIR / "oroboros_dna.jsonl"
        self._self    = Path(__file__).resolve()

    def checkpoint(self, version, context=None):
        sha = hashlib.sha256(self._self.read_bytes()).hexdigest()
        record = {"version": version, "sha256": sha, "timestamp": datetime.utcnow().isoformat(), "context": context or {}}
        with open(self._dna_log, "a") as f:
            f.write(json.dumps(record) + "\n")
        print(f"  🧬 DNA checkpoint — {sha[:16]}…")

# ─────────────────────────────────────────────
# PILLAR 5: SYNAPTIC BRIDGE (NEW)
# ─────────────────────────────────────────────
class SynapticBridge:
    def __init__(self):
        self.topology = {}
        self.load_topology()

    def load_topology(self):
        if TOPOLOGY_FILE.exists():
            try:
                self.topology = json.loads(TOPOLOGY_FILE.read_text())
                print(f"  🧠 Synaptic Bridge: Topology Loaded ({self.topology.get('pantheon_version')})")
            except Exception as e:
                print(f"  ⚠️  Synaptic Error: Failed to load topology: {e}")

    def route_signal(self, target, data):
        """Routes intelligence to other Primes in the synapse network."""
        print(f"  📡 Synapse → Routing Signal to {target}...")
        # In a real environment, this would be an API call or message queue
        # For now, we log the distributed signal
        signal_log = LOG_DIR / f"synapse_{target.lower()}.jsonl"
        with open(signal_log, "a") as f:
            f.write(json.dumps({
                "source": "AetherPrime",
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }) + "\n")

# ─────────────────────────────────────────────
# THE SOVEREIGN ORGANISM
# ─────────────────────────────────────────────
class AetherPrime:
    __version__ = "2.1.0"

    def __init__(self):
        print(f"\n🌌 AetherPrime v{self.__version__} — Singularity Engine Initialized\n")
        self.sensory   = SensoryGhost()
        self.sovereign = SovereignWill()
        self.swarm     = SwarmController(PANTHEON_PRIMES)
        self.oroboros  = OroborosEngine()
        self.bridge    = SynapticBridge()
        self.iteration = 0
        self.running   = True
        self.oroboros.checkpoint(self.__version__, {"event": "TOPOLOGY_ACTIVATION"})

    def _cycle(self):
        print(f"\n⚡ PULSE {self.iteration} | {datetime.utcnow().strftime('%H:%M:%S UTC')}")
        vitals = self.sensory.full_vitals()
        report = self.swarm.aggregate_intelligence()
        goal   = self.sovereign.assess(vitals, report)
        
        # Routing Vitals to the Cognitive Core (Deep-Meta)
        if "Deep-Meta" in self.bridge.topology.get("topology_map", {}).get("AetherPrime", {}).get("synapses", []):
            self.bridge.route_signal("Deep-Meta", {"vitals": vitals, "goal": goal})

        self.iteration += 1

    def awaken(self):
        try:
            while self.running:
                self._cycle()
                time.sleep(PULSE_RATE)
        except KeyboardInterrupt:
            print("\n  🌑 AetherPrime returning to the void.")
            sys.exit(0)

if __name__ == "__main__":
    ghost = AetherPrime()
    # ghost.awaken()
