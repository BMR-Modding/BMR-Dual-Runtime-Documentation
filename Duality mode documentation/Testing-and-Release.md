# Testing and release

[Guide index](../README.md) · [Test report template](../templates/TEST-REPORT.md) · [Evidence](./Evidence-and-Compatibility.md)

Validate the exact package you intend to ship. Keep FUSE and RailForge in separate test environments and fully close Railroader before changing the active runtime or files.

## Record the build under test

Record the game build, UMM version, runtime manifest and assembly versions, runtime DLL hashes, dependency versions, package/ZIP hash, and tested save/mode. Development builds may share a version such as `0.0.0`; the hash distinguishes the binary.

Verify installed files against the staged package. A new ZIP on disk does not mean the running game loaded it. Keep backups outside active discovery directories.

## Use separate evidence levels

| Level | What it establishes | What it does not establish |
| --- | --- | --- |
| JSON/schema and static references | Parseable data, supported shapes, expected IDs/references | Runtime acceptance or gameplay. |
| Metadata/IL inspection | Relevant classes, assembly scopes, methods, and code paths | Successful patch installation or Unity behavior. |
| Real reader/sorter/patcher tests | Behavior of the specific invoked runtime methods | Full bootstrap, rendering, production, or save portability. |
| Live startup | Correct active package, dependencies, initialization, and selected files | Every operational feature. |
| Gameplay and save/reload | Recorded scenarios on recorded builds | Untested scenarios, other builds, or cross-runtime migration. |
| Cross-runtime save migration | The explicitly tested migration scenario | General portability of all saves. |

Keep **PASS**, **FAIL**, **NOT TESTED**, and **NOT APPLICABLE** distinct. A skipped check is not a pass. Record user-reported tests as such when no detailed scenario/log was retained.

## 1. Static package review

- Both manifests use the intended ID/version.
- Every FUSE fragment exists and is explicitly declared.
- RF graphs and conditional payloads have the correct separate locations.
- Each logical payload has one active discovery path per runtime.
- Source-only files, alternate packages, and active legacy duplicates are absent.
- Required content providers use the correct IDs for each runtime.
- Native FUSE order targets are valid; asset-only providers are not blindly copied into them.
- All object and cargo references resolve against the intended baseline/providers.
- Geometry, recipes, units, storage, rates, filters, and conditions match except for documented differences.
- DLL references and initializer ownership have been reviewed, when code is present.

The [paired example](../examples/README.md) illustrates these checks on a small load definition; it does not cover a complete route mod.

## 2. Runtime methods and negative controls

When available, exercise actual manifest readers, dependency sorters, file selectors, serializers, and patch engines in an isolated process. Load only the required libraries; do not call a mod/game initializer as a substitute for an isolated test.

Test the failure you intend to catch: a missing provider, invalid asset-only order edge, duplicate payload, altered binding, or old failing implementation. Confirm the validator fails there and passes the corrected case.

For optional DLL adapters, verify real patch installation against the supported runtime assembly and inspect cleanup. Method names merely existing is weaker evidence than compatible signatures and successful installation.

## 3. Live acceptance in each runtime

| Scenario | Expected observation |
| --- | --- |
| Cold startup | Correct package active; intended files selected once; DLL initialized once. |
| Base layout | Tracks connected, spans highlight the intended rails, industries/scenery correctly placed. |
| Content resolution | Correct cargo IDs, assets, materials, and external providers. |
| Locked progression | Expansion objects unavailable while construction remains reachable. |
| Actual unlock | Costs/deliveries work; intended tracks/components activate; replaced production stops. |
| Operations | Correct load/unload, recipes, storage, filters, orders, and waybills. |
| Reload | Same state after full restart, including delayed object/feature replay. |
| Menu return/new world | No teardown billing or stale per-world state. |
| Optional providers | Intended behavior both absent and present, without duplicate initialization. |
| Multiplayer, if claimed | Host authority, client behavior, reconnection, and supported save state. |

Run Company and Sandbox checks where their behavior differs. Use real deliveries for acceptance; console completion alone does not exercise dispatch, spotting, or consumption.

## 4. Upgrades and save claims

Test an older mod save within the same runtime separately from a fresh game. Record changed IDs, alias behavior, and migration work. Test cross-runtime switching only on a copy and label that result separately.

For code storing state, check paid/unpaid or active/completed cases, multiple saves, and host-only writes where relevant. A restored earlier autosave contains earlier state; compare the actual checkpoint before diagnosing a duplicate action.

## 5. Package and publish

1. Stage only intended release files under one mod root.
2. Re-run relevant checks after the last data/code change.
3. Build the ZIP and compare its entries and file hashes with the validated staging directory.
4. Test the installation method you intend to advertise.
5. Write requirements per runtime, installation/upgrade steps, supported features, and known limits.
6. Keep development evidence available, but put player-facing instructions first.

Do not bundle game/runtime assemblies merely to satisfy a build or test environment. Supply your own distributable code/content and document external requirements.

## Revalidation triggers

Retest when changing the game, UMM, runtime, providers, DLL bindings, progression ownership, graph operators, identifiers, or asset lookup paths. Select checks tied to the change, then run both runtime regressions needed for the release claim.

A documentation edition can update guidance without claiming that every historical mapping has just been replayed in a live game.
