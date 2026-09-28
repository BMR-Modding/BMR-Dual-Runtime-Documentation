# Code mods and optional runtime adapters

[Guide index](../README.md) · [Dependencies](./Dependencies-and-Discovery.md) · [Evidence](./Evidence-and-Compatibility.md)

A DLL does not rule out dual-runtime support. What matters is who initializes it, which assemblies its types come from, which services it calls, and when it expects world objects to exist.

## Choose an architecture

| Audit result | Appropriate starting point |
| --- | --- |
| UMM entry point; game, Unity, Harmony and UMM references; no loader requirement | Retain the DLL after checking lifecycle and interactions in both runtimes. |
| Shared behavior plus a small optional runtime integration | Keep a neutral core and use a narrowly validated adapter. |
| Loader-owned base class, constructor, settings API, or service | Port initialization/settings from source or implement a verified adapter. |
| Required behavior has no equivalent in the other runtime | Implement it explicitly or document the unsupported feature. |
| Unknown binary without sufficient evidence | Report the unresolved bindings; do not call it converted. |

Removing a manifest requirement does not remove a binary dependency. Conversely, generic optional ordering entries do not create a compiled assembly dependency.

## Pattern A: one shared UMM DLL

Whittier Central provides the packaging example. UMM owns `BMRWhittierCentral.dll` and `BMRWhittierCentral.Main.Load`. The DLL uses game hooks without a compiled FUSE dependency. RF's manifest does not initialize it again.

A complete illustrative `Info.json` for this pattern:

```json
{
  "Id": "ExampleAuthor.SharedMod",
  "DisplayName": "Example Shared Mod",
  "Author": "Example Author",
  "Version": "1.0.0",
  "ManagerVersion": "0.27.10",
  "AssemblyName": "ExampleSharedMod.dll",
  "EntryMethod": "ExampleSharedMod.Main.Load",
  "Requirements": [],
  "LoadAfter": ["FUSE", "RTM.RailForge"],
  "FuseRequires": [],
  "FuseLoadAfter": [],
  "FuseDataFiles": ["content.fuse.json"]
}
```

Pair it with:

```json
{
  "manifestVersion": 5,
  "id": "ExampleAuthor.SharedMod",
  "name": "Example Shared Mod",
  "author": "Example Author",
  "version": "1.0.0",
  "requires": [],
  "loadAfter": []
}
```

These are manifest examples, not a supplied DLL or complete mod. Build the named UMM entry point and add translated data before using them. Add actual content providers through the appropriate dependency fields.

Do not add an RF `assemblies` declaration for this same initializer. Establish one owner for initialization, patch registration, event subscriptions, and cleanup. UMM loading the code once does not mean all graph objects are already ready; use observed lifecycle hooks and bounded readiness checks.

## Pattern B: optional runtime integration

Sequential Industry implements optional support for RF captive conversion components without a required RailForge assembly reference. Its approach is useful beyond that mod:

1. Start through UMM and initialize the neutral behavior.
2. Inspect already loaded assemblies for the optional provider.
3. Handle a provider arriving later. Its assembly-load callback only marks work pending; patch work is deferred to the UMM update path.
4. Verify the exact declaring assembly, type, base type, field types, and method signature.
5. Install only the supported integration, once.
6. If installation fails, remove that integration's partial work and report it. Keep supported core behavior available.
7. Remove owned subscriptions/patches on supported shutdown paths.

A loaded assembly establishes type availability; it does not by itself prove that the provider is enabled in the active profile or that its world objects are ready. Verify activity/readiness separately when your integration needs them.

This is a design pattern, not permission to apply the same patch to every component. RF captive conversion components have their own `Service` implementations; patching vanilla `IndustryLoader.Service` alone did not cover them. Sequential Industry explicitly supports the two captive types and leaves `Pay4Resource` unchanged.

Avoid static references to optional runtime types in a supposedly neutral core. A check such as "is RailForge installed?" may come too late if type loading or JIT compilation already needs `RailForge.dll`.

## DELTA45 fuel-hook ownership

DELTA45 adds oil-steam hooks that check for competing fuel owners and can hold support when a foreign contract is unrecognized. Its reviewed LSE tender-guard exception is fingerprint-specific. A shared fuel DLL therefore needs a new compatibility test even though its graph still parses. See the [DELTA45 fuel scope](RailForge-DELTA45-Update.md#oil-fired-steam-and-toolshed).

The internal policy methods used by the documentation probes are inspection targets, not a promised public API for production mods.

## Audit the assembly scope

The Storms Intermodal Yard 1.0.8 audit found these familiar names:

```text
Railloader.SingletonPluginBase<T>
Railloader.IModdingContext
Railloader.IModDefinition
```

Their assembly scope was `RailForge, Version=0.14.7.0`. The inspected FUSE resolver recognized `Railloader*` and `StrangeCustoms`, but not `RailForge`. Similar API names therefore did not satisfy the binary reference.

Inspect metadata/IL without executing an unknown mod initializer. Record:

- referenced assembly names and versions;
- base classes, constructor arguments, and singleton access;
- enable/disable methods and settings storage;
- Harmony targets, signatures, and patch ordering;
- loader-specific services and asset URI assumptions;
- save keys, authority/host behavior, and teardown writes.

Storm's code conversion is still **unproven**. Much operational logic used game APIs, but that is an argument for a focused port, not a passed compatibility test. Prefer the author's source for a maintainable port and preserve settings/behavior deliberately.

## Lifecycle acceptance

Check initialization count, patch count, world readiness, save/reload, menu return, new world creation, and supported disabling behavior. A startup message proves startup only.

Whittier's billing exposed a concrete trap: car-removal callbacks also ran during map teardown. Its shared code needed a game `StateManager.IsUnloading` guard so leaving the map did not settle a purchase. See [Progression and save lifecycle](./Progression-and-Save-Lifecycle.md).

Use [the evidence record](./Evidence-and-Compatibility.md) for the implementations and the limits of their recorded tests.
