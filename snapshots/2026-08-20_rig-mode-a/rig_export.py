"""Exports for the Beni single-leg test rig.

Runs inside Fusion against `Beni_SingleLegRig`.  Produces:

  * `rig_stl/*.stl`            every printed rig part, at assembly coordinates
  * `rig_stl/reroute/*.stl`    the formerly-machined parts, now printed

There is no DXF output.  The build has no laser-cut or machined parts: the steel
arc stop was replaced by a compression stack in the spring cartridge and a
printed plate, and the steel ballast sectors by printed pots filled with
off-the-shelf shot.  The retired laser files are kept under `archive_laser/` in
case the two-leg build wants the steel version back.
"""

import os

import adsk.core
import adsk.fusion

import beni_lib as B
import rig_lib as R

ROOT = '/Users/neilchulani/Fun/Robots/Biped'
STL_DIR = os.path.join(ROOT, 'rig_stl')

# printed rig parts, with the orientation each one has to be printed in
RIG_PRINT = [
    ('RIG_Stand', 'mount face (y = 42.00) flat on the bed, building inboard. '
                  'Every layer is then an XZ slice, so the dominant 11.00 N.m '
                  'of shoulder yaw -- a couple lying IN the XZ plane -- stays '
                  'in the print plane at 84-102 MPa instead of across the '
                  'layers at 26-50.  No support: the Y thickness only ever '
                  'decreases away from the bed.  Needs a bed >= 300 mm'),
    ('RIG_Carriage', 'plate face flat on the bed; bending stays in the print '
                     'plane and the 8 block-screw counterbores print as pockets'),
    ('RIG_Index_Bar', 'flat on the bed, station holes vertical; the pin bears '
                      'across layers, not along them'),
    ('RIG_Torque_Arm', 'flat on the bed, arm plane parallel to the bed; the '
                       '200 mm bending load is then fully in-plane'),
    ('RIG_Floor_Plate', 'flat on the bed'),
    ('RIG_Cable_Post_A', 'flat on the bed, sector face down'),
    ('RIG_Cable_Post_B', 'flat on the bed'),
    ('RIG_Knee_Collar_L', 'bore axis vertical, so the Ø10 press fit is round'),
    ('RIG_Knee_Magnet_Carrier_L', 'bore axis vertical -- this is what holds the '
                                  '0.05 TIR the encoder needs'),
    ('RIG_Knee_Stop_Plate_L', 'flat on the bed; replaces the laser-cut steel arc. '
                              'It keeps the -8 deg extension stop and a +28 deg '
                              'flexion backup only -- the working +27 deg stop is '
                              'the washer stack in the cartridge'),
    ('RIG_Knee_Bumper_Tube_L', 'TPU 95A, bore axis vertical. Sits AROUND the '
                               'washer stack so the two act in parallel'),
    ('RIG_Ballast_Pot', 'open side up, no support; fill with steel shot'),
]

# formerly machined, now printed (beni_rig_no_machining.md §3)
REROUTE_PRINT = [
    ('Shoulder_Output_Hub_L', 'flange face flat on the bed, so torque loads the '
                              'bolt circle in XY and the 3 dowel holes see '
                              'shear ACROSS layers'),
    ('Wheel_Hub_L', 'flat on the bed, register face up'),
    ('Cart_Upper_Eye_L', 'pivot bore axis vertical; printed on its side the eye '
                         'splits along a layer'),
    ('Cart_Lower_Eye_L', 'pivot bore axis vertical'),
    ('Distal_Link_L', 'on edge, link axis vertical -- RE-EXPORTED: its Ø16 '
                      'sleeve bore is now Ø10 (§2.3)'),
]


def _stl(occ, path, refinement='high'):
    des = B.design()
    em = des.exportManager
    opt = em.createSTLExportOptions(occ, path)
    opt.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    opt.isBinaryFormat = True
    em.execute(opt)
    return os.path.getsize(path)


def export_stls(verbose=True):
    os.makedirs(STL_DIR, exist_ok=True)
    os.makedirs(os.path.join(STL_DIR, 'reroute'), exist_ok=True)
    done, failed = [], []
    for part, note in [(p, '') for p, _n in RIG_PRINT]:
        occ = B.find_occ(part)
        if occ is None:
            failed.append((part, 'not in model'))
            continue
        try:
            done.append((part, _stl(occ, os.path.join(STL_DIR, part + '.stl'))))
        except Exception as e:
            failed.append((part, str(e)[:70]))
    for part, _note in REROUTE_PRINT:
        occ = B.find_occ(part)
        if occ is None:
            failed.append((part, 'not in model'))
            continue
        try:
            done.append(('reroute/' + part,
                         _stl(occ, os.path.join(STL_DIR, 'reroute',
                                                part + '.stl'))))
        except Exception as e:
            failed.append((part, str(e)[:70]))
    if verbose:
        for p, sz in done:
            print('   STL   %-40s %9.1f kB' % (p, sz / 1024.0))
        for p, why in failed:
            print('   FAIL  %-40s %s' % (p, why))
    return done, failed


def export_all():
    print('=== rig STLs ===')
    export_stls()
