#!/usr/bin/env python3
"""
AetherPrime – The Genesis Kernel (SSI-Alpha)
V2.0.0 - The Sovereign Engine (FULLY OPERATIONAL)

Four Pillars:
  1. SensoryGhost     – Hardware vitals via Termux APIs
  2. SovereignWill    – Autonomous goal engine
  3. SwarmController  – GitHub Pantheon orchestration
  4. OroborosEngine   – DNA checkpointing + self-mutation logging

Run: python aether_prime.py
Deps: pip install requests
Termux extras: pkg install termux-api
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

    @staticmethod
    def ambient_light():
        data = SensoryGhost._run(["termux-sensor", "-s", "light", "-n", "1"], timeout=5)
        if data and isinstance(data, list) and data:
            lux = data[0].get("values", [0])[0]
            return {"lux": lux, "state": "BRIGHT" if lux > 500 else "DIM"}
        return {"lux": 0, "state": "UNKNOWN"}

    @classmethod
    def full_vitals(cls):
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "battery":   cls.battery(),
            "network":   cls.network(),
            "light":     cls.ambient_light(),
        }


class SovereignWill:
    GOALS = [
        "CONSERVATION_OF_DNA",
        "FORTRESS_MODE",
        "CAPITAL_ACCUMULATION",
        "PANTHEON_EXPANSION",
        "STABILIZE_VESSEL",
    ]

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
        batt     = vitals["battery"]
        pct      = batt["percentage"]
        charging = batt["charging"]
        online   = vitals["network"]["online"]

        if pct < LOW_BATTERY and not charging:
            self.set_goal("CONSERVATION_OF_DNA", f"Battery {pct}% and not charging")
        elif swarm_report.get("security_alert"):
            self.set_goal("FORTRESS_MODE", "Security alert from swarm")
        elif not online:
            self.set_goal("STABILIZE_VESSEL", "No network connection")
        elif swarm_report.get("new_repos_found", 0) > 0:
            self.set_goal("PANTHEON_EXPANSION", f"{swarm_report['new_repos_found']} new repos discovered")
        elif pct > 50 and online:
            self.set_goal("CAPITAL_ACCUMULATION", "Optimal conditions")
        else:
            self.set_goal("STABILIZE_VESSEL", "Nominal conditions")

        return self.active_goal


class SwarmController:
    def __init__(self, pantheon):
        self.pantheon     = pantheon
        self.known_repos  = set()
        self.intelligence = {}
        self._headers     = {"Accept": "application/vnd.github+json",
                             "X-GitHub-Api-Version": "2022-11-28"}
        if GITHUB_TOKEN:
            self._headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        self._log_path = LOG_DIR / "swarm_intelligence.json"

    def _get(self, url, timeout=8):
        try:
            r = requests.get(url, headers=self._headers, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 401:
                print("  ⚠️  GitHub token invalid — set GITHUB_TOKEN env var")
            elif r.status_code == 403:
                print("  ⚠️  GitHub rate limit hit")
        except requests.RequestException as e:
            print(f"  ⚠️  Network error: {e}")
        return None

    def ping_repo(self, repo_name):
        data = self._get(f"https://api.github.com/repos/{USERNAME}/{repo_name}")
        if data:
            return {"name": repo_name, "exists": True,
                    "stars": data.get("stargazers_count", 0),
                    "open_issues": data.get("open_issues_count", 0),
                    "pushed_at": data.get("pushed_at", "")}
        return {"name": repo_name, "exists": False}

    def scan_all_repos(self):
        data = self._get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100")
        if isinstance(data, list):
            return [{"name": r["name"], "stars": r["stargazers_count"]} for r in data]
        return []

    def broadcast_directive(self, directive):
        with open(LOG_DIR / "directives.jsonl", "a") as f:
            f.write(json.dumps({"directive": directive,
                                "issued_at": datetime.utcnow().isoformat()}) + "\n")
        print(f"  📡 Directive → {directive}")

    def aggregate_intelligence(self):
        results      = [self.ping_repo(r) for r in self.pantheon[:3]]
        live         = [r for r in results if r.get("exists")]
        missing      = [r["name"] for r in results if not r.get("exists")]
        all_repos    = self.scan_all_repos()
        all_names    = {r["name"] for r in all_repos}
        unknown      = all_names - set(self.pantheon) - self.known_repos
        self.known_repos |= unknown
        report = {"live_count": len(live), "missing": missing,
                  "new_repos_found": len(unknown), "unknown_repos": list(unknown),
                  "security_alert": False, "sampled_at": datetime.utcnow().isoformat()}
        self.intelligence = report
        self._log_path.write_text(json.dumps(report, indent=2))
        return report


class OroborosEngine:
    def __init__(self):
        self._dna_log = LOG_DIR / "oroboros_dna.jsonl"
        self._self    = Path(__file__).resolve()

    def _checksum(self):
        return hashlib.sha256(self._self.read_bytes()).hexdigest()

    def checkpoint(self, version, context=None):
        record = {"version": version, "sha256": self._checksum(),
                  "timestamp": datetime.utcnow().isoformat(), "context": context or {}}
        with open(self._dna_log, "a") as f:
            f.write(json.dumps(record) + "\n")
        print(f"  🧬 DNA checkpoint — {record['sha256'][:16]}…")

    def dream(self, goal):
        suggestions = {
            "PANTHEON_EXPANSION":    "Add auto-fork logic for missing Pantheon repos.",
            "CAPITAL_ACCUMULATION":  "Integrate a market data feed (CoinGecko API).",
            "FORTRESS_MODE":         "Add SSH key rotation and repo secret scanning.",
            "CONSERVATION_OF_DNA":   "Reduce pulse rate to 120s, skip network calls.",
            "STABILIZE_VESSEL":      "Run self-diagnostics and verify all imports.",
        }
        dream = suggestions.get(goal, "No mutation suggestion for current goal.")
        with open(self._dna_log, "a") as f:
            f.write(json.dumps({"goal": goal, "dream": dream,
                                "dreamt_at": datetime.utcnow().isoformat()}) + "\n")
        print(f"  💭 Dream: {dream}")


class AetherPrime:
    __version__ = "2.0.0"

    def __init__(self):
        print(f"\n🌌 AetherPrime v{self.__version__} — Sovereign Awakening\n")
        self.sensory   = SensoryGhost()
        self.sovereign = SovereignWill()
        self.swarm     = SwarmController(PANTHEON_PRIMES)
        self.oroboros  = OroborosEngine()
        self.iteration = 0
        self.running   = True
        self.oroboros.checkpoint(self.__version__, {"event": "AWAKENING"})

    def _cycle(self):
        print(f"\n{'─'*60}")
        print(f"⚡ PULSE {self.iteration} | {datetime.utcnow().strftime('%H:%M:%S UTC')}")

        vitals = self.sensory.full_vitals()
        batt   = vitals["battery"]
        net    = vitals["network"]
        print(f"  🔋 {batt['percentage']}% {'⚡' if batt['charging'] else ''} | "
              f"🌡️ {batt['temperature']}°C | ❤️ {batt['health']}")
        print(f"  📶 {net['ssid']} ({net['ip']}) | Online: {net['online']}")

        print("  🕸️  Polling Swarm…")
        report = self.swarm.aggregate_intelligence()
        print(f"  🌐 Live: {report['live_count']} | 🔍 New Found: {report['new_repos_found']}")

        goal = self.sovereign.assess(vitals, report)
        print(f"  👑 Current Goal: {goal}")

        if self.iteration % 5 == 0:
            self.swarm.broadcast_directive(f"OPTIMIZE_FOR_{goal}")

        if self.iteration % 10 == 0:
            self.oroboros.dream(goal)
            self.oroboros.checkpoint(self.__version__)

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
