---
name: sync-from-the-source-of-truth
description: "Apply when building or changing sync, publish, import, or deployment tooling that copies authored state into remote systems, caches, or generated output. Declare which source owns each synchronized value and reconcile in that direction."
---

# Sync from the source of truth

Synchronization needs a clear answer to which value should win. Establish the source of truth for the state being synchronized, then make its derived representations agree.

- Identify the resources and fields the source owns before comparing or changing them.
- Derive the intended destination state from that source. Do not treat destination drift as an implicit change to the source.
- Keep caches and identity mappings in their supporting roles; they do not become competing authoring systems.
- Separate mismatches in owned values from independently managed destination content.
- Resolve discrepancies within the authorized scope and verify that the resulting state matches the intended values.

The source of truth is specific to the synchronized state, not necessarily to an entire system. Preserve independently owned fields and apply explicit deletion rules. Genuinely bidirectional editing requires a conflict policy; declaring one source authoritative does not grant permission to overwrite unrelated work.
