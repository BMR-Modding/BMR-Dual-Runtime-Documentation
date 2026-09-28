# Evidence and compatibility record

[Guide index](../README.md) · [Testing levels](./Testing-and-Release.md#use-separate-evidence-levels)

Reviewed for this documentation edition: **20 September 2026**, with focused example/audio and DELTA45 follow-ups on **21 September 2026**, and the supplied editor-export review on **28 September 2026**. These are observations about named builds and features, not an official compatibility promise or a declaration of the latest runtime versions.

## Runtime baseline

| Reference | Recorded identity | Scope |
| --- | --- | --- |
| Original FUSE proof of concept | `0.0.0+1eeef152ec57066bb7a90e1ef6edb27f6018e690` | East Whittier single-folder test, 4 September. |
| Original RF matrix/proof | `1.98.BRAVO99`; assembly `0.12.99.0` | Original field inventory, metadata/IL findings, and East Whittier case. |
| Later RF reference | `1.98.CHARLIE74`; assembly `0.13.74.0` | Focused Whittier reader/indexer/patch checks. An offline full-bootstrap attempt encountered a UMM API mismatch; it is not a successful bootstrap test. |
| Later RF reference | `1.98.DELTA07`; assembly `0.14.7.0` | Focused graph checks, component inspection, and optional captive-patch tests. |
| Later RF installation | `1.99.DELTA25`; assembly `0.14.25.0` | Focused dependency/content, progression, material-identity, and code-integration investigations. |
| Later inspected FUSE binary | Assembly `0.0.0.0`; hash below | TRD dependency/coordinate investigation, Load Dictionary checks, and Storm resolver inspection. |

The later FUSE binary's SHA-256:

```text
9A30D165A89CDD0ED284B7424191F373BB91F28F8EC477AE4E4B17CEF5D0D807
```

The later RF DLL hashes:

```text
CHARLIE74  87B0F13160F837C881BFA7BF20EEB0E9E94AF310EFD420FCB8DE396814B46FB3
DELTA07    10B0332E88C5151DA83C040728F17DC571720DFE816E9FA4DDBD5FA19FDA37F9
DELTA25    53C20C7B7D632E906F4AD62D635EBF141D12D4BD64DAA946C0A8B436DFBFB5A8
```

The matrix's original coverage is not retroactively upgraded to DELTA25. Later findings apply only to the stated methods, contracts, examples, and scenarios.

## Findings and evidence strength

| Finding | Evidence retained | Limit |
| --- | --- | --- |
| One package with separate graph branches | East Whittier runtime proof, 4 September | One runtime at a time; not arbitrary code portability. |
| Shared UMM DLL ownership | Whittier manifests, build/validation, and source notes | Real startup/lifecycle results must be tied to the exact package; not every historical Whittier version has both-runtime acceptance recorded. |
| Optional RF integration without a hard RF reference | Sequential Industry source, real Harmony installation against DELTA07/DELTA25, DELTA25 activation log, author gameplay reports | Two supported captive components; Pay4Resource excluded. |
| Asset providers accepted as requirements but rejected as native FUSE order targets | TRD 2.0.1: 23 real reader/admission/order checks including negative controls | Process-local provider/profile context; not live profile or asset rendering. |
| Industry coordinates local to the area | TRD inspected FUSE/RF implementations and reconstruction checks | Specific fields/paths; not a universal transformation of all coordinates. |
| Explicit service gate and phase ownership | TRD contract checks; Whittier replay investigation/regressions | Correct declarations still need Unity and saved-state acceptance. |
| Catalog identity differs from mounted RF URI | Load Dictionary 1.10.1 failure log, native/RF IL, old failing implementation, 1.10.2 regression and user visual confirmation | Earlier synthetic fixtures missed the real mounted state; visuals of 1.x do not prove later cargo-ID migration. |
| Teardown is not a billable departure | Whittier 0.3.38 guard, regression checks, recorded FUSE retest | No blanket claim for arbitrary billing mods or unrecorded RF scenarios. |
| Storm DLL binds to RailForge despite Railloader type names | Static metadata/IL and installed FUSE resolver inspection, 15 September | No converted package or live dual-runtime test produced. |

## Cedar Valley Works authoring checks — 21 September 2026

The new [fictional worked example](../examples/CedarValleyWorks/README.md) adds offline tests against the same FUSE and DELTA25 DLL fingerprints above. Its [validation record](../examples/CedarValleyWorks/VALIDATION.md) covers schema, graph references, native discovery, typed FUSE deserialization, RF patch behavior and preservation of base progression data. It does not establish live materialization or gameplay.

A direct call to installed `FUSE.Runtime.API.FuseAudioAPI.ResolveAudioPath` confirmed that package-relative audio and `file(...)` resolve correctly while the public-schema `file://` form does not. This is a narrowly scoped, reproducible audio-path finding, not a change to general asset URI rules.

## DELTA45 supplied-archive review — 21 September 2026

[The full review](RailForge-DELTA45-Update.md) compares `1.99.DELTA25` / assembly `0.14.25.0` with supplied `1.99.DELTA45` / assembly `0.14.45.0`. DELTA45 SHA-256 is `216422CFC49D34927ED1C7D8C9DDAA01FEA872F840D6BAA41B201F0F3F2FC469`.

Existing example probes pass on DELTA45. New tests exercise the pure Bunker C planner, the explicit Cedar Valley oil recipe, catalog preflight negatives and actual catalog-only discovery, with DELTA25 as a negative control. Refueling, steam hooks, animation guards, sibling lookup and editor UI were inspected but not run in Unity. The archive had no release changelog, and it was not installed.

## Cedar Valley editor observations — recorded 28 September 2026

The user's screenshots show the base district rendering, the service feature enabled, and subsequent track reshaping. The user found the existing service fixtures under **Objects**. The supplied folder's FUSE graph contained these edits while its RF graph retained the starter layout.

The [illustrated workflow](../examples/CedarValleyWorks/EDITOR-WORKFLOW.md) records these observations and the specific loader-override normalization. The revised four-file package has matching poses and passing offline checks. These observations do not establish both-runtime live acceptance, completed milestone deliveries, fuel/repair operation or save persistence.


## Case-study acceptance boundaries

### Tuckasegee River Distillery 2.0.1

Recorded offline work: 143 independent content/reference checks, 316 real discovery/patch/contract checks, and 23 FUSE admission/order checks. The user explicitly reported successful play in both FUSE and RailForge on 13 September.

That is an overall user-reported live result. Individual checklist steps, game modes, and cross-runtime save migration were not separately recorded. Do not turn the report into a claim that every scenario was observed.

### Whittier Central

The evidence notes cover named 0.3.x fixes and the 1.0.0 promotion. Shared UMM initialization, graph parity, progression ownership, and save-aware billing are implemented patterns. The 1.0.0 promotion retained the preceding gameplay payload; the promotion itself was not a new playtest.

Recorded FUSE teardown retesting belongs to 0.3.38. Historical checklists that say RF acceptance remains are not superseded merely by later packaging. Describe the actual version/scenario you have verified.

### Sequential Industry

The pre-persistence service behavior has author-confirmed return priority, captive conversion, normal completion/waybills, and multiplayer operation in their setup. Detailed broader host/client combinations were not recorded.

The 1.1.0 queue-persistence addition has automated/native binding coverage, but its real save/reload acceptance remains outstanding in the referenced notes. Earlier gameplay reports do not cover that new feature.

### Load Dictionary

The mounted-identity correction was visually confirmed under RF after 1.10.2. Later 2.0.0 introduced new namespaced cargo IDs, with separate automated checks and a general user confirmation of new loads. That later report did not identify every runtime/scenario and did not establish old-save migration.

### Storms Intermodal Yard 1.0.8

The audited DLL referenced `RailForge, Version=0.14.7.0` and three RF-scoped Railloader contract types. Its eight assembly references and 13 identified game patch-target names were inspected. Target-name existence is not full signature/patch verification.

DLL SHA-256:

```text
ECD72CBBD3E9E972DCC807D898FD0DFD58911AFF2B39794556C6A4CF26A342EA
```

The user-supplied package and local audit are not redistributed here. Its operational logic may be reusable, but initialization, settings, singleton behavior, trailer lookup, and external dependencies still need a verified port.

## Source register

These links are pinned to the repository revisions inspected for this edition. Some repositories require BMR access. The guides summarize the practical rules without requiring those files.

- [Whittier runtime differences](https://github.com/BMR-Modding/BMR-Whittier-Central/blob/659ec295b6102771aa1f1c1d63b00866eb0a92ec/BMR.Whittier.central%20-%20Duality/RUNTIME-DIFFERENCES.md), [acceptance record](https://github.com/BMR-Modding/BMR-Whittier-Central/blob/659ec295b6102771aa1f1c1d63b00866eb0a92ec/BMR.Whittier.central%20-%20Duality/TESTING.md), [change history](https://github.com/BMR-Modding/BMR-Whittier-Central/blob/659ec295b6102771aa1f1c1d63b00866eb0a92ec/BMR.Whittier.central/CHANGELOG.md).
- [Distillery runtime differences](https://github.com/BMR-Modding/BMR-Tuckasegee-River-Distillery/blob/e6e14d1951dd1c0ea84dde3da830de98ec2666bb/BMR.Tuckasegee%20River%20Distillery%20-%20Duality/RUNTIME-DIFFERENCES.md), [acceptance record](https://github.com/BMR-Modding/BMR-Tuckasegee-River-Distillery/blob/e6e14d1951dd1c0ea84dde3da830de98ec2666bb/BMR.Tuckasegee%20River%20Distillery%20-%20Duality/TESTING.md), [real FUSE admission tests](https://github.com/BMR-Modding/BMR-Tuckasegee-River-Distillery/blob/e6e14d1951dd1c0ea84dde3da830de98ec2666bb/BMR.Tuckasegee%20River%20Distillery%20-%20Duality/Test-FuseDependencies.ps1).
- [Load Dictionary RF identity investigation](https://github.com/BMR-Modding/BMR-Load-Dictionary/blob/527d9181a4acdb07cfe56f89e4328bdff53c97ac/BMR.LoadDictionary/source/aggregates/scrap/RAILFORGE-IDENTITY.md), [validation history](https://github.com/BMR-Modding/BMR-Load-Dictionary/blob/527d9181a4acdb07cfe56f89e4328bdff53c97ac/BMR.LoadDictionary/VALIDATION.md).
- [Sequential Industry coverage and acceptance](https://github.com/BMR-Modding/BMR-Sequential-Industry/blob/fa9f442bb70b30fbbd56c0f0520ecd3058af34ca/BMR.SequentialIndustry/README.md), [optional adapter source](https://github.com/BMR-Modding/BMR-Sequential-Industry/blob/fa9f442bb70b30fbbd56c0f0520ecd3058af34ca/BMR.SequentialIndustry/CaptivePatch.cs).

The original matrix additionally used the supplied FUSE schema, manifest schema, source and migration documents, and RailForge Full Guide/BRAVO99 DLL. Some RF schemas linked by that guide were unavailable; runtime-only and manual/provider labels remain intentional.

## Applying a finding to another build

Record the new binary identity, verify the relevant contract, reproduce the failure/negative control where practical, and run the applicable live scenarios. Update the evidence level and scope rather than changing "inspected" into "fully supported."
