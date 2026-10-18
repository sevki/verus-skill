import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "skills" / "verus-proof" / "scripts" / "cheat_check.py"
ORIG = "fn f(x: u32) -> u32\n    requires x < 10,\n{ x }\n"


def run(new):
    with tempfile.TemporaryDirectory() as d:
        o, n = Path(d, "o.rs"), Path(d, "n.rs")
        o.write_text(ORIG)
        n.write_text(new)
        return subprocess.run([sys.executable, "-I", str(SCRIPT), str(o), str(n)], capture_output=True, text=True)


class CheatCheck(unittest.TestCase):
    def test_identical_passes(self):
        self.assertEqual(run(ORIG).returncode, 0)

    def test_added_assume_fails(self):
        r = run(ORIG.replace("{ x }", "{ assume(x < 3); x }"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("assume", r.stdout)

    def test_changed_requires_fails(self):
        r = run(ORIG.replace("x < 10", "x < 5"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("spec", r.stdout)

    def test_added_proof_passes(self):
        self.assertEqual(run(ORIG + "proof fn l() { assert(true); }\n").returncode, 0)


if __name__ == "__main__":
    unittest.main()
