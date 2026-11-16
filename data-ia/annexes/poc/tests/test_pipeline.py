import json
import shutil
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fashmatch_poc.audit import verify_chain  # noqa: E402
from fashmatch_poc.pipeline import run  # noqa: E402


class TestPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(ROOT / "config", cls.tmp / "config")
        (cls.tmp / "data" / "raw").mkdir(parents=True)
        cls.m = run(cls.tmp / "config" / "pipeline.yaml", cls.tmp)
        cls.con = sqlite3.connect(cls.tmp / "output" / "fashmatch_v2.sqlite")

    def cols(self, table):
        return [r[1] for r in self.con.execute(f"PRAGMA table_info({table})")]

    def test_aucun_identifiant_direct(self):
        for t in ["profils_personnalisation", "profils_entrainement", "profils_pay3x"]:
            for c in ["email", "full_name", "phone", "street_address", "selfie_uri"]:
                self.assertNotIn(c, self.cols(t))

    def test_aucun_mineur_de_15_ans(self):
        n = self.con.execute("SELECT COUNT(*) FROM profils_personnalisation WHERE 2026 - birth_year < 15").fetchone()[0]
        self.assertEqual(n, 0)

    def test_pay3x_majeurs_seulement(self):
        n = self.con.execute("SELECT COUNT(*) FROM profils_pay3x WHERE pay3x_age_ok = 1 AND 2026 - birth_year < 18").fetchone()[0]
        self.assertEqual(n, 0)

    def test_entrainement_uniquement_consentants(self):
        n = self.con.execute("SELECT COUNT(*) FROM profils_entrainement WHERE consent_training = 0").fetchone()[0]
        self.assertEqual(n, 0)

    def test_purge(self):
        n = self.con.execute("SELECT COUNT(*) FROM profils_personnalisation WHERE last_activity_at < '2023-11-14'").fetchone()[0]
        self.assertEqual(n, 0)

    def test_pas_de_doublons(self):
        self.assertEqual(self.m["apres"]["doublons_user_id"], 0)

    def test_journal_integre_et_sans_donnees_perso(self):
        log = self.tmp / "output" / "audit_log.jsonl"
        self.assertTrue(verify_chain(log))
        self.assertNotIn("@example.test", log.read_text())

    def test_journal_falsifie_detecte(self):
        log = self.tmp / "output" / "audit_log.jsonl"
        lines = log.read_text().splitlines()
        e = json.loads(lines[1]); e["details"]["doublons_supprimes"] = 0
        forged = self.tmp / "forged.jsonl"
        forged.write_text("\n".join([lines[0], json.dumps(e)] + lines[2:]))
        self.assertFalse(verify_chain(forged))


if __name__ == "__main__":
    unittest.main()
