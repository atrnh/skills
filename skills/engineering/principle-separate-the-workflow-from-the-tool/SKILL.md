---
name: principle-separate-the-workflow-from-the-tool
description: "Apply when writing skills, scripts, or integrations meant to work across editors, note apps, storage systems, or other tools. Keep the workflow's decisions and intended results independent of tool-specific operations."
---

# Separate the workflow from the tool

A reusable workflow should retain its purpose and judgment when the tool changes. Identify what the work means before tying it to the operations of one application.

- Describe inputs, decisions, and intended results in terms of the work being done.
- Keep reading, writing, formatting, and annotation mechanics with the tool that performs them.
- Preserve the workflow's meaning when adapting it to another supported environment.
- Make tool limitations explicit where they affect the result, rather than silently changing the task.
- Add support for actual use cases. A clear separation in instructions or functions may be enough.

Portability does not require an adapter framework or implementations for hypothetical tools. A workflow intended for one application can remain specific to it. Separate the parts that need to travel without discarding capabilities the requested work depends on.
