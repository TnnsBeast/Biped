"""Unit/geometry/cost checks for the miniature planning screen, no CAD claims."""

from decimal import Decimal
import json
import math
import unittest

import mini_biped_calc as calc


class MiniatureScreenTests(unittest.TestCase):
    def test_force_units(self):
        # One kgf at a one-metre arm is standard gravity N·m.
        self.assertAlmostEqual(100 * calc.KG_CM_TO_NM, 9.80665)
        self.assertAlmostEqual(10 * calc.KG_CM_TO_NM, 0.980665)

    def test_straight_pose_zero_knee_lever(self):
        result = calc.vertical_force_screen(1.0, 0)
        self.assertEqual(result["knee_torque_nm"], 0.0)
        self.assertAlmostEqual(result["hip_height_m"], 0.170)

    def test_folded_geometry_and_support_share(self):
        # beta=120 -> link tilt=60; height is L + wheel radius.
        both = calc.vertical_force_screen(1.2, 120)
        one = calc.vertical_force_screen(1.2, 120, support_legs=1)
        self.assertAlmostEqual(both["hip_height_m"], 0.100)
        self.assertAlmostEqual(both["knee_lever_m"], 0.070 * math.sqrt(3) / 2)
        self.assertAlmostEqual(one["knee_torque_nm"], 2 * both["knee_torque_nm"])
        self.assertAlmostEqual(calc.vertical_force_screen(1.2, 120, multiplier=2)["knee_torque_nm"], one["knee_torque_nm"])

    def test_hip_ground_moment_sign_and_centered_pose(self):
        self.assertEqual(calc.hip_vertical_force_moment(1.0, 0), 0)
        moment = calc.hip_vertical_force_moment(1.0, 0.04)
        self.assertAlmostEqual(moment, 0.196133)
        self.assertAlmostEqual(calc.hip_vertical_force_moment(1.0, -0.04), -moment)

    def test_rpm_to_surface_speed(self):
        self.assertAlmostEqual(calc.wheel_speed_m_s(60, 1 / math.pi), 1.0)

    def test_invalid_pose_is_rejected(self):
        for kwargs in ({"mass_kg": 0, "flexion_deg": 90},
                       {"mass_kg": 1, "flexion_deg": 180},
                       {"mass_kg": 1, "flexion_deg": -1},
                       {"mass_kg": 1, "flexion_deg": 90, "support_legs": 0}):
            with self.assertRaises(ValueError):
                calc.vertical_force_screen(**kwargs)

    def test_product_budget_and_sample_are_not_full_robot_quote(self):
        data = json.loads(calc.INPUTS.read_text())
        core, total, sample = calc.budgets(data)
        self.assertEqual(core, Decimal("128.45"))
        self.assertEqual(total, Decimal("266.83"))
        self.assertEqual(sample, Decimal("46.82"))
        # A real change to an allowance must propagate, not silently keep cap.
        data["budget_allowances_usd"]["shipping_tax_contingency"] = "50.00"
        self.assertEqual(calc.budgets(data)[1], Decimal("286.83"))


if __name__ == "__main__":
    unittest.main()
