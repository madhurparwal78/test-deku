BUNDLE          S_ecomm_comm_modular-accessory-ecosystem-vb_20260916_091543/
TASK CODE       S_ecomm_comm_modular-accessory-ecosystem-vb_20260916_091543
TASK ID         deku/modular-accessory-ecosystem-vb
STATE           MECHANICALLY-GREEN, NO-SOLUTION
                NOT ADMISSIBLE. Build the app downstream from solution/checklist.md, then run the gates below.

GRADER VERSION  0.22.0
TARGET SCHEMA   1.4
VERIFIER MODE   separate
RUBRIC          tests/rubric.json, 13 judged criteria

KILL BILL NOTE  The storefront uses a least-privilege Kill Bill user created by environment/killbill-init.sh
                (role storefront: account:*, invoice:*). The admin pair is verifier only. Kill Bill boots for
                minutes on a cold volume; allow for it before G15.

G13  docker build -f environment/Dockerfile environment/ ; docker build -f tests/Dockerfile tests/   -> exit 0
G15  docker compose -f environment/docker-compose.yaml up --wait   -> postgres, killbill, killbill-db, mailpit healthy; killbill-init parked
G18  harbor run -p S_ecomm_comm_modular-accessory-ecosystem-vb_20260916_091543 -a oracle, read deployed   -> 1.0
G19  harbor run -p S_ecomm_comm_modular-accessory-ecosystem-vb_20260916_091543 -a oracle  (x2)   -> 1.0, 1.0
G20  harbor run -p S_ecomm_comm_modular-accessory-ecosystem-vb_20260916_091543 -a nop   -> 0.0
G21  mutate the app to mark orders paid without a Kill Bill invoice, run the oracle   -> < 1.0
G25  exploit sweep per reference/F   -> 0/11
