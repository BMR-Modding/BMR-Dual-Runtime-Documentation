# Documentation validation

## 28 September 2026 — Comprehensive GitHub edition

The [editor-adjusted example](examples/CedarValleyWorks/README.md) is now version 1.1.0. Its untouched source export, reviewed overlay and three user screenshots document the editor session. The near-zero entrance was corrected as approved; the coal/water object poses were normalized into loader records and both runtime branches now match.

Current checks: **308 static example assertions**, **482 schema/atlas/runtime-method assertions** against the pinned FUSE/DELTA45 inputs, and **38 DELTA45 policy/discovery assertions** passed. The source export also passed its full public FUSE schema check. See [the example record](examples/CedarValleyWorks/VALIDATION.md) for exact scope and fingerprints.

Documentation checks: **24 Markdown files, 212 local links/anchors, 62 balanced code fences, 30 JSON code examples and 33 JSON files** passed. External source URLs are retained as evidence links; the documentation checker validates repository-local links and anchors. User-reported visuals do not establish completed construction, actual refueling or save/reload acceptance.

## Run the portable checks

From the repository root, using Python 3.10+:

```powershell
python ./tools/validate-documentation.py
python ./examples/CedarValleyWorks/tools/validate-example.py
```

The [documentation checker](tools/validate-documentation.py) validates local links/anchors, JSON files and JSON code blocks, duplicate keys and closed fences. The example checker validates topology, references, runtime field mappings, source provenance, the edited poses and generator reproducibility.

For schema and actual runtime-method checks, provide your local inputs to [Validate-Example.ps1](examples/CedarValleyWorks/tools/Validate-Example.ps1). The historical atlas expects the exact pinned public schema hash. Use [Test-RailForge-Delta45.ps1](examples/CedarValleyWorks/tools/Test-RailForge-Delta45.ps1) only with the matching inspected build. Game/runtime binaries are not redistributed.


## 21 September 2026 — Andrews placement

Cedar Valley Works version 1.0.1 now uses the selected entrance near Andrews. The [placement validation record](examples/CedarValleyWorks/VALIDATION.md) reports 277 static assertions, 482 schema/atlas/runtime-method assertions and 38 DELTA45 policy/discovery assertions passing. A comparison with the pre-placement archive confirmed all 171 node-pair distances were preserved.

Documentation checks passed: **23 Markdown files, 185 local links/anchors, 62 balanced code fences, 30 JSON code examples and 31 JSON files**, with no duplicate keys. Git whitespace validation passed. These checks do not establish final in-game geometry or a connection to the existing railroad.

## 21 September 2026 — DELTA45 follow-up

The [DELTA45 review](<Duality mode documentation/RailForge-DELTA45-Update.md>) records the assembly comparison and targeted new-feature tests. The original counts below describe earlier prepared editions; the expanded set has two additional recipes and the new review guide.

The expanded documentation check passed: **22 Markdown files, 168 local links/anchors, 60 balanced code fences, 30 JSON code examples and 30 JSON files**, with no duplicate keys or Git whitespace errors.

## 21 September 2026 — Cedar Valley Works

The expanded fictional example has its own [validation record](examples/CedarValleyWorks/VALIDATION.md), including schema coverage, connected-graph checks, real runtime discovery/patch probes and a confirmed audio-path discrepancy. Its geometry and gameplay remain untested.

The documentation-wide check also passed: **21 Markdown files, 145 local links/anchors, 55 balanced code fences, 28 JSON code examples and 28 JSON files**, with no duplicate JSON keys. Git whitespace checks passed. The counts include the retained cargo example and historical source manifest.

## 20 September 2026 — Practical edition

This record concerns the prepared documentation edition and its new cargo example. It does not re-test every historical matrix mapping or certify a gameplay release.

## Documentation checks

All documentation checks passed: 16 Markdown files, 85 local links/anchors, balanced code fences, 22 JSON snippets plus 4 example JSON files, no duplicate object keys, exact seven-field cargo mapping, 10 pinned source links across 4 repository revisions, and clean Git whitespace validation.

Historical property-only JSON fragments in the technical guide were wrapped as complete JSON objects. Their stated insertion scopes remain important: a valid snippet is not necessarily a complete graph.

## Actual runtime-method check of the cargo example

**PASS: 16 checks**, using the FUSE and RF binaries identified below.

- RF accepts the two manifests without warnings and preserves package identity/version.
- RF native scanning selects exactly one graph and excludes the FUSE file.
- RF's real patch engine preserves the example load against a minimal loads graph.
- FUSE's declared-file resolver selects exactly its one file.
- FUSE's real serializer reads the example cargo and retains name, units, importability, and numeric values.
- Manifests match; no hard runtime/provider requirement or code initializer exists in this data-only example.

Libraries used:

| Runtime | Assembly version | SHA-256 |
| --- | --- | --- |
| FUSE | 0.0.0.0 | 9A30D165A89CDD0ED284B7424191F373BB91F28F8EC477AE4E4B17CEF5D0D807 |
| RailForge | 0.14.25.0 | 53C20C7B7D632E906F4AD62D635EBF141D12D4BD64DAA946C0A8B436DFBFB5A8 |

These methods ran in an isolated PowerShell process. No game/mod entry point, Unity object creation, installation, or save mutation was performed. This did not exercise full FUSE dependency admission, a complete game graph, a formal JSON-schema validator, live gameplay, or cross-runtime save migration.

The first probe attempt stopped at the FUSE reflection call because PowerShell passed a wrapped object instead of a string. After making the argument type explicit, all 16 checks passed. No example-content correction was required.

## Historical evidence

The individual project investigations and their test boundaries are recorded separately in [Evidence and compatibility](<Duality mode documentation/Evidence-and-Compatibility.md>).
