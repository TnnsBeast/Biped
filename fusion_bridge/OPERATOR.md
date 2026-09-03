# Operator instructions — running the Fusion bridge

You are the **operator**: a terminal agent (or human) with Fusion 360 open. The
**analyst** is an agent that cannot reach Fusion and works only from files in
this repo. Your job is to execute one request and hand back one JSON file.

Protocol: [`PROTOCOL.md`](PROTOCOL.md). Read it once before your first run.

## The loop

**1. Validate the request before touching Fusion.**

```
python3 fusion_bridge/bridge.py check
```

Must print `request valid`. If it does not, stop and report the errors to the
analyst — do not fix the request yourself. A malformed request usually means the
analyst wanted something the whitelist does not offer, and silently editing it
destroys that signal.

**2. Open the right document.** The request's `document` field names it. `probe.py`
asserts this and aborts before running anything, but opening the right one first
saves a round trip.

**3. Run it.** In Fusion: *Utilities → Add-Ins → Scripts and Add-Ins*, or the
Text Commands console:

```python
import sys; sys.path.insert(0, '/Users/neilchulani/Robots/Biped')
import fusion_bridge.probe as probe
probe.run()
```

A dialog reports ops-ok count and guard status. The result lands in
`fusion_bridge/out/<runid>.json`.

**4. Report back.** Tell the analyst the runid and the guard status. The analyst
reads the file itself:

```
python3 fusion_bridge/bridge.py read <runid>
```

## Rules that are not negotiable

**Never add `confirm_mutate` yourself.** If a request contains a mutating op
without it, `probe.py` aborts by design. That flag is the analyst's explicit
statement that it intends to modify the model. Adding it on the analyst's behalf
forges consent for a model write. Report the abort instead.

**Never hand-edit a result file.** It is the audit trail of what the model
actually said on a given date. If a run was wrong, run again with a new runid.

**Never widen the whitelist to satisfy one request.** If the analyst needs an op
that does not exist, add it to `ops.py` as a named, documented function — do not
add a generic "eval this code" op. The whitelist is the thing that stops the
documented API traps from being re-stepped on.

**If the guard fails, stop.** Do not run further requests. `guard.ok == false`
means `REF_GIM6010-8` or `REF_GIM4305-10` has moved off its asserted Y span, i.e.
the motor STEP references have displaced — the known hazard in rig design record
§6.2. Every number in that run is computed against wrong geometry. Recover the
model first (capture `transform2`, restore, re-assert) before running anything
else.

## If the model needs a structural edit

Do not do it through the bridge. The bridge has no op for deleting or adding
occurrences, deliberately: deleting *any* occurrence in `Beni_SingleLegRig`
displaces both motor references, and `isSuppressed = True` is not a workaround
because the property is not readable on this API build — the assignment lands on
the Python wrapper and changes nothing.

The procedure is in `CLAUDE.md` and rig design record §6.2: capture `transform2`
for both `REF_*` occurrences **and every child in their trees**, delete, write
them back, assert the bounding boxes. Prefer changing the builder in
`rig_lib.py` and rebuilding over hand-editing the model at all.

## After any structural edit

Re-run the audits and file a fresh bridge run so the analyst sees the new state:

```python
import rig_lib; rig_lib.checks_44(); rig_lib.real_clashes()
```

## Worth doing on your first successful run

There is no snapshot of `Beni_SingleLegRig` anywhere in this repo — no `.f3d`, no
`.step`, no metrics JSON — despite it being the active, verified build with a
documented reproducible corruption hazard. Exporting one to
`snapshots/<date>_rig-baseline/` is the highest-value artifact currently missing
from the project. See the unresolved list in `PROJECT_STATUS.md`.
