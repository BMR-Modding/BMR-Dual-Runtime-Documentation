# BMR Dual Runtime Modding Guide

**Practical edition — 28 September 2026**

Build or convert a Railroader mod so one installed package works with **either FUSE or RailForge**, one runtime at a time. These community guides cover separate data branches, shared UMM code, dependencies, progression, assets, and release testing.

```text
Your.Mod/
├── Info.json                         FUSE discovery; optional UMM DLL entry
├── Definition.json                   RailForge manifest
├── content.fuse.json                 FUSE data
├── YourMod.dll                       optional shared UMM code
└── RailForge/
    └── game-graph/
        └── content.json              RailForge data
```

The graphs express the same intended behavior in different formats. A shared DLL is possible when its dependencies and lifecycle support both environments. Matching JSON, successful discovery, and working gameplay are separate things to verify.

## Start here

| Your task | Read next |
| --- | --- |
| Understand the folders and make a first package | [Quickstart](<Duality mode documentation/FUSE-RailForge-Dual-Runtime-Quickstart.md>) |
| Convert from FUSE, RailForge, or legacy | [Conversion workflows](<Duality mode documentation/Conversion-Workflows.md>) |
| Translate tracks, industries, scenery, and patches | [Technical guide](<Duality mode documentation/FUSE-RailForge-Dual-Runtime-How-To.md>) |
| Look up fields, arrays, handlers, or namespaces | [Translation matrix](<Duality mode documentation/FUSE-RailForge-Complete-Translation-Matrix.md>) |
| Keep or adapt a DLL | [Code mods and optional adapters](<Duality mode documentation/Code-Mods-and-Optional-Adapters.md>) |
| Fix missing providers or duplicate discovery | [Dependencies and discovery](<Duality mode documentation/Dependencies-and-Discovery.md>) |
| Preserve milestones, visibility, and saved state | [Progression and save lifecycle](<Duality mode documentation/Progression-and-Save-Lifecycle.md>) |
| Follow the Cedar Valley editor session, move service fixtures and preserve exports | [Illustrated editor workflow](examples/CedarValleyWorks/EDITOR-WORKFLOW.md) |
| Fix misplaced industries or incorrect assets | [Assets and coordinates](<Duality mode documentation/Assets-and-Coordinates.md>) |
| Prepare and verify a release | [Testing and release](<Duality mode documentation/Testing-and-Release.md>) |
| Check versions and supporting evidence | [Evidence and compatibility](<Duality mode documentation/Evidence-and-Compatibility.md>) |

## DELTA45 follow-up

[RailForge DELTA45 findings](<Duality mode documentation/RailForge-DELTA45-Update.md>) cover Bunker C fuel services, catalog-only parts packs, sibling asset lookup and missing-animation diagnostics. The existing core example still passes its offline runtime checks. Two optional recipes demonstrate the new authoring implications.

## Copyable starting points

- [Cedar Valley Works](examples/CedarValleyWorks/README.md): an editor-adjusted freight district near Andrews, paired version 1.1.0 graphs, an illustrated walkthrough, 17 syntax recipes and a 432-property field atlas.
- [Paired cargo example](examples/README.md): two manifests and two graphs defining the same cargo.
- [Conversion record](templates/CONVERSION-RECORD.md): inventory, provider mapping, intentional differences, and unresolved work.
- [Test report](templates/TEST-REPORT.md): exact builds, package hashes, observed results, and untested cases.

Examples are authoring material. Read their scope before installing them; do not copy this whole repository into `Mods`.

## Scope of this edition

The original East Whittier layout remains. Later work adds shared DLL ownership, optional adapters, native FUSE ordering rules, progression replay fixes, coordinate checks, and stable asset-catalog identification.

The matrix retains its historical field inventory with targeted corrections. It is **not a full re-audit of every field against every newer runtime**. Cross-runtime save migration needs a separate test. See the [changelog](CHANGELOG.md) and [evidence record](<Duality mode documentation/Evidence-and-Compatibility.md>).

## Provenance

Imported on 2026-09-20 from workspace baseline `f98af3a43f5cd418d8dc1d457007f2d4a68afbad`, including working-tree edits. [source-manifest.json](source-manifest.json) preserves the original import hashes; it is not a checksum manifest for this revised edition.

Some linked evidence repositories require BMR access. The guides explain the practical findings here so those links are supporting evidence, not prerequisites. No game or third-party assemblies are distributed. Existing attribution is retained; this update does not assign a new license.

[All BMR repositories](https://github.com/BMR-Modding/BMR-Modding)
