// Host test: g++ -std=c++17 -O2 -Wall -Wextra test_linkage.cpp -o /tmp/t && /tmp/t
#include <cstdio>
#include <cmath>
#include "r2a_knee_linkage.h"

using namespace beni::r2a;

int main() {
  int fail = 0;
  double worst = 0.0;
  for (int i = 0; i < kTableRows; ++i) {
    double a = kKneeMap[i].alpha_deg;
    double t = crankFromKnee(a);
    worst = fmax(worst, fabs(t - kKneeMap[i].theta_c_deg));
    // closure: crank pin to lever pin must be the rod length
    double d2r = M_PI / 180.0;
    double cx = kCrankMm * cos(t * d2r), cy = kCrankMm * sin(t * d2r);
    double px = kShoulderToKneeMm + kLeverMm * cos((a + kLeverOffsetDeg) * d2r);
    double py = kLeverMm * sin((a + kLeverOffsetDeg) * d2r);
    if (fabs(hypot(px - cx, py - cy) - kRodMm) > 1e-9) { ++fail; std::printf("closure %g\n", a); }
    double back = kneeFromCrank(t);
    if (fabs(back - a) > 1e-6) { ++fail; std::printf("inverse %g -> %g\n", a, back); }
  }
  if (worst > 1e-3) { ++fail; std::printf("table vs closed form %.6f deg\n", worst); }
  if (!(kSoftMinAlphaDeg > kFlexStopDeg + 1.9f && kSoftMaxAlphaDeg < kExtStopDeg - 1.9f)) {
    ++fail; std::printf("soft limits not outside the bumpers\n");
  }
  if (fabs(crankFromKnee(80.0) - 69.403) > 1e-3) { ++fail; std::printf("build pose %f\n", crankFromKnee(80.0)); }
  std::printf("%s: %d rows, max table error %.2e deg, theta_c(51)=%.3f theta_c(150)=%.3f\n",
              fail ? "FAIL" : "PASS", kTableRows, worst, crankFromKnee(51.0), crankFromKnee(150.0));
  return fail ? 1 : 0;
}
