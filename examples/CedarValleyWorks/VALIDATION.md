# Cedar Valley Works validation

[Example index](README.md) · [Walkthrough](WALKTHROUGH.md) · [Recipes](RECIPES.md)

This record separates offline authoring checks, user-reported editor observations and operational acceptance. The earlier offline checks did not launch the game. Subsequent user screenshots and the supplied editor export are recorded separately below; no live mod or save was changed by this documentation update.

## Editor-adjusted example — 28 September 2026, version 1.1.0

- **308 static assertions passed**, including non-degenerate segment chords, the 40-metre entrance correction, all other source node records, loader pose parity, removal of competing scene overrides, source fingerprint and generator reproducibility.
- **482 schema/atlas/runtime-method assertions passed** against the same pinned FUSE schema, installed FUSE DLL and extracted DELTA45 DLL recorded below.
- **38 DELTA45 policy/discovery assertions passed** with the revised graph; no runtime initializer or Unity materialization was called.
- The unmodified [editor export](reference/editor-session-export.fuse.json) passes the public FUSE schema. Its schema validity did not detect the nearly zero-length entrance or the stale RF branch.
- The candidate package remains four JSON files. Both manifests and the FUSE graph identify version **1.1.0**.

Source export SHA-256: `4ec51185c1829115bae0e04163d589f438acc83613eda394ad0f9be46218b039`. [layout-overrides.json](layout-overrides.json) records the approved entrance correction and the loader overrides incorporated into their owning definitions.

The user screenshots show track/scenery rendering and the service feature enabled; the user reported finding loader placement under **Objects**. The screenshots do not identify both runtime builds or establish completed construction, fuel transfer, repair, save/reload or final approach geometry. See the [illustrated session](EDITOR-WORKFLOW.md).

The two override mappings were checked against supplied `FuseDevelopmentGroup-main.zip` sources: `FUSE/Runtime/API/LoaderAPI.cs` (`dab209124dddae42b8c7b32461dfc667b7b49ee55545fadc7145b21d4133d4f1`) and `SceneCloneAPI.cs` (`0ce9293c0267fecb4598e1deac7847763d3b167d40b9a6fe4114ca7156e58738`). Both assign the known root object's local pose. This source inspection is separate from the unchanged installed-binary parser tests.


## Andrews placement — version 1.0.1

The [placement update](PLACEMENT.md) uses entrance `(-30892.42, 527.52, -20231.87)` and yaw `226.75°` from the supplied screenshot. The user identified this as a flat open site near Andrews. The external reference node is not overwritten or automatically joined.

- **277 static assertions passed**, including exact anchor/heading, area/industry alignment, preserved lead/factory lengths, recipe transforms and graph reproducibility.
- A separate comparison with the archived pre-placement graph confirmed **all 171 node-pair distances** remain within 0.000003 metres of their previous values. Non-pose core data is unchanged except the description and version.
- **482 schema/atlas/runtime-method assertions passed** against the extracted DELTA45 DLL and installed FUSE; **38 DELTA45 policy/discovery assertions passed** with the relocated recipe.
- Both candidate manifests and the FUSE graph identify version `1.0.1`. Stable graph IDs, topology, span distances and milestone ownership are preserved.

The builders now read [placement.json](placement.json). Editor refinements are expected; once geometry is deliberately changed, update the teaching-layout assertions and generator source or preserve the edited graphs separately. The passes above describe the supplied placement, not future editor exports.

No Unity materialization, terrain/curve inspection, railroad connection, installation, gameplay or save testing was performed.

## DELTA45 follow-up

The original results below remain the DELTA25 baseline. The [DELTA45 review](../../Duality%20mode%20documentation/RailForge-DELTA45-Update.md) adds two recipes and records **252 static assertions, 482 schema/atlas/existing-runtime assertions against DELTA45, 38 new feature-policy/discovery assertions, and one DELTA25 negative control**.

[Validate-Example.ps1](tools/Validate-Example.ps1) now accepts `-RailForgeAssemblyPath` to test an extracted DLL without installing it. [Test-RailForge-Delta45.ps1](tools/Test-RailForge-Delta45.ps1) tests fuel policy and catalog-only discovery; run each version in a fresh PowerShell process. New-feature fixtures remain outside Mods, and their stub bundles are never loaded.

At that review stage, the core package was unchanged. The Andrews placement above is a separate transform update. DELTA45 DLL: assembly `0.14.45.0`, SHA-256 `216422CFC49D34927ED1C7D8C9DDAA01FEA872F840D6BAA41B201F0F3F2FC469`. Live refueling, steam simulation, graphics and saved-state acceptance remain untested.

## Original DELTA25 results

| Check | Result | What it establishes |
| --- | --- | --- |
| Static validator | **250 assertions passed** | JSON/duplicate-key checks, connected topology, references, counterpart mappings, gating declarations and graph reproducibility |
| Public FUSE schema | **Core, 14 recipe fragments and optional FUSE payload passed** | Correct schema shape for their enclosing documents |
| Audio recipe | **Known schema mismatch reproduced** | Working relative audio paths conflict with the public URI-only rule; URI-form alternate has valid structure |
| Field atlas | **432 values passed** | Every declared property-location specimen meets its individual property schema |
| Installed runtime probe | **30 assertions passed** | Discovery, typed FUSE reading, RF merging, preservation of base progression, patch fixtures and audio path behavior |
| Combined PowerShell check | **481 assertions passed** | The schema/atlas checks and runtime probe above, not 481 gameplay tests |
| Vanilla cargo IDs | **Five found in supplied vanilla graph** | `repair-parts`, `coal`, `diesel-fuel`, `building-supplies` and `rails` exist in that snapshot |
| Live game / assets / saves | **Not run** | No claim of playable placement, rendering, successful orders, progression or save migration |

The static count includes individual JSON files and may increase if reference files are added. The full-schema count does not treat the atlas's field values as complete independent mods.

## Exact evidence

| Input | Version / fingerprint |
| --- | --- |
| FUSE DLL | Assembly `0.0.0.0`; SHA-256 `9A30D165A89CDD0ED284B7424191F373BB91F28F8EC477AE4E4B17CEF5D0D807` |
| RailForge DLL | Installed `1.99.DELTA25`; assembly `0.14.25.0`; SHA-256 `53C20C7B7D632E906F4AD62D635EBF141D12D4BD64DAA946C0A8B436DFBFB5A8` |
| Public FUSE schema | `fuse-mod.schema.json` from supplied `FuseDevelopmentGroup-main/schemas`; draft 2020-12; SHA-256 `A7FA9464B56753962B57BF02A5F0DC0C657FAF986959380B09A75CBF78C8C5D7` |
| Schema identifier | `https://hunterr.dev/fuse/schemas/fuse-mod.schema.json` — identifier from the inspected file, not a claim that a remote copy is unchanged |
| Vanilla graph snapshot | Supplied `vanilla graph-data.json`; SHA-256 `4C897BFC48BEE8DFB2C02C56D8EE329B55A8990DCF995A0B01A6418A4FE2A341` |
| Schema validator | PowerShell `7.6.5`, `Test-Json` |
| Graph contracts | Existing [translation matrix](../../Duality%20mode%20documentation/FUSE-RailForge-Complete-Translation-Matrix.md), TRD/Whittier worked projects and supplied FUSE source/schema |

Neither game assemblies nor copyrighted audio/models are included. Historical matrix claims keep their original evidence scope; creating these specimens does not re-audit every RF handler.

## Reproduce the checks

Run from the `CedarValleyWorks` directory with Python 3.10+ and PowerShell 7.4+:

```powershell
python ./tools/validate-example.py
./tools/Validate-Example.ps1 -FuseSchema "C:/path/to/fuse-mod.schema.json"
./tools/Validate-Example.ps1 -GamePath "D:/SteamLibrary/steamapps/common/Railroader"
```

You may supply both PowerShell arguments together. The script expects FUSE under `Mods/FUSE` and RF under `Mods-Railforge/RTM.RailForge`. Use `-RailForgeAssemblyPath` for another RF DLL location, or adjust the FUSE path in the script for another installation layout. Its reflection calls target the inspected versions and can change across builds.

The runtime probe loads assemblies into its PowerShell process and calls discovery, serialization, patching and path-resolution methods. It does not call a mod initializer, create Unity objects, bootstrap the game, validate full dependency admission, or play audio.

Rebuild the teaching files:

```powershell
python ./tools/build-example.py
python ./tools/build-recipes.py
python ./tools/build-field-atlas.py --schema "C:/path/to/fuse-mod.schema.json"
```

These are example-specific builders, **not a universal converter**. Rebuilding overwrites their generated JSON/atlas files, so edit the builder if you want those changes to survive a rebuild.

## Audio finding

The installed private `FuseAudioAPI.ResolveAudioPath` returned:

| Input | Result relative to package |
| --- | --- |
| `Audio/cvw-bell.wav` | Correct `Audio/cvw-bell.wav` |
| `file(Audio/cvw-bell.wav)` | Correct `Audio/cvw-bell.wav` |
| `file://Audio/cvw-bell.wav` | Incorrect `file:/Audio/cvw-bell.wav` path beneath the package |

The public schema accepts the last form and rejects the first two. Recipe 13 uses the first. The test checks its expected schema rejection, then verifies that the same fields in URI form satisfy the schema. This is a **path-resolution result**, not an audio playback result.

A future FUSE fix should make the discrepancy assertion fail and prompt an update to this record. Do not silently remove the test or rewrite working audio paths based only on schema suggestions.

## Remaining in-game acceptance

Before calling an adapted mod playable, record both-runtime results for:

1. Terrain alignment, track curves, switch behavior, clearance and real railroad connection.
2. Stock/provider asset resolution, prefab placement and material rendering.
3. Interchange and team-track traffic, car filters, contract behavior, rates and storage.
4. Complete construction deliveries, payment, unlock, component retirement and save/reload.
5. Repair, overhaul, fuel deliveries and all three service fixtures.
6. Sandbox and the actual selected Company progression.
7. Map unload/reload and multiplayer authority if relevant.
8. Any optional recipe you adopt, including its provider, timetable, scene, audio or save prerequisites.

No cross-runtime save portability is implied.
