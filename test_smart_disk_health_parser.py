import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import parse_smart

GOOD = """Device Model:     TESTDISK 1000
Serial Number:    SN123
SMART overall-health self-assessment test result: PASSED
  5 Reallocated_Sector_Ct   0x0033   100   100   010    Pre-fail  Always       -       0
  9 Power_On_Hours          0x0032   100   100   000    Old_age   Always       -       1234
194 Temperature_Celsius     0x0022   100   100   000    Old_age   Always       -       34
"""


class TestSmartParser(unittest.TestCase):
    def test_ok_verdict(self):
        r = parse_smart(GOOD)
        self.assertEqual(r["verdict"], "OK")
        self.assertEqual(r["model"], "TESTDISK 1000")
        self.assertEqual(r["power_on_hours"], "1234")

    def test_failed_health(self):
        r = parse_smart(GOOD.replace("PASSED", "FAILED"))
        self.assertEqual(r["verdict"], "FAIL")

    def test_reallocated_triggers_warning(self):
        r = parse_smart(GOOD.replace("-       0\n  9", "-       7\n  9"))
        self.assertEqual(r["verdict"], "WARNING")
        self.assertEqual(r["reallocated_sectors"], 7)


if __name__ == "__main__":
    unittest.main()
