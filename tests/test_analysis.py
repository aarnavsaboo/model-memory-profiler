import unittest

from model_memory_profiler.analysis import summarize
from model_memory_profiler.phases import parse_marker


class Tests(unittest.TestCase):
    def test_summary(self):
        rows = [
            {"type":"sample","t_seconds":0,"rss_kb":1000,"child_rss_kb":0},
            {"type":"sample","t_seconds":1,"rss_kb":2000,"child_rss_kb":500},
        ]
        out = summarize(rows)
        self.assertEqual(out["samples"], 2)
        self.assertGreater(out["peak_tree_rss_mb"], 2)

    def test_phase_marker(self):
        self.assertEqual(parse_marker("PROFILE_PHASE: generation"), "generation")


if __name__ == "__main__":
    unittest.main()
