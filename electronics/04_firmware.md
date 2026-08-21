# 04 — Control and Firmware Architecture

Covers brief §10 deliverable **8**. Numbers below are computed from
`sim/beni.urdf` and `sim/beni_inertia.json`, not from the brief. Where they
disagree with the brief, the brief is wrong and it is flagged.

## 1. Six corrections to the brief

| # | Brief says | Model says |
|---|---|---|
| 1 | Unstable pole 9.7 rad/s, τ = 103 ms | **11.18 rad/s, τ = 89 ms.** The LIPM formula drops body pitch inertia and the wheel reaction torque. You are 15% more urgent than you thought. |
| 2 | — | **RHP zero at +6.53 rad/s in x/τ.** Velocity-loop bandwidth is hard-capped near **3.2 rad/s (0.5 Hz)**, whatever you tune. |
| 3 | 100 mm drop = 3.23 J vs 3.553 J, "~10% margin" | **A 100 mm free drop bottoms out.** The brief omits gravity work during the 50 mm of compression. True demand 4.85 J vs 3.55 J available. **Passive free-drop capacity is ~49 mm for the two-leg robot's 1-DOF model** (spring-rate method, more conservative than the ~60 mm energy method — see `fusion_brief_single_leg_rig.md` §4.3). **For the single-leg rig the 2-DOF reality is tighter: 45 mm planning limit, +24° crossed at 46.3 mm** — see `beni_single_leg_rig_design_record.md` §3. |
| 4 | — | **Leg bounce mode at 3.67 Hz = 23.0 rad/s, only 2.06× the balance pole.** No timescale separation; the balance loop will excite it. |
| 5 | Shoulders raise and lower the body | **dRide/dθ_s = 0 at θ_s = 0.** `ride = 154.269·cos θ_s` — the nominal pose is a stationary point with *zero* height authority. |
| 6 | The knee encoder is your force sensor | True and excellent (0.025 N/leg), **but a free leg reads 8.25 N against the preload.** Below 0.52 g everything looks identical. Threshold on angle, not force. |

Correction 3 invalidates the brief's own test gate ("no powered jump until a
100 mm drop never reaches +27°"). That gate cannot be passed passively — see
`06_logging_and_bringup.md` Stage 5.

## 2. The plant

Planar, wheels lumped, `q = [x, θ]`, `u = τ` (total wheel torque). Keep the
`−τ` reaction term in the pitch equation — most hobby derivations drop it, and
the resulting gains do not work on hardware.

```
m_b = 2.871967 kg   I_b = 0.019158   l = 0.118800 m
m_w = 0.418181 kg   I_w = 0.000749   I_w/r² = 0.2476 kg  (7.5% of mass — keep it)

      ⎡0  1     0        0⎤        ⎡    0    ⎤
A  =  ⎢0  0  −12.0510    0⎥   B  = ⎢  15.0533⎥
      ⎢0  0     0        1⎥        ⎢    0    ⎥
      ⎣0  0  124.9553    0⎦        ⎣−102.7957⎦

poles {0, 0, ±11.1783}      x/τ zeros {±6.5316}      θ/τ zeros {0, 0}
```

Anchors: gravity restoring torque 3.347 N·m/rad; 0.181 N·m of total wheel
torque per 1 m/s² of body acceleration; **a >40° static lean is holdable.
Torque is not the scarce resource — bandwidth, latency and pitch bias are.**

## 3. Balance controller

**Cascaded, not unified.** With 4 actuators and no redundancy there is no null
space for WBC to exploit, and you will crash this robot dozens of times.

```
 v_d  ──► [4-state LQR K(h), 1 kHz] ──► τ_bal ─┐
 ψ̇_d  ──► [yaw PD, 500 Hz]          ──► τ_yaw ─┴─► τ_L, τ_R   (balance priority)
 h_d  ──► [height PI, 10 Hz] ─┐
 roll ──► [roll PD, 10 Hz]    ├─► VMC: τ_sh = Jᵀ F  + spring damping
 φ̇    ──► [damping injection] ┘
```

**Wheels do balance and yaw. Shoulders do posture, height, roll, spring damping
and jumping.** Shoulder torque reaches the body *through* the 3.67 Hz spring,
so it is a slow channel, and you will never saturate the wheels.

### 3.1 Starting gains

Total wheel torque [N·m] from `[x (m), ẋ (m/s), θ (rad), θ̇ (rad/s)]`. Halve
per motor. **Delay margin is the design driver, not performance.**

| set | K | delay margin @1 kHz |
|---|---|---|
| Aggressive | `[−8.000, −8.311, −26.625, −3.273]` | 6 ms |
| Moderate | `[−1.000, −3.120, −16.007, −1.841]` | 10 ms |
| **Soft — start here** | **`[−0.354, −1.483, −9.596, −1.061]`** | **16 ms** |
| Very soft — first light | `[−0.500, −1.422, −7.592, −0.855]` | 20 ms |

`K_θ` moves only −7.6 → −26.6 across a huge Q/R range: the pitch gain is set by
the plant, not by you. What Q actually tunes is the velocity loop, which the
RHP zero caps anyway. **Do not agonise over Q/R.** Rate-limit the operator's
velocity command to ~0.5 Hz or the reference will fight the loop.

At 1 kHz the discrete gains are within 3% of continuous — use continuous. At
200 Hz they are 17% off, which is one more reason to run 1 kHz.

### 3.2 Gain scheduling: implement it, expect 3%

`K_θ` varies **1.0%** over the useful shoulder range (4.8% over the full ±50°),
`K_ẋ` 9.7%, `K_x` not at all. Ride height is at a *maximum* at θ_s = 0, so it
is second-order there. Quadratic fits (h in metres):

```
K_ẋ = −89.1729·h² + 37.2836·h − 11.9322     (max err 0.83%)
K_θ = −10.5489·h² − 20.8889·h − 23.1757     (max err 0.61%)
K_θ̇ = −38.8845·h² +  5.1456·h −  3.1490     (max err 1.41%)
```

12 multiply-adds. Worth having, will not fix anything. **Reflected rotor
inertia matters more:** `N²·J_rotor` shifts `K_ẋ` by up to 13%. Get the real
GIM4305-10 rotor inertia and fold it into `I_w` before touching the schedule.

### 3.3 The bounce mode is the biggest control risk

```
ω_hop = √(1747/3.290) = 23.05 rad/s = 3.67 Hz
balance pole                        = 11.18 rad/s      ratio 2.06
```

The rule of thumb wants ≥3–4×. A bare steel cartridge spring has ζ ≈ 0.01.
**Expect a 3–4 Hz vertical bob that grows as you raise K_θ.** The spring is
fixed hardware, so the fix is active:

```
c_crit   = 2√(k·m) = 151.6 N·s/m
ζ = 0.3  ⇒ 45.5 N·s/m total ⇒ c_φ = 0.192 N·m·s/rad per leg
```

```c
/* shoulder damping injection, 1 kHz */
float phi_dot = diff_lp(phi_meas, 60.0f);   /* 60 Hz LPF differentiator */
tau_sh += -C_PHI * phi_dot * dphi_dtheta(theta_s);
```

**But `dRide/dθ_s = 0` at θ_s = 0, so the shoulder has zero damping authority
at the nominal pose.** Bias the standing pose to θ_s ≈ ±10–15° where
`|dRide/dθ| ≈ 0.027–0.040 m/rad`. Notching the wheel torque at 3.7 Hz is a
band-aid that eats delay margin; use it last.

## 4. The passive knee

Treat it as **measured kinematics**, never as a disturbance to reject — the
ATRIAS/Cassie posture. It enters the design in exactly four places: the
scheduling variable `h(θ_s, φ)`, the damping injection above, the landing
energy budget, and contact detection.

Firmware polynomial (φ in rad, max error 0.0025 N·m over the full range):

```c
/* tau_knee(phi) [N.m], valid -0.1396 .. +0.4712 rad */
static inline float tau_knee(float p){
    return ((-0.6221f*p + 6.4019f)*p + 7.3916f)*p + 1.5706f;
}
```

Contact thresholds — **on angle, not force** (correction 6):

```c
#define PHI_STOP     (-8.000f*DEG)   /* free leg rests here, reads 8.25 N */
#define PHI_TD_ON    (-6.164f*DEG)   /* ~0.63 g */
#define PHI_TD_OFF   (-7.200f*DEG)   /* Schmitt hysteresis */
#define PHI_STATIC   (-0.835f*DEG)   /* 1 g reference */
#define PHI_SOFT_LIM (+22.0f *DEG)   /* CBF activation */
#define PHI_HARDSTOP (+27.0f *DEG)   /* metal */
```

Low-pass φ at 50 Hz before thresholding, add a 3-sample debounce, and subtract
`m_shank·z̈` during fast swings. **Spring for the contact decision, IMU
band-pass 30–200 Hz for the contact timestamp** — the spring lags the impact.

Also add an integrator state to the LQR (`x_aug = [x, ẋ, θ, θ̇, ∫θ]`) to soak
up static preload mismatch and the standing CoM trim. One state, cheap,
robust.

## 5. State estimation

**A 1° pitch bias commands 0.167 N·m and accelerates the robot at 0.92 m/s².**
Everything below serves one requirement: **pitch bias <0.1°, noise <0.05° RMS.**
A 0.1°/s gyro bias integrates to 1° in 10 s, so **gyro bias must be a state.**

**Use a 2-state pitch KF `[θ, b_g]`**, not Madgwick (≈10 ms group delay at
100 Hz — it eats the whole delay margin) and not Mahony (solves a 3-D problem
you don't have).

```
x_{k+1} = [1 −dt; 0 1]·x_k + [dt; 0]·ω_m
z_k = θ_accel,  H = [1 0],  R = σ_a²  (adaptive)
σ_g ≈ 0.004 rad/s/√Hz,  σ_bg ≈ 1e−5,  σ_a = 0.05 rad nominal,
inflated to 0.5 rad when | |a| − g | > 1 m/s²
```

### 5.1 The accelerometer-tilt trap — the highest-value five lines in the stack

`atan2(−a_x, a_z)` is only valid when the robot is not accelerating, and a
balancing robot always is. **At 1 m/s² you get 5.8° of tilt error — 58× the
budget.** This, not the lever arm, is the dominant estimator error.

```c
float a_hat_x   = A12*theta_hat + B2*tau_total;   /* A12=-12.0510, B2=15.0533 */
float theta_acc = atan2f(-(a_corr_x - a_hat_x), a_corr_z);
```

Model-predicted, so no lag and no wheel-slip contamination.

### 5.2 Wheel odometry has a shank term

The wheel motor's parent link is the **shank**, so the encoder is
shank-referenced:

```
v_ground = r·(φ̇_enc + θ̇_shank),   θ_shank = θ_body + θ_shoulder + f(φ_knee)
```

Omitting `r·θ̇_shank` is one of the most common wheeled-biped bugs: at
θ̇ = 1 rad/s it is 0.055 m/s, it is *correlated with pitch motion*, and it
produces a limit cycle. Diagnostic: chock the wheel and pitch the robot by
hand — if the count changes, you need the term.

The LQR's `ẋ` is **wheel-axle** velocity, not CoM velocity
(`v_CoM = v_axle + h·θ̇`).

**Slip detection**, OR all four: chi-square innovation gate (NIS > 6.63);
left/right disagreement against `b·ψ̇_gyro`; torque/acceleration consistency;
and — cheapest and most decisive — **if φ is at the −8° stop the leg is
airborne, so discard its odometry.**

## 6. Jump and landing

### 6.1 Use a scissor crouch

Because `ride = 154.269·cos θ_s` is **even** in θ_s, left = +θ and right = −θ
give identical ride height. That buys: exact cancellation of the 77 mm of
fore-aft wheel travel, pure vertical thrust, a 154 mm virtual wheelbase (so the
crouched stance is statically stable in pitch), and **non-zero dRide/dθ at both
shoulders**, which restores height, damping and CBF authority. This turns
correction 5 from a blocker into a non-issue. Crouch to **±25…±35°**.

### 6.2 Realistic jump target

From a 30° scissor crouch (20.7 mm of stroke) at ~7 N·m peak, discounting the
ideal work by 40–50% for torque droop, wheel spin-up and inefficiency:
**a 100 mm apex is a realistic v1 target.** Thrust is ~30–40° in 60–80 ms,
6.5–8.7 rad/s at the shoulder, ~150 W total mechanical.

### 6.3 Flight: the legs are the reaction mass, not the wheels

```
ξ_wheels = I_w / I_body   = 0.000749 / 0.025079 = 0.0299   →  33.5 : 1
ξ_legs   = 0.03058 / 0.033155                   = 0.922
```

A 20° pitch correction on the wheels alone needs **372 rpm sustained over a
300 ms flight**, and you land with 1.07 m/s of unwanted ground speed. Use
**shoulder position (both legs same direction, ξ = 0.92) as the primary
authority** and the wheels only for the last few degrees. **Despin the wheels
to the expected touchdown ground speed before landing.**

Angular momentum is conserved in flight — **you cannot change L, only
redistribute it. Get it right at takeoff.** Takeoff `|θ̇| < 1 rad/s` is the
single most important jump metric.

### 6.4 State machine

```
IDLE → BALANCE → CROUCH → THRUST → FLIGHT → DESCEND → LAND → RECOVER → BALANCE
                    ▲                                            │
                    └──────────────── abort ◄────────────────────┘
```

| state | actions | exit | abort |
|---|---|---|---|
| CROUCH | scissor to ±30° over 250 ms (slow, springs quasi-static) | within 2° of target | 400 ms timeout |
| THRUST | torque ramp to τ_max in 10 ms; wheel velocity feedforward `ẋ_wheel(θ_s)/r`; **CBF active** | both legs unloaded | φ > 24°, or θ error > 15° |
| FLIGHT | freeze L; leg-reaction pitch nulling; despin wheels; extend toward θ_s ≈ 0 | apex, or 60% of predicted flight time | attitude error > 40° → brace |
| DESCEND | landing pose, shoulders **torque mode**, low stiffness, gravity feedforward | either leg φ > PHI_TD_ON | — |
| LAND | impedance: `τ_sh = K_sh(θ_ref−θ) − C_sh·θ̇_sh`, K_sh low, C_sh high; ref sweeps toward crouch | φ̇ < 0 both legs and \|v_z\| < 0.1 | φ > 25° → max yield |
| RECOVER | blend to BALANCE gains over 200 ms, damp the bounce mode hard | \|θ\| < 5° for 100 ms | fall → SAFE |

The RECOVER blend matters — switching from a compliant landing law straight to
a stiff LQR kicks the bounce mode.

### 6.5 Landing energy — the shoulders are not optional

With a 3° stop margin (limit φ to +24°) the knees hold **2.917 J**:

| drop | v_td | total E | knees | **shoulders must absorb** | per shoulder |
|---|---|---:|---:|---:|---:|
| 100 mm | 1.40 m/s | 4.65 J | 2.92 J | **1.73 J** | 0.87 J |
| 150 mm | 1.72 m/s | 6.26 J | 2.92 J | **3.35 J** | 1.67 J |
| 200 mm | 1.98 m/s | 7.88 J | 2.92 J | **4.96 J** | 2.48 J |

At 40° of shoulder sweep, absorbing 1.73 J needs ~1.2 N·m per shoulder — well
inside the GIM6010-8. **But only if stroke is available**, which means landing
from an *extended* pose and yielding into a crouch. **Landing pose rule:
extend to θ_s ≈ +5…10° during descent, then yield.** (Not exactly 0°, or the
CBF has no authority — see below.)

### 6.6 Hard-stop avoidance

The knee is unactuated, so you cannot command φ; you can only remove the energy
that would drive it to the stop. Velocity-limit curve (a discrete CBF):

```c
#define PHI_MAX  (24.0f*DEG)     /* 3° to the bumper, 3° more to metal */
#define A_MAX    (60.0f)         /* rad/s², tune from Stage-5 drops */

float h = PHI_MAX - phi;
float phid_lim = (h > 0.0f) ? sqrtf(2.0f*A_MAX*h) : 0.0f;
if (phi_dot > phid_lim) {
    float excess  = phi_dot - phid_lim;
    float dz_dphi = jac_knee_z(phi);            /* 0.092..0.116 m/rad */
    float dz_dth  = -0.154269f*sinf(theta_s);   /* ZERO at theta_s = 0 */
    if (fabsf(dz_dth) > 0.01f) tau_sh += -CBF_GAIN*excess*(dz_dphi/dz_dth);
    else                       emergency_extend();
}
```

Note the `dz_dth ≈ 0` branch — the third place the stationary point bites.
Layered protection: planner never commands a jump outside the measured
envelope → CBF at 1 kHz → φ > 25° maximum yield → φ > 26° log a fault →
mechanical bumper at +20°, metal at +27°.

## 7. Software stack

**FreeRTOS, with the 1 kHz control loop as a hardware-timer ISR outside the
scheduler.** Bare-metal superloop collapses once you add SD logging, telemetry
and a CLI. Zephyr only if you already know it. **micro-ROS on the MCU: no** —
non-deterministic latency inside a 16 ms budget.

| Prio | Task | Rate | Notes |
|---|---|---|---|
| ISR | `control_isr` | 1 kHz | Timer ISR, target <200 µs. Nothing that can block. |
| 6 | `can_rx` | event | Drain FIFO to mailboxes; no parsing in ISR |
| 4 | `state_machine` | 500 Hz | Jump FSM |
| 3 | `logger` | 200 Hz | Binary frames → ring buffer |
| 2 | `sd_writer` | ~10 Hz | 4 kB block flushes |
| 1 | `telemetry_tx` | 50 Hz | UDP/USB, decimated, droppable |

Rules: **torque mode always** — never the drive's internal position mode past
the encoder-check stage. **Kick the watchdog from the control ISR only, and
only after verifying the estimator produced a finite result** — a watchdog
kicked from idle proves nothing. Log ISR worst-case execution time every second
via the DWT cycle counter.

**Latency budget: 16 ms of margin with the soft gains, and you must measure it,
not hope.** Timestamp at IMU-sample-complete and at torque-written-to-mailbox.
Target <8 ms end-to-end. Nothing else in this document matters if you blow it.

## 8. Simulation

**MuJoCo primary** (best impact contact model, spatial tendons give the exact
geometric moment arm for free), PyBullet for quick checks, Drake for
linearisation and LQR synthesis. Model the spring as a **spatial tendon**
between sites at Ru = 36 mm and Rl = 54 mm with `stiffness=10450`,
`springlength = e2e(−8°) − F₀/k = 0.06483 m` — MuJoCo then reproduces
`Ru·Rl·sin(110°−φ)/e2e(φ)` automatically.

Settings that matter: `timestep=0.0005` (you have a 20 ms impact),
`cone="elliptic" impratio="10"` (default pyramidal friction makes wheels slip
unrealistically), and **`armature = N²·J_rotor` on every actuated joint** —
64× and 100× the rotor inertia, and the #1 sim-to-real gap for geared drives.

In PyBullet, revolute joints ship with a velocity motor at `maxForce=100`, so a
"passive" knee is silently locked. Explicitly
`setJointMotorControl2(..., VELOCITY_CONTROL, force=0)` and load with
`URDF_USE_INERTIA_FROM_FILE`.

**Model-based, not RL.** You have 4 actuators and a 4-state balance problem
that LQR solves exactly; RL would spend a million steps rediscovering a gain
matrix computable in 50 ms, and it amplifies a sim-to-real gap you have not yet
measured. RL earns its keep later, on the jump trajectory and on fall recovery,
as an *addition* to a working classical stack.

## 9. Calibration and homing

1. **Actuator encoder calibration** — GIM6010-8 needs a one-time forward/reverse
   sweep saved to flash (`0x01F`). Encoder is mono-turn; assume no retention
   across power cycles until proven.
2. **Shoulder zero** — mechanical index against a printed jig. Store the offset
   in the main board's flash, not the driver's, so a driver swap keeps it.
3. **Knee zero** — drive to the −8° stop, record the raw count. Verify
   monotonic over −8°…+27° (BOM step B16).
4. **IMU bias** — 10 s stationary gyro average every boot; accel bias and
   six-face alignment once.
5. **Spring characterisation** — measure `F₀` and `k` in situ. **Do not assume
   30.0 N**; preload is shim-dependent and every threshold in §4 and every row
   in §6.5 scales with it.
6. **Kt verification** on a lever arm — see `03_compute_and_can.md` §1.4.

## 10. Reading list

`arXiv:2407.21500` (DIABLO — closest published architecture: LQR + complementary
filter + separate height/roll/yaw loops) · `arXiv:2005.11435` (Ascento ICRA'19 —
the WIP derivation done correctly, with the reaction term) · Klemm RA-L 2020,
DOI 10.1109/LRA.2020.2979625 (why LQR sits *inside* WBC rather than being
replaced by it) · `github.com/upkie/upkie` (working stack on comparable
CAN-actuator hardware) · `github.com/Skythinker616/foc-wheel-legged-robot`
(most complete open wheel-legged reference) · `arXiv:1904.09251` +
`github.com/RossHartley/invariant-ekf` (contact-aided InEKF, if you outgrow the
2-state KF) · Cassie state estimation, `github.com/UMich-BipedLab/Cassie_StateEstimation`
(springs modelled explicitly in the estimator — your exact problem).
