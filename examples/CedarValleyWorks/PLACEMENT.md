# Cedar Valley Works at Andrews

[Example index](README.md) · [Editor workflow](EDITOR-WORKFLOW.md) · [Walkthrough](WALKTHROUGH.md) · [Validation](VALIDATION.md)

Version **1.1.0** uses the supplied editor export near Andrews. Its FUSE graph had edited tracks and loader overrides; its RF graph still had the starter layout. The reviewed poses now feed both generated graphs.

| Reference | Value |
| --- | --- |
| Current entrance node | `cvw-n-m0` |
| Current entrance world position | `(-30717.615161, 527.52, -20067.424680)` |
| Entrance Euler rotation | `(0, 226.75, 0)` degrees |
| Next node | `cvw-n-m1` at `(-30746.75, 527.52, -20094.832)` |
| Entrance segment | `cvw-s-main-0`; 40-metre chord after correction |
| Area origin | `(-31008.959355, 527.52, -20341.499278)` |
| Original site reference | `N_BMR_ARR_KCM_004` at `(-30892.42, 527.52, -20231.87)` |

The original reference is retained as provenance. It is not the current entrance and is not an external node dependency in the package. The district has no authored connection to the surrounding railroad.

## Adjust the nodes in the editor

1. Copy only the four-file [candidate package](package/ExampleAuthor.CedarValleyWorks) into your development setup, using one runtime at a time.
2. Find the current entrance above. Adjust node positions and headings while preserving IDs unless deliberately changing topology.
3. Inspect the real railroad's node IDs and ownership before joining the approach. Two different IDs at the same position are not a connection.
4. Recheck spans, switch geometry and clearance. The validator rejects nearly zero-length endpoint pairs, but cannot certify safe curves.
5. Move fixtures through **Objects**, and adjust industry markers separately. Follow [the editor workflow](EDITOR-WORKFLOW.md).
6. Save/export and inspect both runtime files. The supplied session changed FUSE only; the presence of both files in a folder did not keep them synchronized.

The service milestone gates the repair/fuel spur, service industry and fixtures. Enable the service feature to inspect that geometry, then test actual progression separately.

## Rebuild without losing the edited layout

[layout-overrides.json](layout-overrides.json) is the reviewed source of node records, three default gauge fields and loader poses. It applies after the original drawing and before the generated files are written. [The untouched editor export](reference/editor-session-export.fuse.json) is evidence, outside runtime discovery; it still contains the entrance defect and competing scene overrides.

Run from this example directory:

```powershell
python ./tools/build-example.py
python ./tools/build-recipes.py
python ./tools/validate-example.py
```

To retain later editor edits, update the reviewed overlay and its provenance, or adopt your exported graphs as your own source and stop rebuilding with this example generator. Changes to generated package files alone are overwritten on rebuild.

The builder supports this example's known IDs and mappings. A changed node set or unsupported overlay property requires a deliberate topology/conversion update; it is not a universal importer.

## Coordinate frames and further relocation

[placement.json](placement.json) still records the original drawing frame for the area, industries, scenery and optional recipes. Its original entrance fields describe the first placement, not the current `cvw-n-m0` pose. The editor overlay contains final poses at that reference placement.

Changing only `placement.json` would move some content while leaving the overlay behind, so the builder rejects a mismatch with `layout-overrides.json`'s `referencePlacement`. For another site, transform the edited nodes and loader poses, the other world content, the area origin and the relevant recipe positions together, then update both reference records.

Industry positions remain area-local. Scene-object `localPosition/localRotation` values belong to the selected object's parent. The two normalized loader overrides target the same loader roots used by FUSE's loader API; that specific fact permits transferring their poses directly. It is not a rule for copying arbitrary scene-local coordinates into world fields.

## What changed during normalization

- Extended `cvw-n-m0` 40 metres back from `cvw-n-m1` along the existing heading, as approved by the user. Their exported separation was about 0.0028 metres.
- Retained the other 18 node records, including edited switch-stand flags.
- Preserved the three FUSE `gauge: "Standard"` fields; omitted them from RF because the established mapping has no general gauge counterpart.
- Incorporated the coal/water Objects poses into their loader definitions and synchronized those records with RF.
- Removed the redundant loader scene overrides, including their `enabled: true` instructions, so the service feature remains the declared visibility owner.
- Retained area/industry positions, freight logic, IDs, span distances, scenery and progression definitions. No engine shed was present in the export.

The screenshots precede this normalization. Final approach geometry, fixture reach, the railroad connection, freight operations and the complete milestone lifecycle still require in-game checks.
