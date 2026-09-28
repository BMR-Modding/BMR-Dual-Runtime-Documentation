# Progression and save lifecycle

[Guide index](../README.md) · [Technical guide](./FUSE-RailForge-Dual-Runtime-How-To.md) · [Evidence](./Evidence-and-Compatibility.md)

Progression conversion must preserve who controls an object, when it becomes available, and how that decision is replayed after loading a save. A visible graph record alone does not prove correct gameplay.

## Distinguish the stages

| Stage | What to verify |
| --- | --- |
| Graph merge | IDs, features, phase references, groups, and delivery data exist. |
| Runtime materialization | Real industries, components, tracks, and scene objects are created. |
| Initial visibility | Locked content starts locked in the intended game mode. |
| Unlock | Real payment/deliveries enable the intended objects and disable replaced behavior. |
| Saved-state replay | Reload and delayed scene creation restore the same state without undoing it. |

In inspected RF builds, definition hydration can succeed while progression visibility enforcement is disabled. Record the progression materializer and initial-visibility settings required by your content; do not silently change global settings for players.

FUSE `initiallyEnabled` and RF `defaultEnableInSandbox` describe Sandbox behavior. They are not a substitute for Company progression or a Company-start feature grant. Test both modes.

## Give each object a clear controller

Maintain an ownership table for the features you author:

| Object | Intended controller | Expected lifetime |
| --- | --- | --- |
| Expansion tracks | Trackwork feature/group | Locked before trackwork; available afterward. |
| Temporary construction component | Its native delivery phase | Available only during that phase. |
| Replacement production formula | Production milestone | Active after the milestone; old formula disabled. |
| Customer loader | Its purchase/unlock milestone | Locked until that milestone completes. |
| Service industry and facilities | Explicit service-expansion gate where needed | Locked until expansion; restored correctly after reload. |

Multiple independent features writing the same availability state can disagree. Retain stable IDs used by saves while removing obsolete control claims where appropriate.

## Case: FUSE inferred a service gate; RF needed it explicitly

For Tuckasegee River Distillery, inspected FUSE inferred the engine-service industry as expansion-controlled from its track spans. The inspected RF paths did not provide that inference.

The RF branch therefore explicitly included `TRD_Engine_service` in the expansion feature's industry gate. It preserved the 13 expansion segments and their group, service loader identities, and existing production references.

Do not generalize this into "include every industry in every feature." Identify the logical gate, translate its exact industry/component references, and test coal, water, diesel, repair, and production behavior while locked and unlocked. The temporary construction component must remain phase-controlled.

## Case: a completed construction site returned after reload

Whittier Central's permanent Trackwork feature still claimed a temporary Production Upgrade delivery component. RF DELTA25 could replay the saved permanent feature after deferred hydration, re-enabling the completed construction site.

The fix removed the claim from both branches and retained an explicit empty list:

```json
{
  "unlockIncludeIndustryComponents": []
}
```

This is the relevant field inside the existing feature, not a complete graph. Preserve that feature's other intended fields.

Omitting the field could retain the old claim on an existing hydrated feature. Keeping `[]` allowed the inspected hydration path to clear it. This is a specific update to an existing feature; do not indiscriminately empty unrelated include arrays.

Test unpaid, active-delivery, just-completed, and saved-completed states. Repeat after delayed scenery load and a full restart. Console advancement can diagnose visibility but cannot prove actual deliveries or ordering.

## Case: removal callbacks during map teardown

Whittier's Repair Parts billing originally treated car removal as a possible departure. The game's map-unload path also removes cars. That could settle a purchase when returning to the menu.

The shared DLL used the verified vanilla `StateManager.IsUnloading` state to suppress purchase writes/settlements during teardown while preserving unpaid saved purchases. Actual departures and full loading remained billable.

For any stateful code, distinguish gameplay removal, map unload, save restoration, and genuine job completion. Test:

1. Partial loading, save, return to menu: no teardown charge.
2. Reload that exact save: unpaid state retained.
3. Depart partially loaded or finish loading: one settlement.
4. Save/reload after payment: no repeat charge.
5. Start another world: no stale per-world state.

These are lifecycle requirements for the billing example, not a generic recipe to suppress all removal callbacks.

## Stable IDs and migration

Keep IDs for unchanged objects and audit all references when an ID changes. A cargo rename can leave existing inventory, cars, orders, or waybills on the old ID. A display-name match does not migrate them.

Distinguish:

- upgrading your mod within one runtime;
- loading a save made with a previous mod version;
- switching a save from FUSE to RF, or back.

Passing one does not establish the others. Record the exact source save, versions, migration mechanism, and observed result before advertising portability. Until then, use separate test saves and describe cross-runtime migration as untested.

Continue with the [test report](../templates/TEST-REPORT.md).
