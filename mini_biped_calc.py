#!/usr/bin/env python3
"""Miniature feasibility screens, not CAD measurements or a release gate.

Run `python3 mini_biped_calc.py` to reproduce the numerical appendix in
docs/design/miniature_wheeled_biped_study.md. Standard library only.

Published inputs and their access qualifications are in
evidence/miniature/2026-10-11_research/vendor_inputs.json. All dimensions,
mass allocations, derating, and control rates below are DESIGN ASSUMPTIONS.
The vertical-force statics omit link mass distribution, horizontal forces,
wheel reaction torque, compliance, friction, inertia, and impacts. Passing
this screen does not establish an operating envelope or structural margin.
"""

from decimal import Decimal
import json
import math
from pathlib import Path

INPUTS = Path(__file__).resolve().parent / "evidence/miniature/2026-10-11_research/vendor_inputs.json"
G = 9.80665  # conventional standard gravity; also used by r2a_calc.py
KG_CM_TO_NM = G / 100.0  # kgf * cm, not kg * cm

# DESIGN ASSUMPTIONS: candidates for packaging and later CAD/load analysis.
LINK_M = 0.070
WHEEL_DIAMETER_M = 0.060
MASS_TARGET_KG = 1.000
MASS_SCREEN_KG = 1.200
STATIC_DERATING = 0.50  # planning reserve, not a measured continuous rating
HIP_WHEEL_OFFSET_M = 0.040
LOCAL_LOOP_HZ = 500
JOINT_BUS_HZ = 100
POLICY_HZ = 50


def vertical_force_screen(mass_kg, flexion_deg, support_legs=2, multiplier=1.0):
    """Equal links, symmetric crouch, beta=0 straight; vertical force only.

    Wheel is directly beneath hip. Per-leg vertical reaction is mg/n.
    Knee lever arm is L sin(beta/2); hip ground-force moment is zero in
    this pose. Other poses require a separate hip moment calculation.
    """
    if mass_kg <= 0 or support_legs not in (1, 2) or multiplier <= 0:
        raise ValueError("positive mass/load and one or two supporting legs required")
    if not 0 <= flexion_deg < 180:
        raise ValueError("flexion must be in [0, 180) degrees")
    half_angle = math.radians(flexion_deg / 2.0)
    force_n = mass_kg * G * multiplier / support_legs
    lever_m = LINK_M * math.sin(half_angle)
    return {
        "vertical_force_n": force_n,
        "knee_lever_m": lever_m,
        "knee_torque_nm": force_n * lever_m,
        "hip_height_m": 2.0 * LINK_M * math.cos(half_angle) + WHEEL_DIAMETER_M / 2.0,
    }


def hip_vertical_force_moment(mass_kg, wheel_offset_m, support_legs=2):
    """Ground-force contribution only; signed horizontal wheel/hip offset."""
    if mass_kg <= 0 or support_legs not in (1, 2):
        raise ValueError("positive mass and one or two supporting legs required")
    return mass_kg * G / support_legs * wheel_offset_m


def wheel_speed_m_s(rpm, diameter_m=WHEEL_DIAMETER_M):
    return rpm * math.pi * diameter_m / 60.0


def budgets(data):
    """Exact decimal price sums; unquoted allowances are deliberately separate."""
    lines = data["baseline_bom"]
    core = sum((Decimal(line["unit_usd"]) * line["quantity"] for line in lines), Decimal("0"))
    allowances = data["budget_allowances_usd"]
    total = core + sum((Decimal(v) for v in allowances.values()), Decimal("0"))
    total += sum((Decimal(item["unit_usd"]) for item in data["power_reference"].values() if isinstance(item, dict)), Decimal("0"))
    sample_ids = {"joint_servo", "wheel_motor", "wheel_driver", "servo_adapter"}
    sample = sum((Decimal(line["unit_usd"]) for line in lines if line["id"] in sample_ids), Decimal("0"))
    return core, total, sample


def main():
    data = json.loads(INPUTS.read_text())
    servo = data["joint_servo"]
    wheel = data["wheel_motor"]
    rated_servo = servo["rated_kgf_cm"] * KG_CM_TO_NM
    reserve = rated_servo * STATIC_DERATING
    print("MINIATURE FEASIBILITY ONLY — no CAD/physical/thermal release")
    print(f"Source lookup: {data['lookup_date']}; some shop prices are indexed, not live checkout quotes.")
    print("\nPublished torque conversions at the specified 12 V:")
    print(f"joint rated {rated_servo:.6f} N·m; stall {servo['stall_kgf_cm'] * KG_CM_TO_NM:.6f} N·m")
    print(f"wheel rated {wheel['rated_kgf_cm'] * KG_CM_TO_NM:.6f} N·m; stall minimum {wheel['stall_min_kgf_cm'] * KG_CM_TO_NM:.6f} N·m")
    print(f"Planning static target = {STATIC_DERATING:.2f} × joint rated = {reserve:.6f} N·m (unvalidated)")
    print("\nEqual-link vertical-force screen; beta is knee flexion from straight:")
    print("mass kg | beta deg | knee N·m, two legs | hip height mm")
    for mass in (0.8, 1.0, 1.2, 1.5):
        for beta in (30, 90, 120):
            result = vertical_force_screen(mass, beta)
            print(f"{mass:.3f} | {beta:3d} | {result['knee_torque_nm']:.6f} | {result['hip_height_m'] * 1000:.3f}")
    base = vertical_force_screen(MASS_SCREEN_KG, 120)
    twice = vertical_force_screen(MASS_SCREEN_KG, 120, multiplier=2.0)
    one_leg = vertical_force_screen(MASS_SCREEN_KG, 120, support_legs=1)
    print(f"\n1.200 kg / beta 120: static {base['knee_torque_nm']:.6f}; 2× vertical load {twice['knee_torque_nm']:.6f}; single-leg support {one_leg['knee_torque_nm']:.6f} N·m")
    print(f"1.200 kg hip vertical-force moment at 40.000 mm wheel offset: {hip_vertical_force_moment(MASS_SCREEN_KG, HIP_WHEEL_OFFSET_M):.6f} N·m")
    max_mass = reserve * 2.0 / (G * LINK_M * math.sin(math.radians(60)))
    print(f"Static-only mass at planning target, beta 120, two legs: {max_mass:.6f} kg (not a payload rating)")
    print("\nWheel surface speeds for proposed 60.000 mm OD (no traction/acceleration proof):")
    for name, rpm in (("standard ST3215 no load", servo["no_load_rpm"]),
                      ("ST3215-HS no load", data["hs_servo"]["no_load_rpm"]),
                      ("DCGM rated point", wheel["rated_rpm"]),
                      ("DCGM no load", wheel["no_load_rpm"])):
        print(f"{name}: {rpm} rpm -> {wheel_speed_m_s(rpm):.6f} m/s")
    print("\nMass allocation, all unverified except nominal servo catalogue mass:")
    allocations = {
        "4 servo nominal masses": 4 * servo["mass_g"] / 1000.0,
        "2 wheel listing mass proxies; NET MASS UNKNOWN": 2 * wheel["listing_weight_kg"],
        "printed structures assumption": 0.160,
        "battery assumption": 0.100,
        "electronics/wire assumption": 0.080,
        "metal hardware assumption": 0.050,
    }
    for label, mass in allocations.items():
        print(f"{label}: {mass:.3f} kg")
    print(f"Total planning allocation: {sum(allocations.values()):.3f} kg")
    core, total, sample = budgets(data)
    print("\nBaseline product prices:")
    for line in data["baseline_bom"]:
        amount = Decimal(line["unit_usd"]) * line["quantity"]
        print(f"{line['quantity']} × {line['id']} @ ${line['unit_usd']} = ${amount:.2f}")
    print(f"Core ${core:.2f}; first sample set ${sample:.2f}")
    for label, amount in data["budget_allowances_usd"].items():
        print(f"UNQUOTED allowance, {label}: ${Decimal(amount):.2f}")
    battery = Decimal(data["power_reference"]["battery"]["unit_usd"])
    charger = Decimal(data["power_reference"]["charger"]["unit_usd"])
    print(f"Power price references: battery ${battery:.2f}, charger ${charger:.2f}; compatibility still to verify")
    print(f"Full-new reference basket with allowances ${total:.2f}")
    print(f"Reuse/borrow suitable charger: ${total - charger:.2f}; bench without pack/charger: ${total - charger - battery:.2f}")
    stall_a = 4 * servo["stall_a"] + 2 * wheel["stall_max_a"]
    print(f"\nCatalogue stall-current sum: {stall_a:.3f} A; servo-only {4 * servo['stall_a']:.3f} A")
    print("Not a supply recommendation: local limits and coordinated acceleration must be designed.")
    print(f"Proposed rates: local {LOCAL_LOOP_HZ} Hz / joint bus {JOINT_BUS_HZ} Hz / policy {POLICY_HZ} Hz; all timing UNVERIFIED")


if __name__ == "__main__":
    main()
