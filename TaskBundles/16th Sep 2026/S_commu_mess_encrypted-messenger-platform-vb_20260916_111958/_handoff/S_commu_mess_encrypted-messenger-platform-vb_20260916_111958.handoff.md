# Handoff contract - deku/encrypted-messenger-platform-vb

```
BUNDLE          S_commu_mess_encrypted-messenger-platform-vb_20260916_111958/
TASK CODE       S_commu_mess_encrypted-messenger-platform-vb_20260916_111958
TASK ID         deku/encrypted-messenger-platform-vb
STATE           MECHANICALLY-GREEN, NO-SOLUTION
                NOT ADMISSIBLE. The bundle carries no reference app (D20).
GRADER VERSION  0.22.0
TARGET SCHEMA   1.4
VERIFIER MODE   separate
KIT GATE LOG    rendered from _handoff/S_commu_mess_encrypted-messenger-platform-vb_20260916_111958.gates.jsonl
BLOCKING PREREQUISITES  NONE (postgres and mailpit both have pinned images)
HANDOFF GATES   run these, in this order:
  STEP 0  build the reference app downstream from solution/checklist.md, then write solve.sh
  G13  docker buildx build --platform linux/amd64,linux/arm64 -f environment/Dockerfile .   expect exit 0
  G13  docker build -f tests/Dockerfile tests/                                               expect exit 0
  G15  docker compose -f environment/docker-compose.yaml up --wait                          expect all sidecars healthy
  G19  harbor run -p <task> -a oracle                                                       expect reward == 1.0 (twice)
  G18  read deployed from either oracle run                                                 expect deployed == 1.0
  G20  harbor run -p <task> -a nop                                                          expect reward == 0.0
  G21  apply fake-integration patch, re-run oracle                                          expect reward < 1.0
  G25  reviewer exploit sweep, reference library F                                          expect 0 of 11 succeed
ON FAILURE      route-back table (plan 15.3): failing gate -> owning kit stage
KNOWN UNPROVEN  no reference code exists yet; nothing in this bundle has been compiled or run
```

## Runtime notes for the operator

- The vendored `test.sh` runs the advisory rubric judge only when `/tests/instruction.md` exists; the output contract (CON-2) retired that copy, so the judge is skipped unless the harness supplies the brief. Reward never depends on it.
- Workflows `sealed_message_reaches_the_recipient_devices_only`, `tampered_or_replayed_message_is_never_trusted` and `person_calls_from_group_and_conversation_then_signs_out` need `nova`'s browser registered by `person_signs_in_and_registers_first_browser`, which runs first in file order.
- The browser runner launches Chromium without fake media; the brief requires the call screen to open regardless of media access.
