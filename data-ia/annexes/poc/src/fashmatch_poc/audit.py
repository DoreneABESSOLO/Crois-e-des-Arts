"""Journal d'audit des traitements (EX-09).

Chaque entrée est chaînée à la précédente par un hash SHA-256 : toute
modification a posteriori du journal casse la chaîne et se détecte
(journal « protégé en écriture » au sens du how-to tech).
Le journal ne contient jamais de donnée personnelle : seulement des
compteurs, des noms d'étapes et des empreintes.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


class AuditLog:
    def __init__(self, path: Path, run_id: str):
        self.path = path
        self.run_id = run_id
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._prev = self._last_hash()

    def _last_hash(self) -> str:
        if not self.path.exists():
            return "0" * 64
        lines = self.path.read_text(encoding="utf-8").strip().splitlines()
        return json.loads(lines[-1])["hash"] if lines else "0" * 64

    def log(self, step: str, purpose: str, legal_basis: str, **details) -> None:
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "run_id": self.run_id,
            "step": step,
            "purpose": purpose,
            "legal_basis": legal_basis,
            "details": details,
            "prev_hash": self._prev,
        }
        payload = json.dumps(entry, sort_keys=True, ensure_ascii=False)
        entry["hash"] = hashlib.sha256(payload.encode()).hexdigest()
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        self._prev = entry["hash"]


def verify_chain(path: Path) -> bool:
    prev = "0" * 64
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        entry = json.loads(line)
        h = entry.pop("hash")
        if entry["prev_hash"] != prev:
            return False
        if hashlib.sha256(json.dumps(entry, sort_keys=True, ensure_ascii=False).encode()).hexdigest() != h:
            return False
        prev = h
    return True
