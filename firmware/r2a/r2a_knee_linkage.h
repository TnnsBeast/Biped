// R2A knee linkage map, joint limits and CAN node plan (single-leg rig).
//
// Header-only and hardware-free: nothing here commands an actuator.  Numbers
// trace to r2a_calc.py (linkage), the Fusion digital gate
// (evidence/r2a/2026-09-27_digital_gate/fusion_measurements.json: stop contact
// angles) and electronics/03_compute_and_can.md §1.3 (CANSimple IDs).
//
// Conventions: alpha is the interior knee angle (legacy phi = 80 - alpha).
// theta_c is the crank angle about the shoulder axis, measured from the
// shoulder->knee line in the proximal-link frame, positive away from the
// folding distal link.  Both are in degrees.  The crank turns WITH alpha
// (dtheta_c/dalpha = N, 0.86..0.94), and the map has no shoulder term: the knee
// actuator's stator rides on the proximal link.
#pragma once

#include <math.h>
#include <stdint.h>

#include "r2a_knee_linkage_table.h"

namespace beni::r2a {

// --- linkage (r2a_calc.py selection; the Fusion model is built on it)
constexpr double kShoulderToKneeMm = 120.0;
constexpr double kCrankMm = 32.0;
constexpr double kRodMm = 120.0;
constexpr double kLeverMm = 30.0;
constexpr double kLeverOffsetDeg = -12.0;   // theta_lever = alpha - 12

// --- stops: rigid radial faces, Fusion-measured contact (bisected to 0.01 deg)
constexpr float kFlexStopDeg = 51.0f;
constexpr float kExtStopDeg = 150.0f;
// TPU bumpers engage about 1.9 deg before each rigid stop (1.0 mm protrusion
// at R30).  Software limits stay outside the bumpers with 1 deg to spare.
constexpr float kSoftMinAlphaDeg = 54.0f;
constexpr float kSoftMaxAlphaDeg = 147.0f;

// Closed-form four-bar (same formula and branch as r2a_calc.solve_linkage).
inline double crankFromKnee(double alpha_deg) {
  const double d2r = M_PI / 180.0;
  const double th_l = (alpha_deg + kLeverOffsetDeg) * d2r;
  const double px = kShoulderToKneeMm + kLeverMm * cos(th_l);
  const double py = kLeverMm * sin(th_l);
  const double dd = hypot(px, py);
  const double cg = (kCrankMm * kCrankMm + dd * dd - kRodMm * kRodMm) / (2.0 * kCrankMm * dd);
  if (cg > 1.0 || cg < -1.0) return NAN;   // linkage cannot assemble
  return (atan2(py, px) + acos(cg)) / d2r;
}

// Table lookup with linear interpolation (for a loop that avoids trig).
inline float crankFromKneeTable(float alpha_deg) {
  float x = (alpha_deg - kTableAlpha0Deg) / kTableStepDeg;
  if (x < 0.0f || x > float(kTableRows - 1)) return NAN;
  int i = int(x);
  if (i == kTableRows - 1) return kKneeMap[i].theta_c_deg;
  float f = x - float(i);
  return kKneeMap[i].theta_c_deg + f * (kKneeMap[i + 1].theta_c_deg - kKneeMap[i].theta_c_deg);
}

// Inverse by bisection on the monotonic map (theta_c rises with alpha).
inline double kneeFromCrank(double theta_c_deg) {
  double lo = kTableAlpha0Deg, hi = kTableAlpha0Deg + kTableStepDeg * (kTableRows - 1);
  if (theta_c_deg < crankFromKnee(lo) || theta_c_deg > crankFromKnee(hi)) return NAN;
  for (int k = 0; k < 60; ++k) {
    double mid = 0.5 * (lo + hi);
    if (crankFromKnee(mid) < theta_c_deg) lo = mid; else hi = mid;
  }
  return 0.5 * (lo + hi);
}

// Knee torque -> crank torque through the ratio N = dtheta_c/dalpha (lossless;
// r2a_calc.py uses eta = 0.95 for its planning figures).
inline float crankTorqueFromKnee(float knee_nm, float alpha_deg) {
  float x = (alpha_deg - kTableAlpha0Deg) / kTableStepDeg;
  if (x < 0.0f || x > float(kTableRows - 1)) return NAN;
  int i = int(x);
  if (i >= kTableRows - 1) i = kTableRows - 2;
  float f = x - float(i);
  float n = kKneeMap[i].ratio_n + f * (kKneeMap[i + 1].ratio_n - kKneeMap[i].ratio_n);
  return knee_nm / n;
}

inline bool kneeWithinSoftLimits(float alpha_deg) {
  return alpha_deg >= kSoftMinAlphaDeg && alpha_deg <= kSoftMaxAlphaDeg;
}

// --- CAN plan (electronics/03 §1.3: CAN_ID = (node_id << 5) | cmd_id)
constexpr uint8_t kShoulderNode = 0;   // factory default, unchanged
constexpr uint8_t kKneeNode = 1;       // set BEFORE the knee unit joins bus A
constexpr uint16_t canId(uint8_t node, uint8_t cmd) { return uint16_t((node << 5) | cmd); }
constexpr uint8_t kCmdHeartbeat = 0x001;
constexpr uint8_t kCmdEstop = 0x002;
constexpr uint8_t kCmdSetAxisNodeId = 0x006;
constexpr uint8_t kCmdGetEncoderEstimates = 0x009;
constexpr uint8_t kCmdSetInputTorque = 0x00E;
constexpr uint8_t kCmdClearErrors = 0x018;
constexpr uint8_t kCmdSaveConfiguration = 0x01F;
static_assert(canId(kKneeNode, kCmdHeartbeat) == 0x021, "knee heartbeat ID");
static_assert(canId(kShoulderNode, kCmdHeartbeat) == 0x001, "shoulder heartbeat ID");

}  // namespace beni::r2a
