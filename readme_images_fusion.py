"""Export the README CAD gallery from the active Beni_Prototype1 document.

Run this file through the Fusion MCP after a model change that affects the full
robot, leg, knee, or wheel-module views. The script changes viewport presentation
and temporary occurrence visibility only; it restores visibility and leaves the
viewport in a fitted isometric view.
"""

import math
import os
import time

import adsk.core
import adsk.fusion


OUTPUT_DIR = "/Users/neilchulani/Robots/Biped/docs/readme"


def _settle(viewport):
    viewport.refresh()
    adsk.doEvents()
    time.sleep(0.4)
    viewport.refresh()


def _save(viewport, filename, width, height):
    path = os.path.join(OUTPUT_DIR, filename)
    options = adsk.core.SaveImageFileOptions.create(path)
    options.width = width
    options.height = height
    options.isAntiAliased = True
    options.isBackgroundTransparent = True
    if not viewport.saveAsImageFileWithOptions(options):
        raise RuntimeError("README image export failed: " + path)
    print(path)


def _standard_view(viewport, orientation, fit=True):
    camera = viewport.camera
    camera.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    camera.viewOrientation = orientation
    camera.isFitView = fit
    camera.isSmoothTransition = False
    viewport.camera = camera
    if fit:
        viewport.fit()
    _settle(viewport)


def _detail_view(viewport, target, extents):
    camera = viewport.camera
    camera.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    camera.eye = adsk.core.Point3D.create(target[0], target[1] + 50.0, target[2])
    camera.target = adsk.core.Point3D.create(*target)
    camera.upVector = adsk.core.Vector3D.create(0.0, 0.0, 1.0)
    camera.viewExtents = extents
    camera.isFitView = False
    camera.isSmoothTransition = False
    viewport.camera = camera
    _settle(viewport)


def _restore_bulbs(original_bulbs):
    for occurrence, state in original_bulbs:
        occurrence.isLightBulbOn = state


def run(_context: str):
    app = adsk.core.Application.get()
    if app.activeDocument.name != "Beni_Prototype1":
        raise RuntimeError("Open Beni_Prototype1 before exporting README images")

    design = adsk.fusion.Design.cast(app.activeProduct)
    viewport = app.activeViewport
    occurrences = list(design.rootComponent.allOccurrences)
    root_occurrences = list(design.rootComponent.occurrences)
    original_bulbs = [(occ, occ.isLightBulbOn) for occ in occurrences]
    original_style = viewport.visualStyle

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        viewport.visualStyle = (
            adsk.core.VisualStyles.ShadedWithVisibleEdgesOnlyVisualStyle
        )

        _standard_view(
            viewport,
            adsk.core.ViewOrientations.IsoTopLeftViewOrientation,
        )
        _save(viewport, "beni_full_robot.png", 1800, 1200)

        for occ in occurrences:
            if "(Mirror)" in occ.component.name:
                occ.isLightBulbOn = False

        _standard_view(
            viewport,
            adsk.core.ViewOrientations.BackViewOrientation,
        )
        _save(viewport, "beni_leg_side.png", 1400, 1000)

        _detail_view(viewport, (7.4, 7.45, -8.7), 5.5)
        _save(viewport, "beni_knee_detail.png", 1400, 1000)

        _restore_bulbs(original_bulbs)
        wheel_hubs = [
            occ for occ in root_occurrences if occ.component.name == "Wheel_Hub_L"
        ]
        if len(wheel_hubs) != 1:
            raise RuntimeError("Expected one top-level Wheel_Hub_L occurrence")
        wheel_box = wheel_hubs[0].boundingBox
        wheel_center_x = (wheel_box.minPoint.x + wheel_box.maxPoint.x) / 2.0
        wheel_center_y = (wheel_box.minPoint.y + wheel_box.maxPoint.y) / 2.0
        wheel_center_z = (wheel_box.minPoint.z + wheel_box.maxPoint.z) / 2.0

        for occ in root_occurrences:
            box = occ.boundingBox
            center_x = (box.minPoint.x + box.maxPoint.x) / 2.0
            center_y = (box.minPoint.y + box.maxPoint.y) / 2.0
            center_z = (box.minPoint.z + box.maxPoint.z) / 2.0
            radial_distance = math.hypot(
                center_x - wheel_center_x,
                center_z - wheel_center_z,
            )
            occ.isLightBulbOn = (
                radial_distance < 4.8
                and abs(center_y - wheel_center_y) < 4.0
            )

        _standard_view(
            viewport,
            adsk.core.ViewOrientations.IsoTopRightViewOrientation,
        )
        _save(viewport, "beni_wheel_module.png", 1400, 1000)
    finally:
        _restore_bulbs(original_bulbs)
        viewport.visualStyle = original_style
        _standard_view(
            viewport,
            adsk.core.ViewOrientations.IsoTopLeftViewOrientation,
        )
