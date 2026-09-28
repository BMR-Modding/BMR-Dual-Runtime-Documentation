# Assets, identities, and coordinates

[Guide index](../README.md) · [Field matrix](./FUSE-RailForge-Complete-Translation-Matrix.md) · [Evidence](./Evidence-and-Compatibility.md)

Matching visual appearance or display names is not enough. Verify the provider, catalog, definition, actual asset, and placement used by each runtime.

## Keep the identities separate

| Identity | Example or purpose |
| --- | --- |
| Mod package ID | Used for provider requirements and ordering. |
| Catalog identity | Stable content identity from `Catalog.json`. |
| Mounted store identifier | Loader-assigned location/URI used to access the mounted store. |
| Definition ID | Identifies a model/material definition. |
| Asset ID | Identifies the resource inside a catalog/bundle. |
| Cargo ID | The load a visual/material matches. |

Do not infer one identity from another. A display label, folder name, and cargo ID may all differ.

## Case: RailForge mounted URI versus catalog ID

Load Dictionary 1.10.1 compared `store.Identifier` with `BMR.LoadDictionary.Scrap`. Under RailForge 1.99.DELTA25, the pack was actually mounted as:

```text
railforge://BMR.Load Dictionary/SCAssetPacks/BMR.LoadDictionary.Scrap
```

The correct pack was rejected, leaving an earlier matching scrap material selected. All installed files were current; reinstalling the same package would not fix the comparison.

The native catalog API provided stable identity:

```csharp
string catalogId = store.Catalog().identifier;
```

Here `Catalog()` returns an `AssetPack.Common.AssetPackCatalog` struct; its field is lowercase `identifier`. Referencing that type requires the appropriate native `AssetPack.Common.dll` at build time, not a new FUSE/RF dependency.

Validate the exact catalog, definition, asset, and cargo binding you intend to select. Handle a malformed unrelated catalog per store so it does not abort the search. Native downstream resolution can then return the real mounted URI for the selected definition. Avoid constructing guessed `railforge://` paths yourself.

This is a specific material-selection pattern, not an instruction to override every pack's priority.

## DELTA45: catalog-only parts and sibling references

The [DELTA45 follow-up](RailForge-DELTA45-Update.md#catalog-only-parts-packs-and-sibling-references) confirms a new standalone discovery alternative: a valid `Catalog.json` and nonempty `Bundle` can be admitted without `Definitions.json`. Keep complete parts folders; a dummy Definitions file is not required solely for that path.

The new sibling-reference fallback is restricted to registered physical sibling stores and catalog identity during validation. Duplicate matches remain ambiguous. This does not change FUSE registration/order rules or turn a mounted URI into a stable catalog ID.

For vehicle packs, DELTA45 can report `RF-LOAD-ANIMATION-001` or `RF-ASSET-026` and continue without a missing load/brake visual. A car loading successfully does not prove every animation works. Verify the Definition and model Bundle are a matched export.

## Make regression fixtures resemble mounted reality

Earlier tests exercised real Harmony/FUSE patch composition but supplied synthetic store IDs equal to catalog IDs. They missed the RailForge bug.

Useful fixtures include:

- an RF-style mount URI and a separate catalog identity;
- a renamed package folder with the same content catalog;
- both competing-store orders and relevant patch-registration orders;
- missing and malformed packs, including a failing catalog before a valid one;
- downstream resolution from the chosen definition to its actual store;
- unrelated cargos/materials that must retain their original result.

Native exact-definition lookup and visual cargo matching can use different keys. In the grain-pack work, a resolvable definition anchor was needed as well as cargo-specific material definitions. Verify the real lookup chain rather than assuming a catalog filename alias resolves a definition.

## Translate identifiers through actual catalogs

A FUSE `asset://` string is not automatically an RF model ID. Resolve the intended catalog record, then use the representation that the target reader accepts. The BMR scenery conversions used verified bare `modelIdentifier` values.

A DLL's fallback search for `railforge://` resources also needs auditing when moving to FUSE. Storm's trailer fallback is an example of an unresolved runtime-specific assumption. Blind prefix replacement does not prove the resource exists.

Check bundles, shaders, material rendering, scale, partial/full loads, and visibility in game after metadata tests. Successful mounting does not establish those results.

## Industry positions are local to their area in the inspected paths

TRD's original industry coordinates were world positions. The installed FUSE IndustryAPI parented them under Ela and assigned `transform.localPosition = definition.Position`; the `coordinateSpace` marker did not change that field's behavior. RF also assigned local industry positions.

For the verified unrotated/unscaled Ela parent, the correction was:

```text
local industry position = intended world position - area world origin
Ela origin              = (9465.46, 546.238831, 7468.69043)
Service world position  = (8860.813, 541.1123, 6245.82031)
Service local position  = (-604.647, -5.126531, -1222.87012)
```

This corrected both branches. It did not move track nodes, scenery, or facility transforms.

Do not subtract the area origin from every position field. Establish whether each field is world-space or parent-local in the actual implementation. If the parent has rotation or scale, simple subtraction is insufficient; use its full inverse transform.

Verify by reconstructing the intended world position and checking the industry's marker, facilities, spans, and interaction points in game. Preserve IDs and operational data while correcting placement.

## Case: moving service fixtures through Objects

In the Cedar Valley session, the user edited coal/water fixtures through **Objects**. The FUSE export contained both original loader records and `world.sceneClones` transforms targeting those same loader roots. Copying only the original loader dictionaries would lose the visible object edits.

For the two known `World/Loaders/<id>` targets, the reviewed loader and scene APIs set the same parent-local pose. Their unit-scale, source-less overrides were incorporated into the loader definitions for both runtime branches, removing the redundant `enabled: true` overrides. Milestone ownership stays with the service feature.

Inspect the actual target and coordinate space before doing this elsewhere. The [illustrated editor workflow](../examples/CedarValleyWorks/EDITOR-WORKFLOW.md#why-an-objects-edit-can-need-normalization) includes the saved poses and evidence limits.
