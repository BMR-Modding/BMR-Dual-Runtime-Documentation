# Syntax cookbook and coverage

[Example index](README.md) · [Walkthrough](WALKTHROUGH.md) · [Field atlas](reference/FUSE-FIELD-ATLAS.md) · [Translation matrix](../../Duality%20mode%20documentation/FUSE-RailForge-Complete-Translation-Matrix.md)

Every `*.recipe.json` file is a **teaching envelope** with a title, status, prerequisites, notes and optional `fuseFragment` / `railforgeFragment` objects. Copy only the relevant fragment into your authored graph, after satisfying its prerequisites. Do not install a recipe envelope or paste it below a literal `fuseFragment` root.

Recipes are alternatives. Several reuse a core span for illustration; applying all of them together would create conflicting operations. `REPLACE-...` values and fictional provider IDs are explicit unresolved references.

Recipe world positions follow the original [Andrews drawing frame](PLACEMENT.md); industry offsets follow that frame. Optional station/turntable/scenery recipes are not automatically fitted to the later edited track geometry. Scene-clone local transforms and generic field-atlas specimens retain their own coordinate meanings. Optional recipe geometry still needs fitting to the site.

## Recipes

| File | What it demonstrates | Boundary |
| --- | --- | --- |
| [01 Partial and replacement patches](recipes/01-partial-and-replace.recipe.json) | Partial component updates, capacity change, span append/clear, whole component replacement | FUSE list semantics differ from RF ordinary arrays |
| [02 Track locations](recipes/02-track-locations.recipe.json) | Normalized versus distance locations, inward ends, partial preservation flags | Actual curve lengths and unsupported metadata require review |
| [03 Passengers and station](recipes/03-passengers-and-station.recipe.json) | Passenger component, timetable code, branches, population, neighbors, physical station | Supply real branch/neighbor topology and final area order |
| [04 Turntable](recipes/04-turntable.recipe.json) | Turntable, three-stall roundhouse, prefabs, flattened RF fields | Connect verified generated helper nodes; custom visual fields are not portable |
| [05 Special components](recipes/05-special-components.recipe.json) | Interchanged loading, teleport loading, captive conversions, Pay4Resource and Empty | Check loaded types/providers; choose a coherent operating design |
| [06 Masks and labels](recipes/06-masks-and-labels.recipe.json) | Circle, rectangle and curve masks; styled speed label | RF curve geometry needs fitting; label text does not enforce speed |
| [07 Splineys and water](recipes/07-splineys-and-water.recipe.json) | Roads, river, trestle, repeated scenery, pond polygon | Replace loaded profiles/styles; no verified RF water-polygon pair |
| [08 Scene manipulation](recipes/08-scene-clones-and-suppression.recipe.json) | Clone, local transform, hide a scene path | Inspect actual scene paths; hiding is not deleting |
| [09 Removals](recipes/09-removals.recipe.json) | Track, industry, scenery and spliney removals | Remove dependents first; RF tombstones apply only to supported collections |
| [10 Settings and conditions](recipes/10-settings-and-conditional-content.recipe.json) | FUSE setting, feature rule, provider conditions | RF needs a separate settings implementation or variant |
| [11 Company start grant](recipes/11-company-start-grant.recipe.json) | Preserve existing start grants while adding one feature | The core's milestone feature must not be start-granted |
| [12 Telegraph poles](recipes/12-telegraph-poles.recipe.json) | FUSE line, RF individual pole, paired movement arrays | Expand the line and wire graph; replace placeholder pole indices |
| [13 Audio](recipes/13-audio.recipe.json) | Whistle, horn envelopes and bell timing | Real audio required; confirmed FUSE schema/path discrepancy |
| [14 Map packages](recipes/14-maps-tiles-and-spawns.recipe.json) | Selectable map, tile source, global spawn | Supply real map files; RF sidecar layout differs |
| [15 Save migrations](recipes/15-migrations.recipe.json) | Destination and property renaming | Test an old save; RF carTypes/object targets have no FUSE execution parity |

Additional reference files:

- [RF audio catalogs](recipes/audio-catalogs.reference.json): three separate root arrays plus their manifest mixinto declarations.
- [RF-only surfaces](recipes/rf-only.reference.json): Company starts, terrain strokes, infrastructure overrides, migrations, container addressing and rolling-stock Definition components. Each entry states its placement. Payloads with placeholders are sketches requiring real exported identity; they were not materialized.
- [Patch fixtures](fixtures/rf-patch-cases.json): one small base document, 12 independent patches and exact expected outputs, exercised with the real RF patch engine.

## DELTA45 additions

| File | What it demonstrates | Boundary |
| --- | --- | --- |
| [16 Bunker C freight](recipes/16-bunker-c-freight.recipe.json) | Exact cargo identity, authored purchase supplier and shared service storage in both graph formats | Freight data does not provide FUSE oil-steam simulation; RF refueling needs live acceptance |
| [17 Catalog-only parts](recipes/17-catalog-only-parts.recipe.json) | Catalog specimen, sibling AssetReference and package layout | Real exported Bundle required; new standalone discovery is specific to DELTA45 |

Read the [DELTA45 guide](../../Duality%20mode%20documentation/RailForge-DELTA45-Update.md) before adopting either. A bare interchange does not automatically gain an oil purchase supplier; an explicit supplier is preserved. A catalog-only pack can pass discovery without proving that Unity can load its bundle.

## Patch operator coverage

| Operator / behavior | Fixture |
| --- | --- |
| Ordinary array replaces | `plain-array-replaces` |
| `$replace` | `replace` |
| `$remove` on array / match | `remove-array`, `find-remove` |
| `$add` | `add`, `find-fallback` |
| `$append` | `append` |
| `$find` selector | `find-patch` |
| `$optional` missing match | `optional-miss` |
| `$clone` | `clone` |
| `$moveTo` | `move` |
| Mixed command and literal array | `mixed-program` |

These are **patch-engine fixtures**, not Railroader graph namespaces. Their `rows` field keeps merge behavior visible without requiring a game object. The fixtures are independent; reset to `base` before each case.

Selectors can use equality, inequality, prefix, suffix and contains comparisons; see the matrix for aliases and numeric values. `$optional` applies to a missing find, not arbitrary missing providers or objects. `$objectsByIdentifier` belongs to asset-container patches, not the game graph.

## Full FUSE property coverage

The [field atlas](reference/FUSE-FIELD-ATLAS.md) contains 432 declared property locations with example values and schema constraints. It includes:

- Package/root metadata, selectable maps, mixintos and version constraints.
- Nodes, segments, locations, spans, areas and removal requests.
- Loads, every declared industry-component property, team profiles and passenger branches.
- Loader fixtures, stations, turntable visuals and roundhouses.
- Scenery, splineys, water polygons, telegraph lines/movement, labels, masks, tiles, spawn points and scene clones.
- Progressions, sections, deliveries, feature arrays, string/list patch forms.
- All setting types/scopes, comparison operators and feature-rule target collections.
- Audio profiles, layers/keyframes, editor metadata and open extension points.

An open-ended field such as `extensions` or custom component `fields` does not define every provider's schema. Its owner must document the actual names, types and lifecycle. Empty dictionaries in the atlas demonstrate allowed JSON values; they do not promise useful behavior.

## RF coverage and honest gaps

The [matrix's graph-root union](../../Duality%20mode%20documentation/FUSE-RailForge-Complete-Translation-Matrix.md#2-complete-graph-root-namespace-union) remains the full RF/FUSE namespace index. This example adds copyable context, rather than claiming a new universal RF schema.

| Surface | Example coverage |
| --- | --- |
| `tracks`, `loads`, `areas/industries` | Complete connected core |
| `scenery`, `loaders`, `mapLabels` | Core plus richer alternatives |
| `mapFeatures`, `progressions` | Core milestone plus start-grant recipe |
| `splineys` | Explicit station, turntable, flowy, trestle, mask, telegraph, terrain and infrastructure specimens |
| `mandelas` | Clone/transform/hide recipe |
| Audio catalogs, spawn points, maps, migrations, Company starts | Separate file/manifest examples; never invented graph roots |
| Containers and rolling-stock components | Placement/envelope examples; actual asset Definitions still required |
| Legacy aliases | Normalize using the matrix; new core uses canonical forms |
| Undocumented `texts`, dynamic `BuildSpliney`, DKW/KRE, CLB shops and arbitrary providers | Known families acknowledged; no invented complete data contract |

FUSE water surfaces, native settings/rules, some turntable visuals, industry rotation/order and several metadata fields have no general verified RF counterpart. RF terrain brushes, Company-start plans and some save migration forms likewise lack a matching native FUSE graph contract.

## Audio path exception found while building this example

The public FUSE schema uses its URI definition for `clip` and `file`. However, the tested FUSE resolver treats `file://Audio/cvw-bell.wav` as a path under a literal `file:` directory. Both `Audio/cvw-bell.wav` and `file(Audio/cvw-bell.wav)` resolve to the intended package-relative file.

Recipe 13 therefore uses the working **package-relative** form and declares `schemaStatus: "known-audio-path-mismatch"`. The validator expects that schema rejection, then separately checks its URI-form structure. The atlas still represents the public schema accurately. Neither check proves that a WAV is present or playable; no audio is bundled.

Do not change all scenery or prefab URIs because of this audio-specific finding. See the exact runtime fingerprint in [Validation](VALIDATION.md).
