# RailForge DELTA45: changes that matter to dual runtime authors

[Guide index](../README.md) · [Cedar Valley example](../examples/CedarValleyWorks/README.md) · [Evidence](Evidence-and-Compatibility.md)

Reviewed **21 September 2026**, comparing the user-supplied **1.99.DELTA45** archive with the **1.99.DELTA25** installation used by these guides.

**The existing paired graph layout still passes the offline checks.** The useful additions concern oil-fuel behavior, asset-pack discovery/resolution, vehicle animation diagnostics and the livery editor. This review found no reason to rewrite Cedar Valley's core graph or invent a new graph namespace.

## What to adopt

| Change | Practical effect | Action for a modder | Evidence level |
| --- | --- | --- | --- |
| Bunker C fuel and interchange purchasing | RF can register the fuel and add purchases at eligible interchanges | Use exact cargo identity, choose authored or RF-managed suppliers, and check price behavior | Pure policy tested; live purchases untested |
| Diesel-stand oil support | Compatible diesel service facilities can receive and dispense Bunker C separately | Deliver fuel into the stand industry's shared storage; test gates and empty storage | Runtime code inspected; live refueling untested |
| Oil-fired steam compatibility | Narrow native slot/hook support, including a verified GS4 pack exception | Preserve real dependencies and test the exact locomotive/provider versions | Code inspected; no locomotive simulation test |
| Catalog-only parts packs | Standalone RF discovery can accept `Catalog.json` + `Bundle` without `Definitions.json` | Keep the complete parts folders; do not create dummy Definitions solely for this path | DELTA25/45 discovery comparison tested |
| Sibling catalog references | RF has a restricted fallback for registered sibling packs | Preserve catalog identities and physical package structure | Code inspected; no Unity asset resolution test |
| Missing animation guards | A missing visual can be skipped with a specific diagnostic | Fix the matching Definition/bundle; inspect the affected animation even if the car loads | Code inspected |
| Livery editor filtering/performance | Scenery can be hidden from pickers; ambient effects can be suspended in the dedicated editor | Check editor filters before diagnosing a missing pack | Code inspected; UI not exercised |

The new [Bunker C recipe](../examples/CedarValleyWorks/recipes/16-bunker-c-freight.recipe.json) and [parts-pack recipe](../examples/CedarValleyWorks/recipes/17-catalog-only-parts.recipe.json) apply these findings to Cedar Valley.

## Bunker C: cargo, purchase destination, receiver, stand, locomotive

These are five separate responsibilities. Defining a load does not implement all five.

### Cargo identity and price

RF's policy uses exact ID `bunker-c`. If absent, its default load is:

```json
{
  "description": "Bunker C",
  "units": "Gallons",
  "density": 65,
  "unitWeightInPounds": 0,
  "importable": true,
  "payPerQuantity": 0,
  "costPerUnit": 0.12
}
```

This object belongs at RF `loads.bunker-c` if you deliberately author the load. Its FUSE counterpart is `operations.loads.bunker-c` with `name` instead of `description`.

An existing compatible load keeps a **positive** authored price. Missing, null or zero `costPerUnit` receives the `0.12` fallback. Zero therefore does not mean free Bunker C under this RF policy. A non-object record, differently cased cargo identity, incompatible units, nonpositive density, non-importable load or invalid negative price prevents automatic purchasing rather than authorizing replacement of that definition.

Use one owner for a shared load. When another pack supplies `bunker-c`, inspect and reuse that definition rather than blindly overwriting its economics.

### Automatic purchasing is conditional

The inspected policy needs:

- Exactly one recognized Interchange component in the industry.
- At least one existing InterchangedIndustryLoader purchase supplier.
- Usable interchange span IDs.
- No explicit industry exclusion, conflicting managed ID or separate authored oil supplier.

A bare interchange is insufficient. **Cedar Valley's core interchange is bare**, so the direct policy test adds the fuel but no automatic purchase destination there.

RF's generated supplier ID is `bmr-universal-bunker-c`, with exact filter `TM` and the interchange's resolved spans. Treat that ID as RF-owned; use your own ID for an authored supplier. An existing authored Bunker C supplier prevents the automatic duplicate.

Recipe 16 deliberately authors `cvw-oil-supply` in both formats. Its positive price and explicit supplier were preserved by the DELTA45 policy probe. The recipe defines freight parity; it does not assert FUSE locomotive oil-consumption support.

As a different RF-oriented design, author an ordinary diesel purchase supplier and let RF add its oil supplier. That automatic addition must be documented as an intentional runtime difference.

### Excluding an interchange

The runtime reads `ExcludedBunkerCInterchanges.txt` from **RailForge's own mod directory**, not every content mod's directory. The file contains exact industry IDs, one per line; blank lines and lines beginning with `#` are ignored. IDs compare case-sensitively. The reader accepts at most 512 distinct IDs, 128 characters per ID and 64 KiB of UTF-8 text.

```text
# Operator-maintained example; this file belongs beside RailForge's Info.json.
cvw-interchange
```

Do not silently ship or overwrite the operator's global exclusion file from a content mod. The built-in exclusion is `Oconalufty-RR-INT`. The runtime also checks the loaded selective-interchange exclusion contract; an unreadable exclusion configuration holds automatic purchasing.

The pure policy tests cover explicit and built-in ID exclusions. The on-disk exclusion reader and selective-interchange integration were inspected, not exercised against a live installation.

### Receiving and refueling

DELTA45's stand support targets native diesel `CarLoadTargetLoader` instances linked to an industry. A qualifying native diesel receiver has shared storage, no automatic load ordering, zero storage consumption, positive finite capacity/transfer rate, a filter matching `TM`, and valid unique spans.

The relevant authoring shape already exists in Cedar Valley's diesel component:

```json
{
  "type": "Model.Ops.IndustryUnloader",
  "name": "Service Diesel",
  "loadId": "diesel-fuel",
  "trackSpans": ["cvw-p-fuel"],
  "carTypeFilter": "TM*",
  "sharedStorage": true,
  "storageChangeRate": 0,
  "maxStorage": 16000,
  "carTransferRate": 60000,
  "orderAroundEmpties": false,
  "orderAroundLoaded": false
}
```

This matches the inspected configuration requirements, but the receiver and stand still need to materialize successfully in Unity. RF can create a corresponding Bunker C receiver with a generated `-rf-bunker-c` suffix, or use a suitable authored receiver. Recipe 16 demonstrates the authored receiver.

Fuel must be unloaded into that industry's Bunker C storage before dispensing. RF checks the selected car's exact oil slot, finite capacity/quantity, available fuel, active industry/component state and ownership. It retains the native diesel path. These are inspected safeguards, not a completed refueling acceptance test.

Both load and industry materializers must be enabled for this stand integration. Dedicated livery-editor sessions suspend the relevant service behavior.

For a progression-gated service yard, test that the receiver and stand stay unavailable before unlock, remain available after save/reload, and do not continue serving after their source industry is disabled.

### Oil-fired steam and Toolshed

The new steam runtime recognizes a constrained native car/tender design: exactly one required `bunker-c` slot and one required `water` slot, both in gallons with valid capacity. A required coal slot rejects this oil path. Exact native types, host authority, catalog identity, quantities and existing fuel-hook ownership also matter. The conversion constant in this build is `0.08` gallons per coal-pound equivalent; it is an implementation detail, not a new graph setting.

There is a **fingerprinted Southern Pacific GS4 1.0.1 exception**, not general Toolshed replacement:

- The scanner checks the exact package identity and an audited inventory of files, sizes and hashes.
- RF's oil hooks must be ready, with load materialization enabled.
- Only a missing, unbounded, exact `Toolshed` requirement receives this exception.
- Other Toolshed features and other dependencies are not supplied by that exception.
- Unknown competing steam-fuel hooks can hold RF's support. One specifically fingerprinted LSE 0.3.11 tender guard has an explicit compatibility path; that is not blanket LSE-version support.

Do not remove another mod's Toolshed requirement or rename a package to obtain admission. For a new locomotive, author and test the actual data/code integration on each runtime.

## Catalog-only parts packs and sibling references

DELTA25's standalone legacy discovery required both `Catalog.json` and `Definitions.json`. DELTA45 adds an alternative accepting a valid catalog with a nonempty `Bundle` file directly in the same folder.

A common package layout is:

```text
Your.Mod/
├── Info.json
├── MainAssets/
│   ├── Catalog.json
│   ├── Definitions.json
│   └── Bundle
└── Parts/
    ├── Catalog.json
    └── Bundle
```

The inspected standalone path checks the root and up to 256 immediate child directories. This is not a promise to recursively discover arbitrary folders. Native declared asset-pack folders use their own discovery path. Admission and UMM ownership checks still apply; this does not authorize RF to take over another active code loader.

Catalog preflight requires a nonempty string identifier, nonempty assets object and correctly typed optional catalog/asset fields. Missing, empty, misplaced or linked Bundle/Catalog files fail the relevant checks. Discovery does **not** establish that the bundle is a valid Unity export or contains the referenced asset.

The comparison test used a clearly marked one-byte Bundle stub outside Mods: DELTA25 did not discover that catalog-only child; DELTA45 did. Separate negative tests covered missing/empty bundles and malformed catalogs. No stub was installed or loaded by Unity.

The new sibling fallback resolves a simple requested **catalog identifier** against registered sibling stores under the same physical parent within the active Mods tree, during validation. Ambiguous catalog matches fail closed. It is not a global filename search or a substitute for declaring dependencies.

This reinforces the earlier advice: catalog identity and mounted store URI are different. Do not manufacture `railforge://` paths or rename catalog identities to resemble directories. FUSE's asset declaration and ordering rules remain separate.

## Missing vehicle animations now have specific recovery paths

Two new guards distinguish a recoverable visual defect from successful content:

| Diagnostic | Inspected behavior | Author action |
| --- | --- | --- |
| `RF-LOAD-ANIMATION-001` | Skips the affected load visual when the exact requested clip is missing; no replacement animation is selected | Check that `Definitions.json` and the model Bundle are the matching complete export; correct the clip reference |
| `RF-ASSET-026` | Removes unavailable brake-clip references before native visual setup continues | Restore the intended clip or remove the invalid visual reference; test visible brake motion |

The load guard matches a specific missing-clip `ArgumentException`. It does not claim to swallow arbitrary component failures. The brake guard's stated intent preserves physical braking while the absent visual cannot move. Neither guard is a reason to release a pack with broken animation references.

This is rolling-stock Definition/model validation, not a new game-graph field.

## Livery editor and other UI additions

The inspected build adds:

- A scenery filter for the livery/Definition asset picker, with paginated results and a persistent show-scenery preference.
- An asset panel and suspension of ambient effects in dedicated Definition-editor sessions unless enabled.
- Additional livery/grime appearance handling, home-menu appearance controls, a fourth vehicle-window color preference and global-chat implementation.

The first two are useful modder troubleshooting notes: a filtered scenery pack may still be loaded, and the quiet editor view is not proof that scenery/weather runtime behavior was removed. UI interactions, chat transport and visual appearance were not tested in this audit. They do not require additions to the core dual runtime graph.

## What stayed stable in this review

Cedar Valley's manifest discovery, FUSE typed reading, RF core patch merge, base-progression preservation and all 12 generic patch fixtures passed with DELTA45.

The direct assembly comparison found no method-instruction changes in `RailForge.RailForgeGraphPatcher` after normalizing build-specific embedded-data type identifiers. Startup integration around the patcher did change for fuel preparation, so this does not certify every lifecycle or saved-state scenario.

No new general `bunkerFuel`, `oilSteam` or settings root is introduced in the examples. The 432-property atlas remains an inventory of the same supplied **FUSE** schema.

## Validation and fingerprints

| Artifact | Identity |
| --- | --- |
| Supplied ZIP | `RF-DELTA45.zip`; SHA-256 `97BA737D037C437D5FE457FE58B6C37E52830AD45FACD187EC67D945B172263B` |
| DELTA45 DLL | Assembly `0.14.45.0`; SHA-256 `216422CFC49D34927ED1C7D8C9DDAA01FEA872F840D6BAA41B201F0F3F2FC469` |
| DELTA25 baseline DLL | Assembly `0.14.25.0`; SHA-256 `53C20C7B7D632E906F4AD62D635EBF141D12D4BD64DAA946C0A8B436DFBFB5A8` |

Results: **252 static example assertions; 482 combined schema/atlas/existing-runtime assertions using DELTA45; 38 new DELTA45 policy/discovery assertions; one DELTA25 catalog-discovery negative control.** The new-feature checks deliberately separate policy/scanner behavior from Unity materialization.

Reproduce in a fresh PowerShell process per runtime version, without installing the archive:

```powershell
pwsh -NoProfile -File ./examples/CedarValleyWorks/tools/Validate-Example.ps1 -GamePath "D:/SteamLibrary/steamapps/common/Railroader" -RailForgeAssemblyPath "C:/audit/DELTA45/RailForge.dll" -FuseSchema "C:/schemas/fuse-mod.schema.json"

pwsh -NoProfile -File ./examples/CedarValleyWorks/tools/Test-RailForge-Delta45.ps1 -GamePath "D:/SteamLibrary/steamapps/common/Railroader" -RailForgeAssemblyPath "C:/audit/DELTA45/RailForge.dll" -ScratchDirectory "C:/audit/fixtures"
```

Use `-BaselineCatalogOnly` with the DELTA25 DLL for the negative control. The feature probe is intentionally pinned to assembly `0.14.45.0` and writes only its scratch fixture folders. The original [validation boundaries](../examples/CedarValleyWorks/VALIDATION.md) still apply.

The supplied archive contained no release changelog. Findings above come from static comparison, targeted implementation inspection and the recorded probes, not inferred official release notes. The installed game, mods and saves were left unchanged. RailForge binaries and decompiled source are not included in the documentation.
