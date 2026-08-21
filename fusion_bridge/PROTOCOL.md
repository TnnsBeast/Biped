# Fusion bridge protocol

A file-based request/response contract between an agent that **cannot** reach
Fusion (call it the *analyst*) and a terminal agent that **can** (the *operator*).

No sockets, no daemon, no MCP. One JSON file in, one JSON file out. Both are in
the repo so every exchange is reviewable and diffable.

```
analyst  ──writes──>  fusion_bridge/request.json
operator ──runs────>  probe.py inside Fusion
operator ──writes──>  fusion_bridge/out/<runid>.json
analyst  ──reads───>  that file, and only that file
```

## Why declarative ops and not "run this Fusion code"

Because the traps in this project are in the API, not the geometry. `isSuppressed`
is silently unwritable; deleting an occurrence displaces both motor STEP
references; bounding boxes inflate under rotation; `interference()` falls back to
`entity.name` so every pair reads `Body1 ↔ Body2`. Freehand API code re-steps on
those. A fixed op whitelist encodes the workarounds once, in
[`ops.py`](ops.py), and every future request inherits them.

So the analyst never sends code. It sends op names from the whitelist.

## Request schema

`fusion_bridge/request.json`:

```json
{
  "runid": "2026-08-17-001",
  "document": "Beni_SingleLegRig",
  "intent": "one line, human readable, why this run exists",
  "ops": [
    {"op": "census"},
    {"op": "mass_report"},
    {"op": "real_clashes", "args": {"min_vol_mm3": 0.5}},
    {"op": "bbox", "args": {"occ": "RIG_Carriage"}}
  ]
}
```

| Field | Meaning |
|---|---|
| `runid` | Names the output file. Analyst picks it; must be unique. |
| `document` | Asserted against the open document name. Mismatch aborts the whole run before any op executes. |
| `intent` | Recorded in the output. Makes the archive readable a month later. |
| `ops` | Executed in order. Each is `{"op": name, "args": {...}}`. |

## Response schema

`fusion_bridge/out/<runid>.json`:

```json
{
  "runid": "2026-08-17-001",
  "document": "Beni_SingleLegRig",
  "intent": "...",
  "aborted": false,
  "guard": {"ok": true, "checks": [...]},
  "results": [
    {"op": "census", "ok": true, "value": {...}, "stdout": "..."},
    {"op": "bbox", "ok": false, "error": "no occurrence named RIG_Carriage"}
  ]
}
```

Every op returns `ok`. A failed op does **not** stop the run — later ops still
execute, and the analyst sees exactly which one failed and why. `stdout` is
captured because most `rig_lib` functions report by printing.

## The guard — the part that is not optional

`guard` is populated on **every** run, before and after the ops, whether or not
the request asked for it. It asserts:

- `REF_GIM6010-8` bounding box reads Y **5.00 … 49.00**
- `REF_GIM4305-10` bounding box reads Y **61.50 … 94.50**

Source: `beni_single_leg_rig_design_record.md` §6.2, and the warning in
`CLAUDE.md`. If either fails, `guard.ok` is `false` and **every result in the
file is suspect** — the model has displaced its motor references and the clash
and mass numbers are being computed against wrong geometry. The analyst must
treat a failed guard as "no data", not as "data with a caveat".

Tolerance is 0.01 mm. It is an equality assert, not a range check.

## Read-only by default

Every op in the whitelist is read-only except those listed under **Mutating ops**
in [`ops.py`](ops.py), which additionally require `"confirm_mutate": true` at the
top level of the request. Pose changes count as mutating: `set_pose` writes
`transform2` on real occurrences.

The operator should refuse a request that asks for a mutating op without that
flag, rather than helpfully adding it.

## Conventions

- Units in JSON are **mm**, **grams**, **kg·m²**, **degrees** — matching the
  documents, not Fusion's internal cm/kg.
- Anything the analyst is going to quote into a document must appear as a number
  in this JSON. The analyst may not read a figure out of `stdout` prose and
  treat it as authoritative — `stdout` is for diagnosis, `value` is for citation.
- Output files are kept. They are the only audit trail of what the model actually
  said on a given date.
