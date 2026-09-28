# FUSE field atlas

[Example walkthrough](../README.md) · [Recipe index](../RECIPES.md) · [Translation matrix](../../../Duality%20mode%20documentation/FUSE-RailForge-Complete-Translation-Matrix.md)

This inventory covers **432 declared property locations** in the supplied public FUSE schema, including nested objects. It is generated from schema ID `https://hunterr.dev/fuse/schemas/fuse-mod.schema.json`, SHA-256 `a7fa9464b56753962b57bf02a5f0dc0c657faf986959380b09a75cbf78c8c5d7`.

Each row demonstrates the JSON value of **one field**. Values are syntax specimens, not one combined game graph. IDs, scene paths, profiles, controllers and assets must resolve in your actual package. Defaults in the schema are not proof of runtime support or sensible gameplay.

Mutually exclusive forms remain separate: choose distance **or** normalized track locations; assetIdentifier **or** prefab for object lines; one mask shape; one setting type. Read the connected core and recipes before combining fields.

The machine-readable [examples](fuse-field-examples.json) preserve exact schema pointers. `Validate-Example.ps1 -FuseSchema <path>` checks every value against its own property schema; that does not validate referenced game objects or the enclosing component's behavior.

## root

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `root.$schema` | `"cvw-example"` | string |
| `root.schemaVersion` | `"1.0"` |  |
| `root.id` | `"cvw-example"` | id; string; pattern=^[A-Za-z0-9][A-Za-z0-9._:-]*$ |
| `root.name` | `"Cedar Valley Works"` | string |
| `root.author` | `""` | string |
| `root.modVersion` | `"1.0.0"` | string |
| `root.railroaderVersion` | `"cvw-example"` | string |
| `root.description` | `"Fictional syntax example."` | string |
| `root.tags` | `[]` | stringArray; array |
| `root.coordinateSpace` | `"world"` | string; enum: world |
| `root.map` | `{"mapFolder":"Maps/CedarValley"}` | map; object |
| `root.mixinto` | `{}` | mixinto; object |
| `root.tracks` | `{}` | tracks; object |
| `root.operations` | `{}` | operations; object |
| `root.world` | `{}` | world; object |
| `root.audio` | `{}` | audio; object |
| `root.progression` | `{}` | progression; object |
| `root.settings` | `{}` | settings; object |
| `root.featureRules` | `{}` | featureRules; object |
| `root.editor` | `{}` | editor; object |
| `root.extensions` | `{}` | object |
## vec3

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `vec3.x` | `1` | number |
| `vec3.y` | `1` | number |
| `vec3.z` | `1` | number |
## map

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `map.displayName` | `"Cedar Valley Works"` | string |
| `map.description` | `"Fictional syntax example."` | string |
| `map.mapFolder` | `"Maps/CedarValley"` | string |
| `map.suppressBaseWorld` | `true` | boolean |
## mixinto

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `mixinto.target` | `"cvw-example"` | string |
| `mixinto.sourceFile` | `"file://Audio/cvw-example.wav"` | string |
| `mixinto.requires` | `[]` | array |
| `mixinto.conflictsWith` | `[]` | array |
## modRequirement

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `modRequirement.id` | `"cvw-example"` | string |
| `modRequirement.notBefore` | `"cvw-example"` | string |
| `modRequirement.notAfter` | `"cvw-example"` | string |
## settingDefinition

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `settingDefinition.type` | `"bool"` | string; enum: bool, boolean, enum, choice, select, number, float, double, int, integer, path, file, folder, color, colour, text, string |
| `settingDefinition.label` | `"cvw-example"` | string |
| `settingDefinition.description` | `"Fictional syntax example."` | string |
| `settingDefinition.scope` | `"user"` | string; enum: user, local, client, profile, modset, mod-set, server, shared, multiplayer |
| `settingDefinition.default` | `"cvw-example"` |  |
| `settingDefinition.values` | `[]` | stringArray; array |
| `settingDefinition.min` | `1` | number |
| `settingDefinition.max` | `1` | number |
| `settingDefinition.step` | `1` | number |
| `settingDefinition.advanced` | `false` | boolean |
| `settingDefinition.reloadRequired` | `false` | boolean |
## featureRule

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `featureRule.setting` | `"cvw-example"` | id; string; pattern=^[A-Za-z0-9][A-Za-z0-9._:-]*$ |
| `featureRule.operator` | `"equals"` | string; enum: equals, notEquals, greaterThan, greaterThanOrEqual, lessThan, lessThanOrEqual |
| `featureRule.value` | `"cvw-example"` |  |
| `featureRule.targets` | `{"trackNodes":[]}` | featureTargets; object |
## featureTargets

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `featureTargets.trackNodes` | `[]` | stringArray; array |
| `featureTargets.trackSegments` | `[]` | stringArray; array |
| `featureTargets.trackSpans` | `[]` | stringArray; array |
| `featureTargets.trackAreas` | `[]` | stringArray; array |
| `featureTargets.loads` | `[]` | stringArray; array |
| `featureTargets.industries` | `[]` | stringArray; array |
| `featureTargets.industryComponents` | `[]` | stringArray; array |
| `featureTargets.loaders` | `[]` | stringArray; array |
| `featureTargets.turntables` | `[]` | stringArray; array |
| `featureTargets.stations` | `[]` | stringArray; array |
| `featureTargets.scenery` | `[]` | stringArray; array |
| `featureTargets.splineys` | `[]` | stringArray; array |
| `featureTargets.waterSurfaces` | `[]` | stringArray; array |
| `featureTargets.telegraphPoles` | `[]` | stringArray; array |
| `featureTargets.mapLabels` | `[]` | stringArray; array |
| `featureTargets.mapMasks` | `[]` | stringArray; array |
| `featureTargets.mapTiles` | `[]` | stringArray; array |
| `featureTargets.sceneClones` | `[]` | stringArray; array |
| `featureTargets.progressions` | `[]` | stringArray; array |
| `featureTargets.mapFeatures` | `[]` | stringArray; array |
| `featureTargets.whistles` | `[]` | stringArray; array |
| `featureTargets.horns` | `[]` | stringArray; array |
| `featureTargets.bells` | `[]` | stringArray; array |
## tracks

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `tracks.nodes` | `{}` |  |
| `tracks.segments` | `{}` |  |
| `tracks.spans` | `{}` |  |
| `tracks.areas` | `{}` |  |
| `tracks.removals` | `{}` | trackRemovals; object |
## trackRemovals

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `trackRemovals.nodes` | `[]` | idArray; array |
| `trackRemovals.segments` | `[]` | idArray; array |
| `trackRemovals.spans` | `[]` | idArray; array |
## trackNode

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `trackNode.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `trackNode.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `trackNode.flipSwitchStand` | `false` | boolean |
| `trackNode.isDiamond` | `false` | boolean |
| `trackNode.groupId` | `"cvw-example"` | idRef; string |
| `trackNode.tags` | `[]` | stringArray; array |
## trackSegment

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `trackSegment.startNodeId` | `"cvw-example"` | idRef; string |
| `trackSegment.endNodeId` | `"cvw-example"` | idRef; string |
| `trackSegment.style` | `"standard"` | string |
| `trackSegment.trackClass` | `"main"` | string |
| `trackSegment.speedLimit` | `45` | integer; minimum=0; maximum=80 |
| `trackSegment.priority` | `0` | integer |
| `trackSegment.groupId` | `"cvw-example"` | idRef; string |
| `trackSegment.tags` | `[]` | stringArray; array |
| `trackSegment.gauge` | `"Standard"` | string; enum: Standard, Narrow, 3ft, 3 ft, ThreeFoot, Three Foot, DualGauge, DualGauge_L, DualGauge_R, DualGauge_T, Dual, Mixed, MixedGauge |
| `trackSegment.bridgeSupportsSteel` | `false` | boolean |
| `trackSegment.yard` | `false` | boolean |
| `trackSegment.partial` | `false` | boolean |
| `trackSegment.preserveStyle` | `false` | boolean |
| `trackSegment.preserveBridgeSupportsSteel` | `false` | boolean |
| `trackSegment.preserveYard` | `false` | boolean |
| `trackSegment.preserveTrackClass` | `false` | boolean |
| `trackSegment.preserveSpeedLimit` | `false` | boolean |
| `trackSegment.preservePriority` | `false` | boolean |
| `trackSegment.preserveGroupId` | `false` | boolean |
## trackLocation

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `trackLocation.segmentId` | `"cvw-example"` | idRef; string |
| `trackLocation.normalized` | `1` | number; minimum=0; maximum=1 |
| `trackLocation.distance` | `1` | number; minimum=0 |
| `trackLocation.end` | `"A"` | string; enum: A, B, Start, End |
| `trackLocation.offset` | `0` | number |
## trackSpan

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `trackSpan.upper` | `{"segmentId":"cvw-example","normalized":1}` | trackLocation; object |
| `trackSpan.lower` | `{"segmentId":"cvw-example","normalized":1}` | trackLocation; object |
| `trackSpan.normalize` | `true` | boolean |
| `trackSpan.groupId` | `"cvw-example"` | idRef; string |
## trackArea

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `trackArea.name` | `"Cedar Valley Works"` | string |
| `trackArea.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `trackArea.radius` | `1` | number; minimum=0 |
| `trackArea.tagColor` | `[1,1,1]` | array; minItems=3; maxItems=4 |
| `trackArea.order` | `1` | integer |
| `trackArea.spanIds` | `[]` | idArray; array |
| `trackArea.groupId` | `"cvw-example"` | idRef; string |
## operations

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `operations.loads` | `{}` |  |
| `operations.industries` | `{}` |  |
| `operations.loaders` | `{}` |  |
| `operations.turntables` | `{}` |  |
| `operations.stations` | `{}` |  |
| `operations.removals` | `{}` | operationRemovals; object |
## operationRemovals

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `operationRemovals.industries` | `[]` | idArray; array |
## load

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `load.name` | `"Cedar Valley Works"` | string |
| `load.units` | `"Pounds"` | string; enum: Pounds, Gallons, Quantity |
| `load.density` | `62.4` | number; minimum=0 |
| `load.unitWeightInPounds` | `0` | number; minimum=0 |
| `load.importable` | `true` | boolean |
| `load.payPerQuantity` | `0` | number |
| `load.costPerUnit` | `0` | number |
| `load.carTypeFilter` | `"XM*"` | string |
| `load.emptyCarType` | `"XM*"` | string |
| `load.loadedCarType` | `"XM*"` | string |
| `load.icon` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `load.fields` | `{}` | object |
## industry

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `industry.name` | `"Cedar Valley Works"` | string |
| `industry.areaId` | `"cvw-example"` | idRef; string |
| `industry.order` | `1` | integer |
| `industry.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `industry.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `industry.usesContract` | `false` | boolean |
| `industry.mergeComponents` | `false` | boolean |
| `industry.replaceComponents` | `false` | boolean |
| `industry.components` | `{}` |  |
## industryComponent

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `industryComponent.remove` | `false` | boolean |
| `industryComponent.partial` | `false` | boolean |
| `industryComponent.type` | `"loader"` | string |
| `industryComponent.name` | `"Cedar Valley Works"` | string |
| `industryComponent.trackSpanIds` | `[]` | idArray; array |
| `industryComponent.trackSpanPatch` | `{}` | stringListPatch; object |
| `industryComponent.carTypeFilter` | `"XM*"` | string |
| `industryComponent.loadId` | `"cvw-example"` | idRef; string |
| `industryComponent.convertedLoadId` | `"cvw-example"` | idRef; string |
| `industryComponent.sharedStorage` | `true` | boolean |
| `industryComponent.storageChangeRate` | `1` | number |
| `industryComponent.maxStorage` | `1` | number; minimum=0 |
| `industryComponent.carTransferRate` | `1` | number; minimum=0 |
| `industryComponent.costPerUnit` | `1` | number |
| `industryComponent.notBeforeHour` | `1` | number; minimum=0; maximum=24 |
| `industryComponent.notAfterHour` | `1` | number; minimum=0; maximum=24 |
| `industryComponent.fillPercentage` | `1` | number; minimum=0; maximum=1 |
| `industryComponent.bookReasons` | `[]` | array |
| `industryComponent.title` | `"cvw-example"` | string |
| `industryComponent.orderAroundEmpties` | `true` | boolean |
| `industryComponent.orderAroundLoaded` | `true` | boolean |
| `industryComponent.inputSpanIds` | `[]` | idArray; array |
| `industryComponent.outputSpanIds` | `[]` | idArray; array |
| `industryComponent.inputTermsPerDay` | `{}` | loadRateMap; object |
| `industryComponent.outputTermsPerDay` | `{}` | loadRateMap; object |
| `industryComponent.idealCars` | `1` | number; minimum=0 |
| `industryComponent.teamProfiles` | `{}` | object |
| `industryComponent.canOverhaul` | `true` | boolean |
| `industryComponent.passengerStopId` | `"cvw-example"` | idRef; string |
| `industryComponent.timetableCode` | `"cvw-example"` | string |
| `industryComponent.basePopulation` | `1` | integer; minimum=0 |
| `industryComponent.neighborIds` | `[]` | idArray; array |
| `industryComponent.branch` | `"cvw-example"` | string |
| `industryComponent.branchDefinitions` | `[]` | array |
| `industryComponent.carLoadPeriod` | `1` | number; minimum=0 |
| `industryComponent.carLengthFeet` | `1` | number; minimum=0 |
| `industryComponent.fields` | `{}` | object |
## teamTrackEntry

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `teamTrackEntry.isExport` | `false` | boolean |
| `teamTrackEntry.loadId` | `"cvw-example"` | idRef; string |
| `teamTrackEntry.loadingTimeDays` | `1` | number; minimum=0 |
| `teamTrackEntry.carTypeFilter` | `"XM*"` | string |
## passengerBranch

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `passengerBranch.branch` | `"cvw-example"` | string |
| `passengerBranch.traverseTimeToNext` | `0` | integer; minimum=0 |
| `passengerBranch.mapFeature` | `"cvw-example"` | idRef; string |
| `passengerBranch.intermediates` | `{}` | object |
## passengerIntermediate

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `passengerIntermediate.code` | `"cvw-example"` | string |
| `passengerIntermediate.traverseTimeToNext` | `0` | integer; minimum=0 |
## loader

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `loader.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `loader.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `loader.prefab` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `loader.industryId` | `"cvw-example"` | idRef; string |
## turntable

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `turntable.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `turntable.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `turntable.radius` | `1` | number; exclusiveMinimum=0 |
| `turntable.subdivisions` | `16` | integer; minimum=4; maximum=32 |
| `turntable.legacyIdentifier` | `"cvw-example"` | string |
| `turntable.roundhouse` | `{"stalls":1}` | roundhouse; object |
| `turntable.visuals` | `{}` | turntableVisuals; object |
## turntableVisuals

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `turntableVisuals.pitAssetIdentifier` | `"cvw-example"` | string |
| `turntableVisuals.pitPosition` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `turntableVisuals.pitRotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `turntableVisuals.pitScale` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `turntableVisuals.bridgeAssetIdentifier` | `"cvw-example"` | string |
| `turntableVisuals.bridgePosition` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `turntableVisuals.bridgeRotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `turntableVisuals.bridgeScale` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `turntableVisuals.bridgeTrackEnabled` | `true` | boolean |
| `turntableVisuals.bridgeTrackGauge` | `1.435` | number; exclusiveMinimum=0 |
| `turntableVisuals.bridgeTrackLength` | `0` | number; minimum=0 |
| `turntableVisuals.bridgeTrackYOffset` | `0.08` | number |
| `turntableVisuals.controllerType` | `"ExampleProvider.Controller, ExampleProvider"` | string |
| `turntableVisuals.interactionRadius` | `16` | number; exclusiveMinimum=0 |
## roundhouse

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `roundhouse.stalls` | `1` | integer; minimum=1 |
| `roundhouse.startAngle` | `0` | number |
| `roundhouse.stallAngle` | `1` | number |
| `roundhouse.trackLength` | `46` | number; exclusiveMinimum=0 |
| `roundhouse.startPrefab` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `roundhouse.endPrefab` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `roundhouse.stallPrefab` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
## station

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `station.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `station.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `station.prefab` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `station.passengerStopId` | `"cvw-example"` | idRef; string |
## world

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `world.scenery` | `{}` |  |
| `world.spawnPoints` | `[]` | array |
| `world.splineys` | `{}` |  |
| `world.waterSurfaces` | `{}` |  |
| `world.telegraphPoles` | `{}` |  |
| `world.telegraphPoleMovements` | `[]` | array |
| `world.mapLabels` | `{}` |  |
| `world.mapMasks` | `{}` |  |
| `world.mapTiles` | `{}` |  |
| `world.sceneClones` | `{}` |  |
| `world.suppressBaseScenePaths` | `[]` | suppressionStringArray; array |
| `world.suppressBaseTrackGroups` | `[]` | suppressionStringArray; array |
| `world.suppressBaseAreas` | `[]` | suppressionStringArray; array |
| `world.suppressScenePaths` | `[]` | suppressionStringArray; array |
| `world.suppressGroups` | `[]` | suppressionStringArray; array |
| `world.suppressAreas` | `[]` | suppressionStringArray; array |
| `world.removals` | `{}` | worldRemovals; object |
## worldRemovals

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `worldRemovals.scenery` | `[]` | worldRemovalArray; array |
| `worldRemovals.splineys` | `[]` | worldRemovalArray; array |
| `worldRemovals.waterSurfaces` | `[]` | worldRemovalArray; array |
| `worldRemovals.telegraphPoles` | `[]` | worldRemovalArray; array |
| `worldRemovals.mapLabels` | `[]` | worldRemovalArray; array |
| `worldRemovals.mapMasks` | `[]` | worldRemovalArray; array |
| `worldRemovals.sceneClones` | `[]` | worldRemovalArray; array |
## scenery

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `scenery.model` | `"cvw-example"` | string; deprecated=True |
| `scenery.assetIdentifier` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `scenery.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `scenery.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `scenery.scale` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `scenery.anchorSpanIds` | `[]` | idArray; array |
## spawnPoint

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `spawnPoint.name` | `"Cedar Valley Works"` | string |
| `spawnPoint.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `spawnPoint.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `spawnPoint.radius` | `3` | number; exclusiveMinimum=0 |
| `spawnPoint.priority` | `0` | integer |
## spliney

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `spliney.type` | `"river"` | string; enum: river, road, terrainRoad, trestle, waterfall, objectLine, object-line, fence, retainingWall |
| `spliney.profile` | `"cvw-example"` | string |
| `spliney.style` | `"cvw-example"` | string |
| `spliney.offsetY` | `0` | number |
| `spliney.headStyle` | `"cvw-example"` | string |
| `spliney.tailStyle` | `"cvw-example"` | string |
| `spliney.assetIdentifier` | `"cvw-example"` | string |
| `spliney.prefab` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `spliney.spacing` | `5` | number; exclusiveMinimum=0 |
| `spliney.instanceScale` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `spliney.rotationOffset` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `spliney.lateralOffset` | `0` | number |
| `spliney.verticalOffset` | `0` | number |
| `spliney.snapToTerrain` | `false` | boolean |
| `spliney.alignToSlope` | `false` | boolean |
| `spliney.placeAtEnd` | `true` | boolean |
| `spliney.maximumInstances` | `1024` | integer; minimum=1; maximum=4096 |
| `spliney.points` | `[{"position":{"x":1,"y":1,"z":1}},{"position":{"x":1,"y":1,"z":1}}]` | array; minItems=2 |
## splineyPoint

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `splineyPoint.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `splineyPoint.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `splineyPoint.width` | `1` | number; exclusiveMinimum=0 |
## waterSurface

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `waterSurface.points` | `[{"x":1,"y":1,"z":1},{"x":1,"y":1,"z":1},{"x":1,"y":1,"z":1}]` | array; minItems=3 |
| `waterSurface.sourceLakePath` | `"World/REPLACE-WITH-VERIFIED-PATH"` | string |
| `waterSurface.materialName` | `"cvw-example"` | string |
| `waterSurface.lockHeight` | `true` | boolean |
| `waterSurface.snapToTerrain` | `false` | boolean |
| `waterSurface.enableCollider` | `true` | boolean |
| `waterSurface.uvScale` | `1` | number; exclusiveMinimum=0 |
| `waterSurface.triangleDensity` | `0.2` | number; maximum=1; exclusiveMinimum=0 |
| `waterSurface.maximumTriangleArea` | `50` | number; exclusiveMinimum=0 |
| `waterSurface.yOffset` | `0` | number |
## telegraphPoles

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `telegraphPoles.profile` | `"cvw-example"` | string |
| `telegraphPoles.polePrefab` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `telegraphPoles.wirePrefab` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `telegraphPoles.spacing` | `1` | number; exclusiveMinimum=0 |
| `telegraphPoles.points` | `[{"x":1,"y":1,"z":1},{"x":1,"y":1,"z":1}]` | array; minItems=2 |
## telegraphPoleMovement

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `telegraphPoleMovement.poleIndices` | `[1]` | array; minItems=1 |
| `telegraphPoleMovement.offset` | `{"x":1,"y":1,"z":1}` | vec3; object |
## mapLabel

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `mapLabel.text` | `"cvw-example"` | string |
| `mapLabel.style` | `"label"` | string; enum: label, speedLimit, speed-limit |
| `mapLabel.speedLimitMph` | `1` | integer; minimum=1; maximum=80 |
| `mapLabel.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `mapLabel.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `mapLabel.size` | `1` | number; exclusiveMinimum=0 |
| `mapLabel.color` | `"#FFFFFFFF"` | string; pattern=^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$ |
## circleMask

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `circleMask.type` | `"circle"` |  |
| `circleMask.center` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `circleMask.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `circleMask.radius` | `1` | number; exclusiveMinimum=0 |
| `circleMask.falloff` | `1` | number; minimum=0 |
| `circleMask.enableSetHeight` | `true` | boolean |
| `circleMask.enableCutTrees` | `true` | boolean |
| `circleMask.enableMaskModifier` | `true` | boolean |
| `circleMask.maskName` | `"cvw-example"` | string |
| `circleMask.order` | `1` | integer |
## rectangleMask

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `rectangleMask.type` | `"rectangle"` |  |
| `rectangleMask.center` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `rectangleMask.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `rectangleMask.size` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `rectangleMask.falloff` | `1` | number; minimum=0 |
| `rectangleMask.enableSetHeight` | `true` | boolean |
| `rectangleMask.enableCutTrees` | `true` | boolean |
| `rectangleMask.enableMaskModifier` | `true` | boolean |
| `rectangleMask.maskName` | `"cvw-example"` | string |
| `rectangleMask.order` | `1` | integer |
## curveMask

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `curveMask.type` | `"curve"` |  |
| `curveMask.center` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `curveMask.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `curveMask.width` | `1` | number; exclusiveMinimum=0 |
| `curveMask.points` | `[{"x":1,"y":1,"z":1},{"x":1,"y":1,"z":1}]` | array; minItems=2 |
| `curveMask.falloff` | `1` | number; minimum=0 |
| `curveMask.enableSetHeight` | `true` | boolean |
| `curveMask.enableCutTrees` | `true` | boolean |
| `curveMask.enableMaskModifier` | `true` | boolean |
| `curveMask.maskName` | `"cvw-example"` | string |
| `curveMask.order` | `1` | integer |
## mapTileSource

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `mapTileSource.directory` | `"Maps/CedarValley"` | string |
| `mapTileSource.sourceFolder` | `"Maps/CedarValley"` | string |
| `mapTileSource.priority` | `0` | integer |
## sceneClone

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `sceneClone.targetPath` | `"World/REPLACE-WITH-VERIFIED-PATH"` | string |
| `sceneClone.source` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `sceneClone.enabled` | `true` | boolean |
| `sceneClone.localPosition` | `{"x":1,"y":1,"z":1}` |  |
| `sceneClone.localRotation` | `{"x":1,"y":1,"z":1}` |  |
| `sceneClone.localScale` | `{"x":1,"y":1,"z":1}` |  |
## audio

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `audio.whistles` | `{}` |  |
| `audio.horns` | `{}` |  |
| `audio.bells` | `{}` |  |
## audioWhistle

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `audioWhistle.name` | `"Cedar Valley Works"` | string |
| `audioWhistle.clip` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `audioWhistle.model` | `{}` | audioAssetReference; object |
| `audioWhistle.rampUpPitch` | `1` | number |
| `audioWhistle.lerpSpeed` | `1` | number |
| `audioWhistle.airLerpSpeed` | `1` | number |
## audioHorn

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `audioHorn.name` | `"Cedar Valley Works"` | string |
| `audioHorn.layers` | `[{"file":"scenery://freight-house-general"}]` | array; minItems=1 |
## audioHornLayer

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `audioHornLayer.file` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `audioHornLayer.keyframes` | `[]` | array |
## audioBell

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `audioBell.name` | `"Cedar Valley Works"` | string |
| `audioBell.file` | `"scenery://freight-house-general"` | uri; string; pattern=^(vanilla\|path\|scenery\|asset\|rail\|file\|empty\|fuse)://.*$ |
| `audioBell.indexTimes` | `[]` | array |
## audioAssetReference

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `audioAssetReference.assetPackIdentifier` | `"cvw-example"` | string |
| `audioAssetReference.assetIdentifier` | `"cvw-example"` | string |
## audioKeyframe

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `audioKeyframe.t` | `1` | number |
| `audioKeyframe.value` | `1` | number |
## progression

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `progression.progressionId` | `"cvw-example"` | idRef; string |
| `progression.sections` | `[]` | array |
| `progression.progressions` | `{}` |  |
| `progression.mapFeatures` | `{}` |  |
## progressionDefinition

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `progressionDefinition.baseProgression` | `"cvw-example"` | idRef; string |
| `progressionDefinition.sections` | `{}` |  |
| `progressionDefinition.enableFeaturesAtStart` | `[]` | idPatch |
## section

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `section.id` | `"cvw-example"` | idRef; string |
| `section.progressionId` | `"cvw-example"` | idRef; string |
| `section.displayName` | `"Cedar Valley Works"` | string |
| `section.description` | `"Fictional syntax example."` | string |
| `section.prerequisiteSections` | `[]` | idArray; array |
| `section.prerequisiteSectionIds` | `[]` | idArray; array |
| `section.enableFeaturesOnUnlock` | `[]` | idArray; array |
| `section.disableFeaturesOnUnlock` | `[]` | idArray; array |
| `section.enableFeaturesOnAvailable` | `[]` | idArray; array |
| `section.unlockIncludeIndustries` | `[]` | idArray; array |
| `section.unlockExcludeIndustries` | `[]` | idArray; array |
| `section.unlockIncludeIndustryComponents` | `[]` | idArray; array |
| `section.areasEnableOnUnlock` | `[]` | idArray; array |
| `section.gameObjectsEnableOnUnlock` | `[]` | stringArray; array |
| `section.trackGroupsEnableOnUnlock` | `[]` | idArray; array |
| `section.trackGroupsAvailableOnUnlock` | `[]` | idArray; array |
| `section.interchangeTransfers` | `{}` | object |
| `section.deliveryPhases` | `[]` | array |
## deliveryPhase

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `deliveryPhase.cost` | `0` | integer |
| `deliveryPhase.industryComponentId` | `"cvw-example"` | idRef; string |
| `deliveryPhase.deliveries` | `[]` | array |
## delivery

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `delivery.carTypeFilter` | `"XM*"` | string |
| `delivery.loadId` | `"cvw-example"` | idRef; string |
| `delivery.count` | `1` | integer; minimum=1 |
| `delivery.direction` | `"loadToIndustry"` | string; enum: loadToIndustry, loadFromIndustry, import, export |
| `delivery.destinationIndustryId` | `"cvw-example"` | idRef; string |
## mapFeature

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `mapFeature.displayName` | `"Cedar Valley Works"` | string |
| `mapFeature.description` | `"Fictional syntax example."` | string |
| `mapFeature.initiallyEnabled` | `false` | boolean |
| `mapFeature.groupIds` | `[]` | idArray; array |
| `mapFeature.prerequisiteFeatureIds` | `[]` | idArray; array |
| `mapFeature.trackGroupsEnableOnUnlock` | `[]` | idArray; array |
| `mapFeature.trackGroupsAvailableOnUnlock` | `[]` | idArray; array |
| `mapFeature.areasEnableOnUnlock` | `[]` | idArray; array |
| `mapFeature.gameObjectsEnableOnUnlock` | `[]` | stringArray; array |
| `mapFeature.unlockIncludeIndustries` | `[]` | idArray; array |
| `mapFeature.unlockExcludeIndustries` | `[]` | idArray; array |
| `mapFeature.unlockIncludeIndustryComponents` | `[]` | idArray; array |
## editor

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `editor.projectName` | `"Cedar Valley Works"` | string |
| `editor.lastEditedUtc` | `"2026-09-21T00:00:00Z"` | string |
| `editor.viewport` | `{}` | object |
| `editor.viewport.position` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `editor.viewport.rotation` | `{"x":1,"y":1,"z":1}` | vec3; object |
| `editor.selectedObject` | `{}` | object |
| `editor.selectedObject.id` | `"cvw-example"` | idRef; string |
| `editor.selectedObject.type` | `"loader"` | string |
## stringListPatch

| Field | Example value | Schema constraints |
| --- | --- | --- |
| `stringListPatch.add` | `[]` | idArray; array |
| `stringListPatch.append` | `[]` | idArray; array |
| `stringListPatch.prepend` | `[]` | idArray; array |
| `stringListPatch.insert` | `[]` | idArray; array |
| `stringListPatch.replace` | `[]` | idArray; array |
| `stringListPatch.remove` | `[]` | idArray; array |
