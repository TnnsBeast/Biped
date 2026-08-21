"""Fusion script entry point for the bridge.

Fusion calls run(context) when you press Run in Scripts and Add-Ins. All this
does is delegate to fusion_bridge.probe, which does the real work.

Installed by pointing Scripts and Add-Ins at this folder -- see
fusion_bridge/OPERATOR.md.
"""

import os
import sys
import traceback

import adsk.core

# fusion_bridge/BeniBridge/ -> repo root, so `import fusion_bridge` resolves
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        if REPO not in sys.path:
            sys.path.insert(0, REPO)

        # reload so edits to the bridge land without restarting Fusion
        import importlib
        import fusion_bridge.ops
        import fusion_bridge.probe
        importlib.reload(fusion_bridge.ops)
        importlib.reload(fusion_bridge.probe)

        fusion_bridge.probe.run()
    except Exception:                                     # noqa: BLE001
        if ui:
            ui.messageBox('BeniBridge failed before it could write a result:\n\n%s'
                          % traceback.format_exc())
