# Dual runtime examples

Start with the small cargo example below, or explore [Cedar Valley Works](CedarValleyWorks/README.md) for a complete fictional district, a conversion walkthrough, advanced syntax recipes and a field atlas.

## Paired cargo example

[Guide index](../README.md) · [Quickstart](<../Duality mode documentation/FUSE-RailForge-Dual-Runtime-Quickstart.md>)

`ExampleAuthor.DualCargo` demonstrates the smallest useful paired-data pattern: one custom load called **Example Crated Goods** with ID `exampleauthor.crated-goods`.

```text
ExampleAuthor.DualCargo/
├── Info.json
├── Definition.json
├── cargo.fuse.json
└── RailForge/
    └── game-graph/
        └── cargo.json
```

FUSE reads `operations.loads` from its declared file. RF reads `loads` from its native folder. FUSE's `name` becomes RF's `description`; the other six cargo fields retain the same values.

This package supplies a cargo definition only. It creates no track, industry, automatic order, or visual load. A compatible loader/delivery using the cargo is needed for a gameplay demonstration. The numbers are illustrative, not economic balancing advice.

## Adapt it

1. Copy only the `ExampleAuthor.DualCargo` folder to your development area.
2. Choose your own stable package and cargo IDs; update both manifests and graphs.
3. Keep manifest versions and `modVersion` synchronized.
4. Add content/providers using the appropriate guides.
5. Verify both branches and test in separate runtime environments.

The example has no DLL, asset pack, third-party content, hard runtime requirement, or conditional payload. Do not add loader DLLs simply to make it resemble a code mod.

## Validation status

This is a newly authored documentation example. Its JSON, field parity, file placement, and manifests are checked during documentation preparation. Runtime-method probe results, if obtained, are recorded in [VALIDATION.md](../VALIDATION.md).

No live Railroader gameplay, installation-method acceptance, or save-migration test is claimed for this example. Perform those checks for the actual mod you build from it.
