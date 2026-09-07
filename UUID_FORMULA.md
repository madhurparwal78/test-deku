# How the bundle UUID is derived

The directory name in this export is a **UUIDv5** — a name-based UUID from
RFC 4122. It is a pure function of a namespace and a string, not a random value.

```python
import uuid

TASK = "S_ecomm_comm_hardware-companion-storefront_20260901_123839"
bundle_uuid = uuid.uuid5(uuid.NAMESPACE_URL, f"deku/{TASK}")
# -> e0f889a5-7a3b-5a05-a837-43ac155857a6
```

Reproduce it from a shell:

```bash
python3 -c "import uuid; print(uuid.uuid5(uuid.NAMESPACE_URL,
  'deku/S_ecomm_comm_hardware-companion-storefront_20260901_123839'))"
```

---

## The algorithm

```
namespace   6ba7b811-9dad-11d1-80b4-00c04fd430c8      the standard URL namespace
name        deku/S_ecomm_comm_hardware-companion-storefront_20260901_123839
```

**1. Hash the namespace bytes concatenated with the UTF-8 name.**

```
SHA-1( namespace.bytes ++ name.encode("utf-8") )
  = e0f889a57a3b0a05a83743ac155857a69db2c5e4          160 bits
```

**2. Keep the first 16 bytes.** The remaining 4 are discarded.

**3. Stamp the version and variant bits.**

```python
b[6] = (b[6] & 0x0F) | 0x50     # version 5 in the high nibble of byte 6
b[8] = (b[8] & 0x3F) | 0x80     # RFC 4122 variant in the top bits of byte 8
```

**Result**

```
e0f889a5-7a3b-5a05-a837-43ac155857a6
                ^    ^
                |    variant  (a = 0b1010, RFC 4122)
                version 5
```

The stamp is visible if you compare against the raw digest. SHA-1 produced
`…7a3b 0a05 a837…` and the UUID reads `…7a3b-5a05-a837…`: that `0 → 5` is step 3
overwriting four bits of the hash.

Verified by hand against Python's implementation — both produce
`e0f889a5-7a3b-5a05-a837-43ac155857a6`.

---

## Why v5 rather than v4

| | |
|---|---|
| **v4** | Random. A fresh id on every call, so re-running the export would create a new directory and orphan the previous one. |
| **v5** | Deterministic. The same task name always yields the same uuid, on any machine, forever. The export is idempotent: run it ten times, you get one directory. |

---

## The name string is a convention, not a standard

`deku/<task_name>` was chosen for this export. Any other prefix produces a
completely different uuid — `<task_name>` alone, or `deku/tasks/<task_name>`,
would each give something else.

Two consequences worth knowing:

1. **If these ids must match ids generated elsewhere**, that pipeline has to use
   the identical namespace *and* the identical name string. Neither is
   discoverable from the uuid itself.

2. **`task.toml` carries an empty `uuid_v5` field.** That suggests the task
   pipeline intends to hold a canonical id. If so, populating it there and
   reading it here is the better source of truth than recomputing from the
   directory name, which changes if a task is ever renamed.

---

## Per-run ids

This bundle keeps all eight runs under one uuid, so only the task is hashed.
An earlier layout gave each run its own bundle, using:

```python
uuid.uuid5(uuid.NAMESPACE_URL, f"deku/{TASK}/run_{n}")
```

Recorded here in case that layout is wanted again — the ids it produces are
stable and reproducible in the same way.
