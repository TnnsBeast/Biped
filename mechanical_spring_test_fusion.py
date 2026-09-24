"""Controlled ABS mechanical spring-test article for ``Beni_SingleLegRig``.

All functions in this file are run through the Fusion MCP.  The article adapts
the owned OD18 / ID9 / 50 mm die spring for an unpowered, supported hand test.
It deliberately starts at essentially zero compression at the -8 degree
extension stop and limits the test to +15 degrees.  It is not a spring-rate,
structural, powered-motion, traction, proof, drop, or human-adjacent release.
"""

from collections import Counter
import hashlib
import json
import math
import os
import struct

import adsk.core
import adsk.fusion

import beni_lib as B
import rig_lib as R
import rig_export as E


ROOT = os.path.dirname(os.path.realpath(__file__))
OUT_DIR = os.path.join(ROOT, 'first_article_stl', 'mechanical_spring_test')
EVIDENCE_DIR = os.path.join(
    ROOT, 'evidence', 'assembly', '2026-09-17_abs_spring_mechanical_test')

UPPER = 'ABS_TEST_Cart_Upper_Eye_50mm'
LOWER = 'ABS_TEST_Cart_Lower_Eye_50mm'
GUIDE = 'ABS_TEST_Cart_Guide_Bar_50mm'
STOP = 'ABS_TEST_Knee_Stop_Plate_15deg'
SPACER = 'ABS_TEST_Knee_Pin_Outboard_Spacer'
RIM = 'ABS_TEST_Wheel_Rim_NoTyre'
# Modelled in the rig but not in the unpowered ABS article: the structural
# cartridge, stop, encoder and wheel beside their ABS_TEST_* substitutes, the
# unreleased collar envelope, the floor plate and step-2 fixtures, and anything
# the rig conversion removes (rig_lib.RIG_REMOVED).
NOT_IN_ABS_ARTICLE = frozenset((
    'Cart_Upper_Eye_L', 'Cart_Lower_Eye_L', 'Cart_Guide_Rod_L',
    'Cart_Preload_Shim_L', 'Knee_Spring_L', 'RIG_Knee_Stop_Plate_L',
    'HW_WasherStack_M5', 'RIG_Knee_Bumper_Tube_L', 'RIG_Knee_Magnet_Carrier_L',
    'Wheel_Rim_L', 'Wheel_Tyre_L', 'RIG_Knee_Collar_L', 'Knee_Encoder_PCB_L',
    'HW_Magnet_D6x2p5_Diametric', 'RIG_Floor_Plate')
    + R.STEP2_FIXTURES + R.RIG_REMOVED)
SPRING_REF = 'REFERENCE_Owned_Spring_Envelope_OD18_ID9_L50'

OWNED_SPRING_OD = 18.0
OWNED_SPRING_ID = 9.0
OWNED_SPRING_FREE = 50.0
SPRING_PILOT_D = 8.0       # physically passed on both detached caps
SPRING_PILOT_UP_L = 4.0
SPRING_PILOT_LO_L = 6.0

TEST_PHI_EXT = -8.0
TEST_PHI_FLEX = 15.0
UPPER_SEAT_S = 11.0        # frozen upper pivot-to-seat datum
TEST_DEAD = B.cart_len(TEST_PHI_EXT) - OWNED_SPRING_FREE
LOWER_PIVOT_TO_SEAT = TEST_DEAD - UPPER_SEAT_S

GUIDE_SOCKET_D = 6.0       # 0.626 mm diametral room around the bar diagonal
GUIDE_BAR_SIDE = 3.8       # 5.374 mm diagonal inside the 6.0 mm guide bores
GUIDE_BAR_S0 = 4.8
GUIDE_BAR_S1 = 60.5
LOWER_GUIDE_END_FROM_PIVOT = 4.0

PIVOT_BORE_D = 4.4         # test clearance for the nominal 4 mm clevis pins
PIN_END_Y = R.AXLE_Y0 + R.PIN_LEN
SPACER_Y0 = PIN_END_Y + 0.3
SPACER_Y1 = 99.4           # 0.5 mm before the encoder bracket plate
SPACER_OD = 15.0
SPACER_LOCATOR_D = 7.6
SPACER_LOCATOR_Y1 = 101.4


def _bodies(comp):
    return [comp.bRepBodies.item(i) for i in range(comp.bRepBodies.count)]


def _poly(comp, y, points, op='new'):
    sk = B.sk_on_y(comp, y)
    B.polyline(sk, points)
    return B.extrude(comp, sk.profiles.item(0), 1.0, op=op,
                     participants=_bodies(comp) if op in ('cut', 'inter') else None)


def _cart_geometry():
    length = B.cart_len(0.0)
    direction = ((B.LX - B.UX) / length, (B.LZ - B.UZ) / length)
    normal = (-direction[1], direction[0])

    def point(s, radius=0.0):
        return (B.UX + s * direction[0] + radius * normal[0],
                B.UZ + s * direction[1] + radius * normal[1])

    return length, direction, normal, point


def _revolved_ring(comp, point, length, s0, s1, r_in, r_out, op='new'):
    sk = B.sk_on_y(comp, B.LEG_Y_MID)
    axis = sk.sketchCurves.sketchLines.addByTwoPoints(
        B.sxz(*point(-25.0, 0.0)), B.sxz(*point(length + 25.0, 0.0)))
    axis.isConstruction = True
    corners = [point(s0, r_in), point(s1, r_in),
               point(s1, r_out), point(s0, r_out)]
    lines = sk.sketchCurves.sketchLines
    for index in range(4):
        lines.addByTwoPoints(B.sxz(*corners[index]),
                             B.sxz(*corners[(index + 1) % 4]))
    return B.revolve(comp, B.biggest_profile(sk), axis, 360.0, op)


def _cart_rect(comp, point, y0, s0, s1, width, thickness, op):
    sk = B.sk_on_y(comp, y0)
    corners = [point(s0, -width / 2.0), point(s1, -width / 2.0),
               point(s1, width / 2.0), point(s0, width / 2.0)]
    B.polyline(sk, corners)
    return B.extrude(comp, B.biggest_profile(sk), thickness, op,
                     participants=_bodies(comp) if op in ('cut', 'inter') else None)


def _cut_printable_pivot(comp, point, center_s, apex_direction, y0):
    """Cut a horizontal-pin hole with a self-supporting pointed roof."""
    radius = PIVOT_BORE_D / 2.0
    sk = B.sk_on_y(comp, y0 - 1.0)
    center = point(center_s, 0.0)
    B.circle(sk, center[0], center[1], PIVOT_BORE_D)
    B.polyline(sk, [point(center_s, -radius),
                    point(center_s + apex_direction * 2.0 * radius, 0.0),
                    point(center_s, radius)])
    B.extrude(comp, B.profiles(sk), 21.0, 'cut',
              participants=_bodies(comp))


def _build_upper():
    length, _direction, _normal, point = _cart_geometry()
    y0 = B.LEG_Y_MID - 9.5
    B.drop_comp(UPPER)
    occ = B.new_comp(UPPER)
    comp = occ.component
    sk = B.sk_on_y(comp, y0)
    a, b = point(0.0), point(2.0)
    B.slot(sk, a[0], a[1], b[0], b[1], 13.0)
    B.extrude(comp, B.biggest_profile(sk), 19.0, 'new')
    # A 45-degree width transition avoids the unsupported 3.5 mm ledge in the
    # original eye when the cartridge axis is printed vertically.
    sk = B.sk_on_y(comp, y0)
    B.polyline(sk, [point(2.0, -6.5), point(5.5, -10.0),
                    point(UPPER_SEAT_S, -10.0),
                    point(UPPER_SEAT_S, 10.0), point(5.5, 10.0),
                    point(2.0, 6.5)])
    B.extrude(comp, B.biggest_profile(sk), 19.0, 'join')
    _revolved_ring(comp, point, length, UPPER_SEAT_S,
                   UPPER_SEAT_S + SPRING_PILOT_UP_L,
                   0.0, SPRING_PILOT_D / 2.0, 'join')
    _revolved_ring(comp, point, length, GUIDE_BAR_S0 - 0.2,
                   UPPER_SEAT_S + SPRING_PILOT_UP_L + 0.2,
                   0.0, GUIDE_SOCKET_D / 2.0, 'cut')
    _cut_printable_pivot(comp, point, 0.0, 1.0, y0)
    # Clip the rounded tip to an exact 5 x 19 mm bed plane at s = -6.0.
    _cart_rect(comp, point, y0 - 1.0, -25.0, -6.0, 30.0, 21.0, 'cut')
    comp.bRepBodies.item(0).name = UPPER
    return occ


def _build_lower():
    length, _direction, _normal, point = _cart_geometry()
    lower_seat = length - LOWER_PIVOT_TO_SEAT
    y0 = B.LEG_Y_MID - 9.5
    B.drop_comp(LOWER)
    occ = B.new_comp(LOWER)
    comp = occ.component
    sk = B.sk_on_y(comp, y0)
    a, b = point(length), point(length - 2.0)
    B.slot(sk, a[0], a[1], b[0], b[1], 13.0)
    B.extrude(comp, B.biggest_profile(sk), 19.0, 'new')
    sk = B.sk_on_y(comp, y0)
    B.polyline(sk, [point(lower_seat, -10.0),
                    point(length - 5.5, -10.0),
                    point(length - 2.0, -6.5),
                    point(length - 2.0, 6.5),
                    point(length - 5.5, 10.0),
                    point(lower_seat, 10.0)])
    B.extrude(comp, B.biggest_profile(sk), 19.0, 'join')
    _revolved_ring(comp, point, length,
                   lower_seat - SPRING_PILOT_LO_L, lower_seat,
                   0.0, SPRING_PILOT_D / 2.0, 'join')
    _revolved_ring(comp, point, length,
                   lower_seat - SPRING_PILOT_LO_L - 0.5,
                   length - LOWER_GUIDE_END_FROM_PIVOT,
                   0.0, GUIDE_SOCKET_D / 2.0, 'cut')
    _cut_printable_pivot(comp, point, length, -1.0, y0)
    # This is the lower eye's bed plane when -cartridge-axis prints upward.
    _cart_rect(comp, point, y0 - 1.0, length + 6.0, length + 25.0,
               30.0, 21.0, 'cut')
    comp.bRepBodies.item(0).name = LOWER
    return occ


def _build_guide():
    _length, _direction, _normal, point = _cart_geometry()
    B.drop_comp(GUIDE)
    occ = B.new_comp(GUIDE)
    comp = occ.component
    _cart_rect(comp, point, B.LEG_Y_MID - GUIDE_BAR_SIDE / 2.0,
               GUIDE_BAR_S0, GUIDE_BAR_S1, GUIDE_BAR_SIDE,
               GUIDE_BAR_SIDE, 'new')
    comp.bRepBodies.item(0).name = GUIDE
    return occ


def _build_stop():
    B.drop_comp(STOP)
    occ = B.new_comp(STOP)
    comp = occ.component
    kx, kz = R.KNEE_X, R.KNEE_Z
    sk = B.sk_on_y(comp, R.STOP_PLATE_Y0)
    B.arc_sector(sk, kx, kz, R.STOP_SECTOR_R_IN, R.STOP_SECTOR_R_OUT,
                 R.STOP_SECTOR_A0, R.STOP_SECTOR_A1)
    B.extrude(comp, B.biggest_profile(sk),
              R.STOP_PLATE_Y1 - R.STOP_PLATE_Y0)

    angle_ext = R.STOP_DOWEL_A_PHI0 - TEST_PHI_EXT
    angle_flex = R.STOP_DOWEL_A_PHI0 - TEST_PHI_FLEX
    radius = (R.STOP_SLOT_R_IN + R.STOP_SLOT_R_OUT) / 2.0
    sk = B.sk_on_y(comp, R.STOP_PLATE_Y0)
    points = []
    for index in range(25):
        angle = math.radians(angle_flex +
                             (angle_ext - angle_flex) * index / 24.0)
        points.append((kx + radius * math.cos(angle),
                       kz + radius * math.sin(angle)))
    for index in range(len(points) - 1):
        B.slot(sk, points[index][0], points[index][1],
               points[index + 1][0], points[index + 1][1],
               R.STOP_SLOT_R_OUT - R.STOP_SLOT_R_IN)
    # Leave the same closed outboard skin as the canonical rig plate.  The
    # ordered Ø6 x 10 dowel is captured between this skin and the distal-link
    # socket floor instead of relying on a printed press fit.
    B.extrude(comp, B.profiles(sk), R.STOP_SLOT_DEPTH,
              op='cut', participants=_bodies(comp))

    sk = B.sk_on_y(comp, R.STOP_PLATE_Y0)
    for angle_deg in R.STOP_INSERT_A:
        angle = math.radians(angle_deg)
        B.circle(sk, kx + R.STOP_INSERT_R * math.cos(angle),
                 kz + R.STOP_INSERT_R * math.sin(angle), 3.4)
    B.extrude(comp, B.profiles(sk), R.STOP_PLATE_Y1 - R.STOP_PLATE_Y0,
              op='cut', participants=_bodies(comp))
    comp.bRepBodies.item(0).name = STOP
    return occ


def _build_spacer():
    B.drop_comp(SPACER)
    occ = B.new_comp(SPACER)
    comp = occ.component
    B.cyl_y(comp, None, R.KNEE_X, R.KNEE_Z, SPACER_OD,
            SPACER_Y0, SPACER_Y1)
    B.cyl_y(comp, None, R.KNEE_X, R.KNEE_Z, 4.0,
            SPACER_Y0 - 0.5, SPACER_Y1 + 0.5, op='cut',
            participants=_bodies(comp))
    B.cyl_y(comp, None, R.KNEE_X, R.KNEE_Z, SPACER_LOCATOR_D,
            SPACER_Y1, SPACER_LOCATOR_Y1, op='join')
    comp.bRepBodies.item(0).name = SPACER
    return occ


def _build_test_rim():
    """Support-free ABS wheel shell for the suspended mechanical test.

    The hub interface and outer drum are the frozen geometry.  The tyre bead,
    inboard flange, and unsupported inner ledge are omitted because this test
    keeps the wheel clear of the floor and does not fit the TPU tyre.
    """
    B.drop_comp(RIM)
    occ = B.new_comp(RIM)
    comp = occ.component
    B.ring(comp, B.RIM_WEB_Y_A, B.RIM_WEB_INNER_R, 45.0,
           B.RIM_WEB_Y_B - B.RIM_WEB_Y_A, 'new', cx=B.WX, cz=B.WZ)
    B.ring(comp, B.RIM_Y0, 44.0, B.RIM_OD / 2.0,
           B.RIM_WEB_Y_B - B.RIM_Y0, 'join', cx=B.WX, cz=B.WZ)
    sk = B.sk_on_y(comp, B.RIM_WEB_Y_A - 1.0)
    B.circles_polar(sk, B.WX, B.WZ, B.RIM_BOLT_PCD, 4.3, 6, 0.0)
    B.extrude(comp, B.profiles(sk),
              (B.RIM_WEB_Y_B - B.RIM_WEB_Y_A) + 2.0, 'cut',
              participants=_bodies(comp))
    sk = B.sk_on_y(comp, B.RIM_WEB_Y_A)
    B.circles_polar(sk, B.WX, B.WZ, B.RIM_BOLT_PCD,
                    B.WHEEL_RIM_RELIEF_D, 6, 0.0)
    B.extrude(comp, B.profiles(sk), B.WHEEL_RIM_RELIEF_DEPTH, 'cut',
              participants=_bodies(comp))
    sk = B.sk_on_y(comp, B.RIM_WEB_Y_A - 1.0)
    B.circles_polar(sk, B.WX, B.WZ, 66.0, 14.0, 6, 30.0)
    B.extrude(comp, B.profiles(sk),
              (B.RIM_WEB_Y_B - B.RIM_WEB_Y_A) + 2.0, 'cut',
              participants=_bodies(comp))
    comp.bRepBodies.item(0).name = RIM
    return occ


def _build_spring_reference(phi=0.0):
    direction, length = B.cart_dir(phi)

    def point(s, radius=0.0):
        normal = (-direction[1], direction[0])
        return (B.UX + s * direction[0] + radius * normal[0],
                B.UZ + s * direction[1] + radius * normal[1])

    lower_seat = length - LOWER_PIVOT_TO_SEAT
    B.drop_comp(SPRING_REF)
    occ = B.new_comp(SPRING_REF)
    comp = occ.component
    _revolved_ring(comp, point, length, UPPER_SEAT_S, lower_seat,
                   OWNED_SPRING_ID / 2.0, OWNED_SPRING_OD / 2.0, 'new')
    comp.bRepBodies.item(0).name = SPRING_REF
    return occ


def _register_pose_classes():
    for name in (UPPER, GUIDE):
        if name not in B.CART_UP_NAMES:
            B.CART_UP_NAMES = B.CART_UP_NAMES + (name,)
    if LOWER not in B.CART_LO_NAMES:
        B.CART_LO_NAMES = B.CART_LO_NAMES + (LOWER,)
    if STOP not in B.PROX_NAMES:
        B.PROX_NAMES = B.PROX_NAMES + (STOP,)
    if SPACER not in B.PROX_NAMES:
        B.PROX_NAMES = B.PROX_NAMES + (SPACER,)
    if RIM not in B.DIST_NAMES:
        B.DIST_NAMES = B.DIST_NAMES + (RIM,)


def _topology(occ):
    assert occ and occ.component.bRepBodies.count == 1
    body = occ.component.bRepBodies.item(0)
    assert body.isSolid and body.lumps.count == 1
    assert all(edge.faces.count == 2 for edge in body.edges)
    box = body.boundingBox
    return {
        'volume_mm3': body.volume * 1000.0,
        'faces': body.faces.count,
        'edges': body.edges.count,
        'closed_manifold': True,
        'bbox_mm': [box.minPoint.x * 10.0, box.maxPoint.x * 10.0,
                    box.minPoint.y * 10.0, box.maxPoint.y * 10.0,
                    box.minPoint.z * 10.0, box.maxPoint.z * 10.0],
    }


def build(_context: str):
    app = adsk.core.Application.get()
    assert app.activeDocument.name == 'Beni_SingleLegRig'
    R.ref_assert()
    R.placed_assert()
    _register_pose_classes()
    parts = [R.guarded(builder) for builder in
             (_build_upper, _build_lower, _build_guide, _build_stop,
              _build_spacer, _build_test_rim, _build_spring_reference)]
    B.capture_nominal(force=True)
    for occurrence in B.root().occurrences:
        occurrence.isLightBulbOn = (B.base_name(occurrence.component.name)
                                    not in NOT_IN_ABS_ARTICLE)
    app.activeViewport.fit()
    app.activeViewport.refresh()
    print(json.dumps({part.component.name: _topology(part) for part in parts},
                     indent=2, sort_keys=True))


def _tm():
    return adsk.fusion.TemporaryBRepManager.get()


def _copy_at_occ(occ):
    body = _tm().copy(occ.component.bRepBodies.item(0))
    assert _tm().transform(body, occ.transform2)
    return body


def _overlap(first, second):
    a, b = first.boundingBox, second.boundingBox
    if any(getattr(a.maxPoint, axis) <= getattr(b.minPoint, axis) + 1e-8 or
           getattr(b.maxPoint, axis) <= getattr(a.minPoint, axis) + 1e-8
           for axis in ('x', 'y', 'z')):
        return 0.0
    result = _tm().copy(first)
    assert _tm().booleanOperation(
        result, second, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return result.volume * 1000.0


def _shifted(body, x=0.0, y=0.0, z=0.0):
    result = _tm().copy(body)
    transform = adsk.core.Matrix3D.create()
    transform.translation = adsk.core.Vector3D.create(
        x / 10.0, y / 10.0, z / 10.0)
    assert _tm().transform(result, transform)
    return result


def _spring_envelope(phi, end_clearance=0.1):
    direction, length = B.cart_dir(phi)
    lower_x, lower_z = B.lower_pivot_at(phi)
    start_s = UPPER_SEAT_S + end_clearance
    end_from_lower = LOWER_PIVOT_TO_SEAT + end_clearance
    first = adsk.core.Point3D.create(
        (B.UX + start_s * direction[0]) / 10.0, B.LEG_Y_MID / 10.0,
        (B.UZ + start_s * direction[1]) / 10.0)
    second = adsk.core.Point3D.create(
        (lower_x - end_from_lower * direction[0]) / 10.0,
        B.LEG_Y_MID / 10.0,
        (lower_z - end_from_lower * direction[1]) / 10.0)
    outer = _tm().createCylinderOrCone(
        first, OWNED_SPRING_OD / 20.0, second, OWNED_SPRING_OD / 20.0)
    inner = _tm().createCylinderOrCone(
        first, OWNED_SPRING_ID / 20.0, second, OWNED_SPRING_ID / 20.0)
    assert _tm().booleanOperation(
        outer, inner, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return outer


def _linear_path(body, fixed, vector, travel_mm, step_mm=0.5):
    steps = int(round(travel_mm / step_mm))
    maximum = 0.0
    for index in range(steps + 1):
        offset = travel_mm - index * step_mm
        trial = _shifted(body, x=vector[0] * offset,
                         # Avoid exact coincident assembly faces, which make
                         # Fusion's temporary Boolean kernel indeterminate.
                         y=vector[1] * offset + 0.001,
                         z=vector[2] * offset)
        values = []
        for item in fixed:
            try:
                values.append(_overlap(trial, item))
            except RuntimeError:
                # Retry a kernel-indeterminate coincident slice on both sides
                # of the nominal path.  Any real overlap survives 0.01 mm.
                retries = []
                for epsilon in (-0.01, 0.01):
                    retries.append(_overlap(_shifted(trial, y=epsilon), item))
                values.append(max(retries))
        maximum = max(maximum, sum(values))
        if maximum > 0.001:
            break
    return maximum


def _radial_path_search(body, fixed, travel_mm=40.0):
    rows = []
    for angle_deg in range(0, 360, 15):
        angle = math.radians(angle_deg)
        vector = (math.cos(angle), 0.0, math.sin(angle))
        maximum = _linear_path(body, fixed, vector, travel_mm)
        rows.append({'angle_deg': angle_deg,
                     'maximum_interference_mm3': maximum})
    clear = [row for row in rows
             if row['maximum_interference_mm3'] <= 0.001]
    assert clear
    return {'travel_mm': travel_mm, 'clear_directions': clear,
            'directions_checked': len(rows)}


def _occ_interference(moving, fixed):
    collection = adsk.core.ObjectCollection.create()
    collection.add(moving)
    for occurrence in fixed:
        collection.add(occurrence)
    request = B.design().createInterferenceInput(collection)
    request.areCoincidentFacesIncluded = False
    result = B.design().analyzeInterference(request)
    if not result:
        return 0.0
    return sum(result.item(index).interferenceBody.volume * 1000.0
               for index in range(result.count))


def _occ_linear_path(moving, fixed, vector, travel_mm, step_mm=0.5):
    base = list(moving.transform2.asArray())
    maximum = 0.0
    try:
        steps = int(round(travel_mm / step_mm))
        for index in range(steps + 1):
            offset = travel_mm - index * step_mm
            translation = B._trans_arr((vector[0] * offset,
                                        vector[1] * offset,
                                        vector[2] * offset))
            moving.transform2 = B._as_matrix(B._mm(translation, base))
            maximum = max(maximum, _occ_interference(moving, fixed))
            if maximum > 0.001:
                break
    finally:
        moving.transform2 = B._as_matrix(base)
    return maximum


def _occ_radial_path_search(moving, fixed, travel_mm=40.0):
    rows = []
    for angle_deg in range(0, 360, 15):
        angle = math.radians(angle_deg)
        maximum = _occ_linear_path(
            moving, fixed, (math.cos(angle), 0.0, math.sin(angle)), travel_mm)
        rows.append({'angle_deg': angle_deg,
                     'maximum_interference_mm3': maximum})
    clear = [row for row in rows
             if row['maximum_interference_mm3'] <= 0.001]
    assert clear
    return {'travel_mm': travel_mm, 'clear_directions': clear,
            'directions_checked': len(rows)}


def _pose(theta, phi):
    _register_pose_classes()
    snap = B.nominal_snapshot()
    B.pose(snap, theta, phi)


def _restore():
    B.restore_nominal()
    R.ref_assert()
    R.placed_assert()


def audit(_context: str):
    assert adsk.core.Application.get().activeDocument.name == 'Beni_SingleLegRig'
    from mechanical_release_audit_fusion import assert_all
    measured_interfaces = assert_all()
    _register_pose_classes()
    B.capture_nominal(force=True)
    report = {
        'measured_interface_contracts': measured_interfaces,
        'scope': 'unpowered supported ABS mechanical spring demonstration',
        'spring': {
            'owned_od_mm': OWNED_SPRING_OD,
            'owned_id_mm': OWNED_SPRING_ID,
            'free_length_mm': OWNED_SPRING_FREE,
            'rate': 'unmeasured; no force or equilibrium claim',
            'test_range_deg': [TEST_PHI_EXT, TEST_PHI_FLEX],
            'dead_length_mm': TEST_DEAD,
        },
        'poses': [],
        'topology': {},
        'ordered_pin_interfaces': {
            'clevis_M4x40': {
                'quantity_used': 2,
                'shaft_diameter_mm': B.CLEVIS_PIN_D,
                'selected_link_passage_diameter_mm': B.CLEVIS_LINK_BORE_D,
                'shaft_length_mm': B.CLEVIS_PIN_SHAFT_LEN,
                'retaining_hole_diameter_mm': B.CLEVIS_PIN_HOLE_D,
                'retaining_hole_datum_from_head_mm':
                    B.CLEVIS_PIN_HOLE_DATUM,
                'printed_stack_mm': B.CLEVIS_RETAINED_STACK,
                'washer': 'ISO 7089 M4, 4.3 x 9 x 0.8 mm',
                'conservative_hole_edge_clearance_mm':
                    (B.CLEVIS_PIN_HOLE_DATUM - B.CLEVIS_PIN_HOLE_D / 2.0
                     - B.CLEVIS_RETAINED_STACK - B.CLEVIS_WASHER_T),
                'upper_integral_boss_side': 'inboard; outboard print datum preserved',
                'lower_integral_boss_side': 'outboard; inboard print datum preserved',
                'cotter_keepout': ('orient the supplied cotter radially away from '
                                   'the knee; 30 mm centred XZ envelope reserved'),
            },
            'stop_dowel_D6x10': {
                'quantity_used': 1,
                'pin_span_y_mm': [B.STOP_PIN_SOCKET_Y0,
                                  B.STOP_PIN_SOCKET_Y0 + B.STOP_PIN_LEN],
                'distal_socket_diameter_mm': B.STOP_PIN_SOCKET_D,
                'distal_socket_depth_mm': B.STOP_PIN_SOCKET_DEPTH,
                'printed_socket_floor_mm':
                    B.STOP_PIN_SOCKET_Y0 - B.CH_Y1,
                'plate_channel_depth_mm': R.STOP_SLOT_DEPTH,
                'plate_outer_skin_mm': R.STOP_OUTER_SKIN,
                'pin_end_to_channel_cap_clearance_mm':
                    (R.STOP_PLATE_Y0 + R.STOP_SLOT_DEPTH
                     - (B.STOP_PIN_SOCKET_Y0 + B.STOP_PIN_LEN)),
            },
            'shoulder_root_dowels_D4x10': {
                'quantity_used': 3,
                'pcd_mm': B.ROOT_DOWEL_PCD,
                'angles_deg': list(B.ROOT_DOWEL_A),
                'hub_press_socket_mm': [B.ROOT_DOWEL_HUB_SOCKET_D,
                                        B.ROOT_DOWEL_HUB_DEPTH],
                'link_slip_socket_mm': [B.ROOT_DOWEL_LINK_SOCKET_D,
                                        B.ROOT_DOWEL_LINK_DEPTH],
                'axial_bottom_clearance_mm':
                    B.ROOT_DOWEL_LINK_DEPTH
                    - (B.ROOT_DOWEL_LEN - B.ROOT_DOWEL_HUB_DEPTH),
            },
        },
    }
    for name in (UPPER, LOWER, GUIDE, STOP, SPACER, RIM):
        report['topology'][name] = _topology(B.find_occ(name))
    assert report['ordered_pin_interfaces']['clevis_M4x40'][
        'conservative_hole_edge_clearance_mm'] >= 0.39
    assert report['ordered_pin_interfaces']['stop_dowel_D6x10'][
        'printed_socket_floor_mm'] >= 0.49
    assert report['ordered_pin_interfaces']['stop_dowel_D6x10'][
        'pin_end_to_channel_cap_clearance_mm'] >= 0.29
    assert report['ordered_pin_interfaces']['shoulder_root_dowels_D4x10'][
        'axial_bottom_clearance_mm'] >= 0.19

    prox_box = _topology(B.find_occ('Proximal_Link_L'))['bbox_mm']
    distal_box = _topology(B.find_occ('Distal_Link_L'))['bbox_mm']
    report['print_datum_preservation'] = {
        'proximal_outboard_max_y_mm': prox_box[3],
        'proximal_required_mm': B.PROX_PRINT_FACE_Y,
        'distal_inboard_min_y_mm': distal_box[2],
        'distal_required_mm': B.LEG_Y_IN,
    }
    assert abs(prox_box[3] - B.PROX_PRINT_FACE_Y) <= 0.001
    assert abs(distal_box[2] - B.LEG_Y_IN) <= 0.001

    original_visibility = [(occ, occ.isLightBulbOn)
                           for occ in B.root().occurrences]
    try:
        for phi in [TEST_PHI_EXT] + [float(v) for v in range(-7, 16)]:
            _pose(0.0, phi)
            upper = _copy_at_occ(B.find_occ(UPPER))
            lower = _copy_at_occ(B.find_occ(LOWER))
            guide = _copy_at_occ(B.find_occ(GUIDE))
            stop = _copy_at_occ(B.find_occ(STOP))
            dowel = _copy_at_occ(B.find_occ('HW_DowelPin_D6x10'))
            prox = _copy_at_occ(B.find_occ('Proximal_Link_L'))
            distal = _copy_at_occ(B.find_occ('Distal_Link_L'))
            spring = _spring_envelope(phi)
            spring_length = B.cart_len(phi) - TEST_DEAD
            channel_start = B.cart_len(phi) - LOWER_PIVOT_TO_SEAT - SPRING_PILOT_LO_L
            channel_end = B.cart_len(phi) - LOWER_GUIDE_END_FROM_PIVOT
            guide_overlap = min(GUIDE_BAR_S1, channel_end) - max(
                GUIDE_BAR_S0, channel_start)
            row = {
                'phi_deg': phi,
                'cartridge_pin_distance_mm': B.cart_len(phi),
                'installed_spring_length_mm': spring_length,
                'spring_compression_mm': OWNED_SPRING_FREE - spring_length,
                'guide_overlap_mm': guide_overlap,
                'guide_to_channel_end_clearance_mm': channel_end - GUIDE_BAR_S1,
                'upper_lower_interference_mm3': _overlap(upper, lower),
                'guide_lower_solid_interference_mm3': _overlap(guide, lower),
                'cartridge_to_proximal_mm3':
                    _overlap(upper, prox) + _overlap(lower, prox) +
                    _overlap(guide, prox),
                'cartridge_to_distal_mm3':
                    _overlap(upper, distal) + _overlap(lower, distal) +
                    _overlap(guide, distal),
                'spring_envelope_to_links_mm3':
                    _overlap(spring, prox) + _overlap(spring, distal),
                'stop_dowel_interference_mm3': _overlap(stop, dowel),
            }
            assert row['spring_compression_mm'] >= -0.001
            assert row['guide_overlap_mm'] >= 5.5
            assert row['guide_to_channel_end_clearance_mm'] >= 1.9
            assert row['upper_lower_interference_mm3'] <= 0.001
            assert row['guide_lower_solid_interference_mm3'] <= 0.001
            assert row['cartridge_to_proximal_mm3'] <= 0.001
            assert row['cartridge_to_distal_mm3'] <= 0.001
            assert row['spring_envelope_to_links_mm3'] <= 0.001
            # Slot should be clear in the open interval.  At both endpoints the
            # conformal stop is allowed to touch, but not to overlap materially.
            assert row['stop_dowel_interference_mm3'] <= 0.05
            report['poses'].append(row)

        report['stop_overtravel_proof'] = []
        for phi in (TEST_PHI_EXT - 0.5, TEST_PHI_FLEX + 0.5):
            _pose(0.0, phi)
            interference = _overlap(_copy_at_occ(B.find_occ(STOP)),
                                    _copy_at_occ(B.find_occ('HW_DowelPin_D6x10')))
            report['stop_overtravel_proof'].append({
                'phi_deg': phi,
                'stop_dowel_interference_mm3': interference,
            })
            assert interference > 0.05

        # Assemble at the zero-compression extension stop.  Prove independent
        # radial access for both eyes, axial insertion for the guide/spring,
        # and straight insertion of both steel clevis pins.
        _pose(0.0, TEST_PHI_EXT)
        upper_occ = B.find_occ(UPPER)
        lower_occ = B.find_occ(LOWER)
        guide_occ = B.find_occ(GUIDE)
        prox_occ = B.find_occ('Proximal_Link_L')
        distal_occ = B.find_occ('Distal_Link_L')
        direction, _length = B.cart_dir(TEST_PHI_EXT)
        spring = _spring_envelope(TEST_PHI_EXT)
        clevis = sorted(B.find_all_occ('HW_ClevisPin_M4x40'),
                        key=lambda item: item.boundingBox.minPoint.z,
                        reverse=True)
        assert len(clevis) == 2
        report['assembly_paths'] = {
            'upper_eye_radial': _occ_radial_path_search(
                upper_occ, [prox_occ]),
            'lower_eye_radial': _occ_radial_path_search(
                lower_occ, [distal_occ]),
            'guide_into_upper': {
                'travel_mm': 40.0,
                'maximum_interference_mm3': _occ_linear_path(
                    guide_occ, [upper_occ, prox_occ],
                    (direction[0], 0.0, direction[1]), 40.0),
            },
            'spring_over_guide': {
                'travel_mm': 30.0,
                'maximum_interference_mm3': _linear_path(
                    spring, [_copy_at_occ(upper_occ),
                             _copy_at_occ(guide_occ), _copy_at_occ(prox_occ)],
                    (direction[0], 0.0, direction[1]), 30.0),
            },
            'upper_clevis_from_inboard': {
                'travel_mm': 40.0,
                'maximum_interference_mm3': _occ_linear_path(
                    clevis[0], [upper_occ, prox_occ],
                    (0.0, -1.0, 0.0), 40.0),
            },
            'lower_clevis_from_inboard': {
                'travel_mm': 40.0,
                'maximum_interference_mm3': _occ_linear_path(
                    clevis[1], [lower_occ, distal_occ],
                    (0.0, -1.0, 0.0), 40.0),
            },
        }
        for name in ('guide_into_upper', 'spring_over_guide',
                     'upper_clevis_from_inboard', 'lower_clevis_from_inboard'):
            assert report['assembly_paths'][name][
                'maximum_interference_mm3'] <= 0.001
        _restore()

        # Pin spacer is carried by the proximal side.  It must sit between the
        # metal pin and the existing encoder bracket without touching either.
        spacer = _copy_at_occ(B.find_occ(SPACER))
        pin = _copy_at_occ(B.find_occ('HW_DowelPin_D10x35'))
        bracket = _copy_at_occ(B.find_occ('Knee_Encoder_Bracket_L'))
        report['pin_keeper'] = {
            'pin_to_spacer_interference_mm3': _overlap(pin, spacer),
            'spacer_to_bracket_interference_mm3': _overlap(spacer, bracket),
            'nominal_pin_end_gap_mm': SPACER_Y0 - PIN_END_Y,
            'nominal_bracket_gap_mm': 99.9 - SPACER_Y1,
            'inboard_retention': 'firm-thumb receiver fit; hand-contained test only',
        }
        assert report['pin_keeper']['pin_to_spacer_interference_mm3'] <= 0.001
        assert report['pin_keeper']['spacer_to_bracket_interference_mm3'] <= 0.001

        # The support-free test rim follows the already-verified straight
        # outboard service path and retains the six frozen hub interfaces.
        rim = _copy_at_occ(B.find_occ(RIM))
        fixed = [_copy_at_occ(B.find_occ('Wheel_Hub_L')),
                 _copy_at_occ(B.find_occ('Distal_Link_L'))]
        motor = B.find_occ('REF_GIM4305-10')
        for index in range(motor.childOccurrences.count):
            child = motor.childOccurrences.item(index)
            for body_index in range(child.bRepBodies.count):
                fixed.append(_tm().copy(child.bRepBodies.item(body_index)))
        report['rim_service_path'] = []
        for step in range(81):
            offset = 40.0 - step * 0.5
            value = sum(_overlap(_shifted(rim, y=offset), body)
                        for body in fixed)
            assert value <= 0.001
            report['rim_service_path'].append({
                'offset_y_mm': offset,
                'interference_mm3': value,
            })

        # The physical cap test owns pilot fit.  These are exact CAD checks for
        # radial clearances around the same nominal dimensions.
        report['radial_clearances_mm'] = {
            'spring_id_to_pilot_diametral': OWNED_SPRING_ID - SPRING_PILOT_D,
            'guide_bore_to_bar_diagonal':
                GUIDE_SOCKET_D - GUIDE_BAR_SIDE * math.sqrt(2.0),
        }
        assert report['radial_clearances_mm']['spring_id_to_pilot_diametral'] == 1.0
        assert report['radial_clearances_mm']['guide_bore_to_bar_diagonal'] > 0.20
    finally:
        _restore()
        for occ, state in original_visibility:
            occ.isLightBulbOn = state

    # Sweeping/rebuilding reference parts must not silently cut printed parts.
    assert_all()
    evidence_dir = _context or EVIDENCE_DIR   # a path argument is a dry run
    os.makedirs(evidence_dir, exist_ok=True)
    path = os.path.join(evidence_dir, 'fusion_mechanical_audit.json')
    with open(path, 'w') as stream:
        json.dump(report, stream, indent=2, sort_keys=True)
    print(json.dumps(report, indent=2, sort_keys=True))


def _export_axis_up(occ, export_name, axis, support_policy, out_dir=OUT_DIR):
    """Export with the selected cartridge axis mapped to print +Z."""
    from mechanical_release_audit_fusion import assert_part
    assert_part(occ.component.name)
    body = occ.component.bRepBodies.item(0)
    ax, az = axis
    perpendicular = (-az, ax)
    rotation = adsk.core.Matrix3D.create()
    rotation.setWithArray([
        perpendicular[0], 0.0, perpendicular[1], 0.0,
        0.0, 1.0, 0.0, 0.0,
        ax, 0.0, az, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ])
    transformed = _tm().copy(body)
    assert _tm().transform(transformed, rotation)
    shift = adsk.core.Matrix3D.create()
    shift.translation = adsk.core.Vector3D.create(
        0.0, 0.0, -transformed.boundingBox.minPoint.z)
    assert _tm().transform(transformed, shift)

    support_faces = []
    unsupported_downward_planes = []
    for index, face in enumerate(transformed.faces):
        plane = adsk.core.Plane.cast(face.geometry)
        if plane is None:
            continue
        ok, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
        assert ok
        z_mm = face.pointOnFace.z * 10.0
        if normal.z < -0.999999:
            row = {'index': index, 'z_mm': z_mm,
                   'area_mm2': face.area * 100.0}
            if abs(z_mm) <= 0.001:
                support_faces.append(row)
            else:
                unsupported_downward_planes.append(row)
    assert support_faces
    assert sum(row['area_mm2'] for row in support_faces) >= 90.0
    assert not unsupported_downward_planes

    root = B.root()
    temporary = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    temporary.component.name = export_name
    base = temporary.component.features.baseFeatures.add()
    base.name = export_name + '_FusionTransform'
    base.startEdit()
    result = temporary.component.bRepBodies.add(transformed, base)
    base.finishEdit()
    assert result and result.isSolid
    result.name = export_name
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, export_name + '.stl')
    staged_path = path + '.pending.stl'
    image_path = os.path.join(out_dir, '00_fusion_' + export_name + '.png')
    visibility = [(item, item.isLightBulbOn) for item in root.occurrences]
    try:
        for item, _state in visibility:
            item.isLightBulbOn = item == temporary
        size = E._stl(temporary, staged_path)
        from mechanical_release_audit_fusion import (
            assert_export, pinned_release_current)
        gate = assert_export(occ.component.name, staged_path)
        if pinned_release_current(occ.component.name, path):
            release_file = 'retained'
            size = os.path.getsize(path)
        else:
            os.replace(staged_path, path)
            release_file = 'written'
        E._save_print_image(image_path)
    finally:
        if os.path.exists(staged_path):
            os.remove(staged_path)
        for item, state in visibility:
            if item != temporary:
                item.isLightBulbOn = state
        temporary.deleteMe()
    box = transformed.boundingBox
    return {
        'source_part': occ.component.name,
        'export_name': export_name,
        'stl': path,
        'stl_bytes': size,
        'release_file': release_file,
        'mesh_gate': gate and gate.get('gate'),
        'fusion_screenshot': image_path,
        'source_axis_mapped_to_print_z': [ax, 0.0, az],
        'support_faces': support_faces,
        'unsupported_downward_planar_faces': unsupported_downward_planes,
        'oriented_bbox_mm': [
            (box.maxPoint.x - box.minPoint.x) * 10.0,
            (box.maxPoint.y - box.minPoint.y) * 10.0,
            (box.maxPoint.z - box.minPoint.z) * 10.0,
        ],
        'minimum_z_mm': 0.0,
        'support_policy': support_policy,
        'horizontal_pivot_bridge_mm': PIVOT_BORE_D,
    }


def _verify_binary_stl(path, native_volume_mm3):
    data = open(path, 'rb').read()
    triangles = struct.unpack_from('<I', data, 80)[0]
    assert len(data) == 84 + triangles * 50
    edges = Counter()
    degenerate = 0
    volume = 0.0
    points = []
    for index in range(triangles):
        values = struct.unpack_from('<12fH', data, 84 + index * 50)
        triangle = [tuple(values[3 + item * 3:6 + item * 3])
                    for item in range(3)]
        points.extend(triangle)
        if len(set(triangle)) < 3:
            degenerate += 1
        for item in range(3):
            edges[tuple(sorted((triangle[item],
                                triangle[(item + 1) % 3])))] += 1
        a, b, c = triangle
        volume += (a[0] * (b[1] * c[2] - b[2] * c[1]) +
                   a[1] * (b[2] * c[0] - b[0] * c[2]) +
                   a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
    report = {
        'file': path,
        'triangles': triangles,
        'nonmanifold_edges': sum(value != 2 for value in edges.values()),
        'degenerate_triangles': degenerate,
        'minimum_z_mm': min(point[2] for point in points),
        'dimensions_mm': [max(point[axis] for point in points) -
                          min(point[axis] for point in points)
                          for axis in range(3)],
        'mesh_volume_mm3': volume,
        'native_volume_relative_error':
            abs(volume - native_volume_mm3) / native_volume_mm3,
        'sha256': hashlib.sha256(data).hexdigest(),
    }
    assert report['nonmanifold_edges'] == 0
    assert report['degenerate_triangles'] == 0
    assert abs(report['minimum_z_mm']) <= 0.00001
    assert report['native_volume_relative_error'] < 0.002
    return report


def _assembly_image(phi, filename):
    """ABS article only, from the front-outboard side where the leg is visible.

    Visibility and camera are restored afterwards; the capture no longer leaves
    the structural parts hidden in the model.
    """
    R.guarded(_build_spring_reference, phi)
    B.capture_nominal(force=True)
    _pose(0.0, phi)
    root = B.root()
    B.design().activateRootComponent()
    bulbs = [(occurrence, occurrence.isLightBulbOn) for occurrence in root.occurrences]
    viewport = adsk.core.Application.get().activeViewport
    old_camera = viewport.camera
    try:
        for occurrence in root.occurrences:
            occurrence.isLightBulbOn = (B.base_name(occurrence.component.name)
                                        not in NOT_IN_ABS_ARTICLE)
        camera = viewport.camera
        target = adsk.core.Point3D.create(0.0, 5.0, -8.0)
        camera.target = target
        camera.eye = adsk.core.Point3D.create(target.x - 25.0, target.y + 45.0,
                                              target.z + 20.0)
        camera.upVector = adsk.core.Vector3D.create(0.0, 0.0, 1.0)
        camera.isFitView = True
        viewport.camera = camera
        viewport.refresh()
        assert viewport.saveAsImageFile(filename, 2000, 1500)
    finally:
        for occurrence, state in bulbs:
            occurrence.isLightBulbOn = state
        viewport.camera = old_camera
        _restore()


def release(_context: str):
    """Export the six current spring-test parts; a path argument is a dry run."""
    app = adsk.core.Application.get()
    assert app.activeDocument.name == 'Beni_SingleLegRig'
    from mechanical_release_audit_fusion import assert_all
    assert_all()
    out_dir = _context or OUT_DIR
    evidence_dir = _context or EVIDENCE_DIR
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(evidence_dir, exist_ok=True)
    _register_pose_classes()
    B.design().activateRootComponent()
    B.capture_nominal(force=True)
    R.ref_assert()
    R.placed_assert()

    direction, _length = B.cart_dir(0.0)
    exports = []
    exports.append(R.guarded(
        _export_axis_up, B.find_occ(UPPER),
        UPPER + '_AXIS_UP_PRINT_ORIENTED', direction,
        'Import unchanged. No supports. Use a brim; inspect the 4.4 mm '
        'self-supporting horizontal pivot passage.', out_dir))
    exports.append(R.guarded(
        _export_axis_up, B.find_occ(LOWER),
        LOWER + '_AXIS_UP_PRINT_ORIENTED',
        (-direction[0], -direction[1]),
        'Import unchanged. No supports. Use a brim; inspect the 4.4 mm '
        'self-supporting horizontal pivot passage.', out_dir))

    # The captive stop plate is released by ordered_pin_integration_fusion;
    # exporting it here would overwrite the superseded Sept 17 file.
    standard = [
        (GUIDE, GUIDE + '_FLAT_PRINT_ORIENTED', E._export_max_y_face_down,
         'Import unchanged; no supports; 3.8 mm square face on bed.'),
        (SPACER, SPACER + '_PRINT_ORIENTED', E._export_min_y_face_down,
         'Import unchanged; no supports; broad 15 mm face on bed.'),
        (RIM, RIM + '_PRINT_ORIENTED', E._export_max_y_face_down,
         'Import unchanged; no supports; broad web face on bed; no tyre.'),
        ('Knee_Encoder_Bracket_L',
         'ABS_TEST_Knee_Encoder_Bracket_PIN_KEEPER_PRINT_ORIENTED',
         E._export_max_y_face_down,
         'Import unchanged; no supports; shelf face on bed and posts up.'),
    ]
    for source, name, exporter, policy in standard:
        exports.append(R.guarded(exporter, B.find_occ(source), name,
                                 out_dir, policy))

    mesh = {}
    for item in exports:
        source = B.find_occ(item['source_part'])
        native_volume = _topology(source)['volume_mm3']
        mesh[item['export_name']] = _verify_binary_stl(
            item['stl'], native_volume)

    nominal_image = os.path.join(
        evidence_dir, '00_fusion_full_mechanical_test_phi_0.png')
    flexed_image = os.path.join(
        evidence_dir, '01_fusion_full_mechanical_test_phi_15.png')
    _assembly_image(0.0, nominal_image)
    _assembly_image(TEST_PHI_FLEX, flexed_image)
    R.guarded(_build_spring_reference, 0.0)
    B.capture_nominal(force=True)
    _restore()

    manifest = {
        'fusion_document': app.activeDocument.name,
        'scope': 'unpowered supported ABS mechanical spring demonstration',
        'spring': {
            'owned_od_mm': OWNED_SPRING_OD,
            'owned_id_mm': OWNED_SPRING_ID,
            'free_length_mm': OWNED_SPRING_FREE,
            'rate': 'unmeasured',
            'range_deg': [TEST_PHI_EXT, TEST_PHI_FLEX],
            'compression_mm': [0.0,
                               OWNED_SPRING_FREE -
                               (B.cart_len(TEST_PHI_FLEX) - TEST_DEAD)],
        },
        'exports': exports,
        'mesh_verification': mesh,
        'assembly_images': [nominal_image, flexed_image],
    }
    with open(os.path.join(out_dir, 'fusion_manifest.json'), 'w') as stream:
        json.dump(manifest, stream, indent=2, sort_keys=True)
    with open(os.path.join(evidence_dir, 'fusion_release_manifest.json'), 'w') as stream:
        json.dump(manifest, stream, indent=2, sort_keys=True)
    print(json.dumps(manifest, indent=2, sort_keys=True))
