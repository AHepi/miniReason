"""Source-route compatibility checks, independent of semantic content."""
import unittest
from types import SimpleNamespace
from minireason.open_inquiry import _evidence_targets, _target_matches_port


class RouteCompatibility(unittest.TestCase):
    def test_both_evidence_route_apis_preserve_targets(self):
        target = object()
        seen = []
        def by_kind(key):
            seen.append(key)
            return (target,)
        def by_tier(key):
            seen.append(key)
            return (target,)
        self.assertEqual(_evidence_targets(SimpleNamespace(for_kind=by_kind), "evidence"), (target,))
        self.assertEqual(_evidence_targets(SimpleNamespace(for_evidence=by_tier), "evidence"), (target,))
        self.assertEqual(seen, ["evidence.evidence", "evidence"])
        with self.assertRaises(TypeError):
            _evidence_targets(SimpleNamespace(), "evidence")

    def test_pid_and_port_type_routes_match_without_leaking_other_routes(self):
        port = SimpleNamespace(port_id="intake", port_type="open.source-input")
        self.assertTrue(_target_matches_port(SimpleNamespace(tag="pid", port_id="intake"), port))
        self.assertTrue(_target_matches_port(SimpleNamespace(target="port_type", port_type="open.source-input"), port))
        self.assertFalse(_target_matches_port(SimpleNamespace(tag="pid", port_id="elsewhere"), port))
        self.assertFalse(_target_matches_port(SimpleNamespace(tag="context_slot", slot="defs"), port))


if __name__ == "__main__":
    unittest.main()
