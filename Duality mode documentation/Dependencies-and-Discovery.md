# Dependencies and discovery

[Guide index](../README.md) · [Quickstart](./FUSE-RailForge-Dual-Runtime-Quickstart.md) · [Evidence](./Evidence-and-Compatibility.md)

Separate three questions: **does the provider exist, in what order is its data applied, and who loads each payload?**

## Use the right dependency system

| Field | Owner and purpose | Practical boundary |
| --- | --- | --- |
| `Info.json.Requirements` | Generic UMM requirements; also audited by RF in the tested pattern | Every required item must make sense in both installations. Do not hard-require FUSE or RF for a package supporting either. |
| `Info.json.LoadAfter` | UMM ordering hint | It does not substitute for a required content provider or enforce FUSE data order. |
| `Info.json.FuseRequires` | FUSE data admission | Inspected native discovery can accept data providers, recognized replacement capabilities, and present non-data/asset providers. |
| `Info.json.FuseLoadAfter` / `FuseLoadBefore` | FUSE package ordering | Use valid targets for the selected discovery path. Do not assume UMM's optional ordering behavior. |
| `Definition.json.requires` | RF requirements | Use the RF edition's actual package ID and supported version bounds. |
| `Definition.json.loadAfter` / `loadBefore` | RF ordering | Order patches that depend on another provider's result. |

## Asset-only FUSE providers are the important exception

TRD 2.0.1's tests exercised the installed FUSE manifest reader and sorter:

- `BMR.LoadDictionary` was a native FUSE data package and a valid order target.
- `ALW.SceneryAssets.FUSE` and `C_L_B.ASSETS01` satisfied requirements as asset providers.
- Adding either asset provider to native `FuseLoadAfter` caused a blocking "no matching FUSE data package" error.
- Removing those two order edges, while keeping the requirements, admitted the package and ordered the dictionary before it.

Use this shape for that particular provider set. It is a manifest fragment, shown as a complete JSON object for clarity:

```json
{
  "Requirements": [],
  "LoadAfter": ["FUSE", "RTM.RailForge", "BMR.LoadDictionary"],
  "FuseRequires": [
    { "Id": "BMR.LoadDictionary", "NotBefore": "1.3.0" },
    "ALW.SceneryAssets.FUSE",
    "C_L_B.ASSETS01"
  ],
  "FuseLoadAfter": ["BMR.LoadDictionary"]
}
```

Replace the providers with your own verified dependencies. This is historical TRD configuration, not a recommendation to require these packs for every mod.

Native FUSE missing/disabled order targets can block admission. The inspected implementation has special handling for known runtime replacement capabilities and more permissive legacy advisory order references. Those exceptions do not make arbitrary native order edges safe.

## Version metadata is not proof of enforcement

The inspected native FUSE admission path reads `FuseRequires` into ID lists. A declared `NotBefore` was not established as an enforced minimum there. This qualification concerns that native package path; it is not a claim that every FUSE condition or legacy path ignores versions.

Keep accurate version declarations for intent and tooling, but check the actual provider version during validation and report the tested minimum. Test admission with a missing, disabled, and deliberately too-old provider before promising automatic rejection. Do not copy FUSE's limitation onto RF or a different FUSE build without inspection.

## DELTA45 has a narrow GS4 exception

The new RF oil-fuel integration includes an audited Southern Pacific GS4 1.0.1 package path. Only that fingerprinted data profile, with RF's oil hooks ready, can use the missing unbounded `Toolshed` requirement exception. Other Toolshed features, packs, versions and dependencies are not covered. See the [exact scope](RailForge-DELTA45-Update.md#oil-fired-steam-and-toolshed).

This does not change the rule for a new mod: declare the providers its actual behavior needs. Do not delete requirements to make admission succeed.

## Map provider identity explicitly

Use IDs from manifests, not folder names or display labels.

| Logical provider | FUSE ID | RF ID |
| --- | --- | --- |
| Example shared dictionary | `ExampleAuthor.Loads` | `ExampleAuthor.Loads` |
| Example separately packaged scenery | `ExampleAuthor.Scenery.FUSE` | `ExampleAuthor.Scenery` |

These are illustrative identities. Check your installed packages. A recognized provider ID does not prove that the required load, prefab, material, or component exists; validate content as well.

## Give each payload one discovery path

- Declare every FUSE fragment in `FuseDataFiles`. Do not rely on fallback scanning.
- Put ordinary RF graphs below `RailForge/game-graph`.
- Put conditional RF graphs outside that root and reference them once through the condition.
- Do not also retain an active equivalent legacy graph.
- Keep source backups and alternate versions outside the distributed package and active `Mods` directory.
- In the shared-UMM code pattern, keep one initializer; do not also declare it for RF.
- Check exact case, separators, and package-relative paths. Keep referenced files within the package.

The historical FUSE fallback chooses one eligible root file rather than all `.fuse.json` files. Explicit lists avoid both missing fragments and accidental fallback selection. See the [matrix](./FUSE-RailForge-Complete-Translation-Matrix.md#complete-fuse-infojson-field-inventory) for that version-specific behavior.

## Verify discovery and admission separately

A file resolver finding four FUSE files proves selection, not dependency admission. A JSON patch merging proves data behavior, not UMM startup. Test each stage independently:

1. Manifest identity and provider metadata.
2. Admission and dependency/order rules.
3. Exact selected filenames and count.
4. Graph merge and surviving object IDs.
5. One code initialization, if present.
6. Live assets and gameplay.

When diagnosing a failure, capture the actual active mod paths. An earlier TRD session still used the original installed package even though the new dual-runtime ZIP existed elsewhere. Hash the installed payload against the release you intend to test.
