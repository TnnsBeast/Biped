"""Release tessellation standard for printed-part STLs. Execute via Fusion MCP.

Every reviewed release mesh exported before 2026-09-24 has a 0.0039-0.0040 mm
chord sagitta on its circular edges, including the Ø4.30 root sockets, Ø12
bore and Ø56 flange of the PINREV2 hub. That machine's Fusion honoured the High
preset's surface deviation. Fusion 2705.1.25 ignores surface deviation, both in
STL export and in TriangleMeshCalculator, and honours only the normal
deviation: High gave 10° segments on small holes and a 0.0125 mm chord on large
ones. A fit transfers only when coupon and part share a tessellation, so the
same chord is set here through the segment angle of the largest curved radius.
All 15 current printed parts contain only planar and cylindrical faces.
"""
import math

import adsk.core
import adsk.fusion

CHORD_MM = 0.004          # sagitta measured on the reviewed release meshes
CHORD_GATE_MM = 0.005     # acceptance limit for a newly written release mesh
MAX_SEGMENT_DEG = 10.0    # the High preset's normal deviation
MIN_SEGMENT_DEG = 0.5     # floor for faces whose radius cannot be read


def max_curved_radius_mm(bodies):
    """Largest radius of any curved face; None when every face is planar."""
    largest = None
    for body in bodies:
        for face in body.faces:
            geometry = face.geometry
            radius = None
            if adsk.core.Plane.cast(geometry):
                continue
            cylinder = adsk.core.Cylinder.cast(geometry)
            torus = adsk.core.Torus.cast(geometry)
            sphere = adsk.core.Sphere.cast(geometry)
            if cylinder:
                radius = cylinder.radius * 10.0
            elif torus:
                radius = (torus.majorRadius + torus.minorRadius) * 10.0
            elif sphere:
                radius = sphere.radius * 10.0
            else:
                # Cones, splines and other surfaces: bound the radius by the
                # face's bounding-box diagonal instead of guessing a value.
                box = face.boundingBox
                radius = box.minPoint.distanceTo(box.maxPoint) * 10.0
            largest = radius if largest is None else max(largest, radius)
    return largest


def segment_deg(radius_mm, chord_mm=CHORD_MM):
    """Segment angle whose chord sagitta on radius_mm equals chord_mm."""
    if not radius_mm:
        return MAX_SEGMENT_DEG
    ratio = max(-1.0, min(1.0, 1.0 - chord_mm / radius_mm))
    angle = math.degrees(2.0 * math.acos(ratio))
    return max(MIN_SEGMENT_DEG, min(MAX_SEGMENT_DEG, angle))


def stl_options(export_manager, geometry, path, bodies):
    """Binary STL options meeting CHORD_MM on any Fusion build seen so far.

    High keeps the preset surface deviation for builds that honour it; the
    explicit normal deviation controls the chord on builds that do not.
    """
    options = export_manager.createSTLExportOptions(geometry, path)
    options.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    options.normalDeviation = segment_deg(max_curved_radius_mm(bodies))
    options.isBinaryFormat = True
    return options
