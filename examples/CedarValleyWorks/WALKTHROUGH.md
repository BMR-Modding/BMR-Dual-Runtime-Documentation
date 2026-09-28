# Build and convert Cedar Valley Works

[Example index](README.md) · [Recipes](RECIPES.md) · [Validation](VALIDATION.md)

The crate works receives unfinished crates, finishes them using shared storage, and loads finished crates for export. The interchange provides the district's exchange tracks. The public team track offers independent freight profiles. A delivery milestone opens a repair and fueling facility.

All production rates and money values are teaching values. Balance them with the car capacities, time scale and contracts in your actual game.

## 1. Start with package identity and discovery

The [Info.json](package/ExampleAuthor.CedarValleyWorks/Info.json) and [Definition.json](package/ExampleAuthor.CedarValleyWorks/Definition.json) share ID `ExampleAuthor.CedarValleyWorks` and version `1.1.0`.

FUSE's explicit `FuseDataFiles` selects `game-graph.fuse.json`. RailForge discovers `RailForge/game-graph/cedar-valley.json`. There is no DLL initializer and no duplicate legacy graph.

Rename the package to your own author/mod ID when adopting it. Replace `cvw-` and `cvw.` entity IDs consistently throughout both graphs before releasing your first version. After release, those IDs are saved identities: preserve them or write and test an intentional migration. A display-name change is not an ID migration.

## 2. Keep an entity map beside the graph

| Entity | ID / references | Purpose |
| --- | --- | --- |
| Area | `cvw-area` | Parent of all four industries |
| Main nodes | `cvw-n-m0` through `cvw-n-m7` | District lead |
| Main segments | `cvw-s-main-0` through `cvw-s-main-6` | Connections along the lead |
| Interchange | `cvw-interchange.exchange` → `cvw-p-interchange` | Yard loop exchange |
| Works | `cvw-works.receive / finish / ship` → `cvw-p-factory` | Shared receiving, production and loading |
| Construction | `cvw-works.construction` → `cvw-p-construction` | Temporary phase-owned component |
| Team track | `cvw-team.public` → `cvw-p-team` | Two public freight profiles |
| Engine service | `cvw-service.repair / parts / coal / diesel` | Repair and shared fuel storage |
| Service spans | `cvw-p-repair`, `cvw-p-fuel` | Physical service bindings |
| Service feature | `cvw-feature-service` | Gates `cvw-service-track`, industry and fixtures |
| Milestone | `ewh.sections.cvw-build-service` | Adds one section to the existing Company progression |

Dots in this table denote component references or object navigation as appropriate; they are not additional dictionary entries. FUSE's compact phase reference is exactly `cvw-works.construction`. Feature-rule component references use a different slash form, such as `cvw-works/receive`.

## 3. Build the tracks before the industries

A node is a position and orientation. A segment connects two nodes. A span describes the usable part of one or more connected segments. An industry component binds to spans, not directly to a node or display label.

The example includes a through lead, a loop between `m1` and `m6`, three base sidings and a branching service spur. Every node is reachable in the graph; no node has more than three incident segments. These checks establish topology, not train-safe geometry.

The factory segment illustrates the field conversion:

FUSE:

```json
{
  "startNodeId": "cvw-n-f0",
  "endNodeId": "cvw-n-f1",
  "style": "yard",
  "trackClass": "industrial",
  "speedLimit": 5,
  "groupId": "cvw-base-track"
}
```

RailForge:

```json
{
  "startId": "cvw-n-f0",
  "endId": "cvw-n-f1",
  "style": "Yard",
  "trackClass": "Industrial",
  "speedLimit": 5,
  "groupId": "cvw-base-track"
}
```

FUSE's `yard` and `bridgeSupportsSteel` flags are not copied into unsupported RF segment fields. The example expresses the intended RF appearance through `style` and `trackClass`. Gauge metadata is not proof of a working narrow- or dual-gauge RF track implementation.

The shared distance-based factory span is:

```json
{
  "upper": { "segmentId": "cvw-s-factory", "end": "A", "distance": 15 },
  "lower": { "segmentId": "cvw-s-factory", "end": "B", "distance": 15 },
  "normalize": true
}
```

The endpoints face inward. Each distance is measured from its named end; the lower endpoint here is **15 metres from B**, not 15 metres from A. The original factory segment was a straight 120-metre teaching segment, giving a nominal 90-metre usable span. The edited endpoints remain about 120 metres apart; the actual curve length must be measured in the editor. Recheck the span after adjustments. The normalized-location recipe retains the idealized 120-metre calculation as a separate exercise.

## 4. Distinguish world and industry-local coordinates

The [Andrews placement](PLACEMENT.md) now uses the edited entrance `(-30717.615161, 527.52, -20067.424680)`, with yaw `226.75°`. The area origin stays at `(-31008.959355, 527.52, -20341.499278)`. Nodes and scenery use world positions; the loader root uses the map's world-aligned parent in this example.

The crate works industry is at `(5.988070, 0, -35.554789)` relative to the area, giving world position `(-31002.971285, 527.52, -20377.054067)`. The area parent remains unrotated. This is the original industry marker: moving its track nodes does not move it automatically. Reposition the marker separately if you want it centered on the edited factory siding.

| Object | FUSE field | RF field | Space in this example |
| --- | --- | --- | --- |
| Track node | `position` | `position` | World |
| Area | `tracks.areas.<id>.position` | `areas.<id>.localPosition` | Root area transform |
| Industry | `operations.industries.<id>.position` | `areas.<area>.industries.<id>.localPosition` | Parent-local |
| Scenery | `position` | `position` | World |
| Loader fixture | `operations.loaders.<id>.position` | `loaders.<id>.position` | Loader parent; world-aligned in this example |

The FUSE root `coordinateSpace: "world"` is not permission to put world coordinates in the industry-local field. Inspected runtime paths assign these industry transforms locally.

For translation alone, move world positions and the area origin together; industry-local offsets stay unchanged. This placement also rotates the layout. Because the area parent stays unrotated, the builder rotates industry-local offsets as vectors without adding the world anchor to them. It rotates world points about the entrance and adds the heading to upright node/scenery/fixture rotations. Scene-clone transforms stay local to their own, separately chosen parents.

## 5. Define cargo before referencing it

The two custom loads are:

| ID | Name | Importable | Intended use |
| --- | --- | --- | --- |
| `cvw.unfinished-crates` | Unfinished Crates | Yes | Factory input and team-track receipts |
| `cvw.finished-crates` | Finished Crates | No | Factory output and team-track exports |

FUSE `operations.loads.<id>.name` becomes RF `loads.<id>.description`. Both use `Pounds`. The example retains density, weight, importability and payment fields explicitly.

A custom load definition is not a rolling-stock model or a visual cargo container. The example uses boxcar filters (`XM*`) and does not provide new car definitions. If a load needs a particular car body or container, supply and validate that asset separately.

Five stock loads are referenced: `repair-parts`, `coal`, `diesel-fuel`, `building-supplies` and `rails`. Their IDs were checked in the supplied vanilla graph; see the validation record.

## 6. Connect receiving, production and loading

`cvw-works` has four components:

| Component | FUSE type | Role |
| --- | --- | --- |
| `receive` | `unloader` | Unloads unfinished crates into shared storage |
| `finish` | `formulaic` | Consumes 20,000 pounds/day and produces 20,000 pounds/day |
| `ship` | `loader` | Loads finished crates from shared storage |
| `construction` | `progression` | Handles delivery orders while the service-yard phase is pending |

The receiver and shipper have 120,000-pound capacity, 60,000 transfer-rate values, and `storageChangeRate: 0`. The formula is the explicit production source; do not accidentally also give the loader a passive production rate.

FUSE formula:

```json
{
  "type": "formulaic",
  "name": "Crate Finishing",
  "sharedStorage": true,
  "inputTermsPerDay": { "cvw.unfinished-crates": 20000 },
  "outputTermsPerDay": { "cvw.finished-crates": 20000 }
}
```

RF changes the type to `Model.Ops.FormulaicIndustryComponent`. It does not add a span to the formula. The receiver and shipper convert `trackSpanIds` to `trackSpans` and keep their actual track bindings.

The two physical freight operations share the factory span in this compact example. In a larger plant, create separate receiving and loading spans and update both branches. Storage belongs to the industry; splitting these components into unrelated industries changes the storage design.

## 7. Add the interchange and team track

`cvw-interchange.exchange` uses FUSE `interchange` / RF `Model.Ops.Interchange` and the loop's span.

`cvw-team.public` uses FUSE `teamTrack` / RF `Model.Ops.TeamTrack`. Its keyed profiles describe inbound unfinished crates and outbound finished crates. `isExport` controls direction; `loadingTimeDays` is one day in both profiles.

Profile keys are stable tags, not arbitrary UI labels. Keep them when updating the package. RF can also accept an array of profiles with explicit tags; the core keeps the dictionary so identity remains obvious.

The team track's profiles represent independent public traffic. They are not a scripted transfer from the factory's storage. Interchange operation, car availability and contract generation must be checked in game.

## 8. Separate service logic from service visuals

The engine-service industry contains:

- A repair component using `repair-parts`, with overhaul enabled.
- A parts unloader feeding the same industry's shared storage.
- Coal and diesel unloaders bound to the fuel span.
- Three separate loader fixtures: water column, coal conveyor and diesel fueling stand.

The loader fixtures use verified stock prefab identifiers. FUSE binds them through `industryId`; RF uses `industry`. A coal conveyor visual by itself does not define a coal-receiving operation.

The core deliberately gates the **service industry**, its track group, and the physical fixtures together. The construction siding remains part of the base district.

Move the water column, coal conveyor and diesel stand through the editor's **Objects** panel. The [editor workflow](EDITOR-WORKFLOW.md#move-coal-water-and-diesel-through-objects) explains the saved scene overrides and why version 1.1.0 folds those poses back into the loader records.

## 9. Give the milestone ownership of construction

The example patches `progressions.ewh.sections`. It neither replaces the base section dictionary nor replaces Company start grants. A Company using another progression needs a deliberate equivalent section; simply declaring a custom progression does not select it.

The service phase costs 2,500 and requests two carloads of building supplies and two of rails at `cvw-p-construction`. The original S-shaped siding had no special operational meaning: its identity and span binding provide the function. After completion, the track remains while the phase-owned construction component retires.

The user's screenshot shows **Map Features → Cedar Valley Engine Service** enabled. That demonstrates the visible expansion, not completion of the delivery/payment milestone or persistence after reload.

FUSE phase reference:

```json
{
  "industryComponentId": "cvw-works.construction"
}
```

RF phase reference:

```json
{
  "industryComponent": {
    "areaId": "cvw-area",
    "industryId": "cvw-works",
    "componentId": "construction"
  }
}
```

FUSE deliveries contain `destinationIndustryId` and `direction: "loadToIndustry"`. RF expresses the destination through the phase component and uses `"LoadToIndustry"`.

The feature's `unlockIncludeIndustryComponents` is explicitly empty. The permanent service feature does not own `construction`. The delivery phase activates and retires that temporary component; a saved feature replay must not resurrect it.

Expected lifecycle, to test in each runtime:

| State | Expected behavior |
| --- | --- |
| New Company on `ewh` | Base district usable; service expansion locked |
| Phase pending | Construction orders use the existing construction siding |
| Phase complete | Service tracks, industry and fixtures enabled; construction component retired |
| Save/reload after completion | Service remains enabled; no new construction orders |
| Reload another map/save | No stale district objects or duplicate components |
| Sandbox | `initiallyEnabled/defaultEnableInSandbox: false` leaves the feature initially off; use the runtime's feature controls to test it |

Do not add the service feature to `enableFeaturesAtStart`; that would defeat the milestone. The separate start-grant recipe is for features intended to be available on every Company load.

## 10. Resolve assets deliberately

The works uses `scenery://freight-house-general` in FUSE and the catalog ID `freight-house-general` in RF. The service building similarly maps `scenery://brick-substation-medium` to `brick-substation-medium`.

Those exact mappings come from the existing dual runtime Whittier example. They are not a universal rule to strip URI prefixes. Check the loaded catalog for every asset you add.

For feature-controlled objects, FUSE references the service scenery's bare authored ID; RF uses `scenery://cvw-scenery-service`. The service loader IDs retain their known handler object names. Do not confuse a catalog model ID with an instance ID.

## 11. Extend one system at a time

The [recipes](RECIPES.md) show passengers and a station, a turntable/roundhouse, special component types, masks, splineys, water, telegraph poles, scene clones, removals, settings, optional content, audio, map tiles, spawns and migrations.

Each recipe declares its prerequisites and what has no direct counterpart. Resolve placeholders, merge only the relevant inner fragment at the indicated root, and update references in both branches. Recipe envelopes are not mod files.

### Optional DELTA45 exercise: buy, deliver and dispense oil

The [Bunker C recipe](recipes/16-bunker-c-freight.recipe.json) extends the same district. It defines a priced `bunker-c` load, adds `cvw-oil-supply` at the interchange, and adds `cvw-oil-receive` to the existing service industry. The service milestone still gates the whole industry.

Follow the complete chain: purchase the tank car, deliver it to `cvw-p-fuel`, unload into shared Bunker C storage, then test the existing diesel stand with a compatible oil-fuel slot. Test empty storage and the locked service-yard state as well.

The two fragments demonstrate matching freight data. DELTA45's stand and steam simulation are additional runtime behavior; FUSE needs independently verified locomotive support. The direct policy test confirms that RF preserves the explicit supplier and positive price, not that a locomotive has been refueled.

## 12. Turn the specimen into your mod

1. Copy the candidate package to your development project and assign your own stable IDs.
2. At the Andrews starting site, connect the entrance to verified map nodes and adjust turnout curves, grades and clearance. The [editor workflow](PLACEMENT.md#adjust-the-nodes-in-the-editor) explains how to retain these changes.
3. Inspect all stock and provider asset IDs in each runtime.
4. Adapt production, storage, car filters, contracts and the selected Company progression.
5. Run the supplied static/schema checks after each edit. If editing generated files, also update their example-specific builder or stop using it.
6. Install only your candidate package in a disposable test setup, one runtime at a time.
7. Drive every route, work freight, complete the milestone, save/reload, and test map teardown and multiplayer roles where relevant.
8. Record versions, package hashes and observed results before release.

Use the [release test report](../../templates/TEST-REPORT.md) and [conversion record](../../templates/CONVERSION-RECORD.md). Passing the provided parser tests is a useful checkpoint, not completion of those gameplay steps.
