# Authoring and conversion workflows

[Guide index](../README.md) · [Quickstart](./FUSE-RailForge-Dual-Runtime-Quickstart.md) · [Field matrix](./FUSE-RailForge-Complete-Translation-Matrix.md)

Choose the workflow that matches the source you maintain. Each produces one package with separate runtime data and, when applicable, shared or adapted code.

## 1. Classify the whole mod

Keep the original outside the release directory and record its version and hashes. Inventory manifests, fragments, conditions, graph operators, assets, DLLs, settings, progression, and saved identifiers. Use the [conversion record](../templates/CONVERSION-RECORD.md).

| What you find | Next step |
| --- | --- |
| Data using known mappings | Translate with the matrix and compare behavior. |
| Patches to existing game/provider objects | Resolve baseline and merge intent first. |
| External assets/data | Map exact provider IDs and content identities per runtime. |
| A UMM DLL using game/Harmony APIs | Audit references and lifecycle; it may be reusable unchanged. |
| A DLL using loader APIs or loader-owned base classes | Audit assembly identity; plan an adapter or source rebuild. |
| An unknown handler, extension, or custom component | Identify its provider or replacement behavior before claiming support. |

Preserving an unknown object in conversion metadata does not make its feature work. Keep every intended feature in the inventory until it has both an implementation and a test result.

## 2. New mod or FUSE-first

1. Build native FUSE content and test the intended gameplay.
2. Freeze it as the source of intent.
3. Add `Definition.json` and translate into `RailForge/game-graph`.
4. Work in reference order: tracks/spans, loads, areas/industries, scenery/handlers, progression.
5. Record deliberate differences. Preserve IDs for unchanged logical objects.
6. Validate each branch against its runtime, then playtest the exact package in separate environments.

Generate the second branch where practical. If editing it manually, review each source change against the other branch. Correct a shared design error in both branches; keep a runtime-specific workaround narrowly scoped.

## 3. RailForge-first

Keep the working RF package authoritative. It does not need to be round-tripped through FUSE before adding a FUSE branch.

### Recover the patch's intended result

RF data may describe only changes to the game and earlier providers. Inventory:

- records created versus records already present;
- required game/provider versions and patch order;
- omitted values, complete arrays, `$replace`, `$find`, `$add`, and supported null tombstones;
- behavior implemented outside the graph.

Evaluate the patch against the correct baseline for comparison. **Do not publish the entire merged vanilla graph as your FUSE payload.** Translate this mod's authored changes, with inherited values understood and unrelated content preserved.

For example, an RF patch changing only `carTransferRate` must preserve that component's load, storage, span, and ordering settings. Use the applicable FUSE partial/merge contract. Default zeros or an incomplete replacement object change its meaning.

### Translate intent, not operator spelling

| RF intent | FUSE work |
| --- | --- |
| Omitted property | Preserve inherited value through the applicable partial contract. |
| Complete ordinary array | Preserve replacement intent; verify the target namespace's rules. |
| `components.$replace` | Supply the complete component set with the appropriate replacement flag. |
| `$find` or array program | Resolve the target and use an equivalent supported patch, or derive the final scoped value. |
| Supported null tombstone | Use the corresponding removal mechanism. |
| Provider/handler behavior | Use a verified counterpart or implement missing behavior. |

An important asymmetry: ordinary RF arrays replace, but `trackSpanIds` on a FUSE component with `partial: true` can append distinct IDs. A literal array copy can therefore bind different tracks.

Add `Info.json` with explicit `FuseDataFiles`. Keep RF data in its native folder, test FUSE independently, then run an RF regression with the same package. Future RF source changes must update the FUSE branch.

## 4. Legacy-first

Treat RailLoader/Strange Customs-family material as source or an intentional compatibility path.

1. Inventory every legacy root, mixinto, condition, handler, assembly, and provider.
2. Classify each payload as **native conversion**, **deliberate legacy reader**, **provider/code required**, or **unresolved**.
3. Convert recognized FUSE data and inspect the conversion report. Preserved-only content needs further work.
4. Translate RF data natively, or retain a verified RF legacy path for that payload.
5. Remove equivalent active legacy copies from the release. Keep original source in development storage.
6. Audit DLLs separately, even if the graph and type names look portable.

A reader recognizing a filename does not establish that its providers, assets, and code will run.

## 5. Conditional content

Use equivalent conditions and runtime-correct provider IDs on the two fragments.

```text
Your.Mod/
├── base.fuse.json
├── optional-yard.fuse.json
└── RailForge/
    ├── game-graph/base.json
    └── conditional/optional-yard.json
```

FUSE lists both FUSE files in `FuseDataFiles`; the optional file carries `mixinto.requires` / `conflictsWith`. RF references the conditional file from `Definition.json.mixintos`.

Keep conditional RF files outside `RailForge/game-graph`. Native scanning otherwise bypasses the condition and the mixinto may apply the data a second time. Package-level requirements are appropriate only when the whole package needs the provider. The [technical guide](./FUSE-RailForge-Dual-Runtime-How-To.md#conditional-mixintos-in-the-dual-package) contains the declarations.

## 6. Compare identity and behavior

Compare IDs, geometry, span endpoints, units, recipes, storage, rates, filters, order flags, milestones, and asset identities. Display names alone are insufficient.

Record every permitted difference with its reason, affected references, and regression case. Never globally clear `groupId` because one optional route's group hid some base tracks.

Cargo renaming is also a save decision. Changing `scrap-metal` to `bmr.scrap-metal` creates another ID; inventory, orders, and waybills do not automatically follow. Coordinate the branches and document the upgrade separately.

## 7. Automation boundaries

Manifests, file placement, known field mappings, reference comparisons, and packaging are good automation targets. Baseline-dependent patch intent, unknown handlers, DLL adaptation, and save migration need explicit rules and evidence.

A converter should report per-feature status: **translated**, **needs provider/adapter**, or **unresolved**, plus its separate validation level. It must not silently drop features it cannot translate.

Continue with [Testing and release](./Testing-and-Release.md).
