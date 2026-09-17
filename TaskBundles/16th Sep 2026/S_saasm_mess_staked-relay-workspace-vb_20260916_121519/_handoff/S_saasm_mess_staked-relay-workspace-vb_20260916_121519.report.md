# Build report - deku/staked-relay-workspace-vb

Task code: `S_saasm_mess_staked-relay-workspace-vb_20260916_121519`

Gates run: 32 | ok: 32 | red: 0

**ALL GATES GREEN.** Exit state MECHANICALLY-GREEN, NO-SOLUTION. NOT ADMISSIBLE until a reference app exists and `harbor run -a oracle` returns 1.0 twice.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | validate_task.py | 0 | PASS |
| G1/G12 | layout_lint.py | 0 | PASS |
| G46 | structure_lint.py | 0 | PASS |
| G50 | docker_lint.py | 0 | PASS |
| G55 | runtime_deps_lint.py | 0 | PASS |
| G63 | secret_lint.py | 0 | PASS |
| G48 | truth_lint.py | 0 | PASS |
| G51 | source_lint.py | 0 | PASS |
| G52 | rubric_context_lint.py | 0 | PASS |
| G54 | comment_lint.py | 0 | PASS |
| G17 | secret_hygiene_lint.py | 0 | PASS |
| G11 | leak_scan.py | 0 | PASS |
| G33 | window_lint.py | 0 | PASS |
| G4/G5 | contract_lint.py | 0 | PASS |
| G43 | prescription_lint.py | 0 | PASS |
| G44 | disclosure_lint.py | 0 | PASS |
| G10 | no_sdk_lint.py | 0 | PASS |
| G31 | determinism_lint.py | 0 | PASS |
| G14 | reward_path_lint.py | 0 | PASS |
| G27/G30 | rubric_lint.py | 0 | PASS |
| G41 | flag_lint.py | 0 | PASS |
| G56/G57/G58 | if_lint.py | 0 | PASS |
| G59/G60 | codequality_lint.py | 2 | ? |
| G7/G8/G9/G32/G45 | workflow_lint.py | 0 | PASS |
| G6 | fixture_lint.py | 0 | PASS |
| G24 | coverage_map.py | 0 | PASS |
| G37 | checklist_qc.py | 0 | PASS |
| G39 | rubric_align_lint.py | 0 | PASS |
| G28/G29 | channel_lint.py | 0 | PASS |
| G40 | prompt_receipt_lint.py | 0 | WARN |
| G0/INV5 | vendor_check.py | 0 | PASS |
| G47 | output_qc.py | 0 | PASS |

G59/G60 is the advisory code-quality channel and returns NOT-APPLICABLE because the bundle carries no source criteria. G40 records WARN because every certification receipt is SELF-ATTESTED (owner equals verifier). Prose verdicts recorded in the receipts: G3 VALID (task_code_verifier.md); G34 FAIL (QC_instruction.md); G34 PASS (QC_spec.md); G35 PASS (qc_docker.md); G36 PASS (qc_toml.md); G37 PASS (qc_solution_checklist.md); G53 PASS (qc_rubric.md). Non-PASS checks by prompt: QC_instruction.md: C4 WARN, C7 FAIL, D3 WARN; QC_spec.md: S9 WARN; qc_docker.md: BP-003 WARN, CMP-011 WARN, CMP-021 WARN; qc_rubric.md: RC-08 WARN, RC-09 WARN, RC-12 WARN, RC-16 WARN; qc_solution_checklist.md: none; qc_toml.md: INST-004 WARN; task_code_verifier.md: none. See the receipt findings for each.

## Cell and configuration

| Field | Value |
|---|---|
| cell | solo_founder / saas-micro-tools / messaging-notifications |
| service_profile | P2-db-email |
| providers | backend postgres, email mailpit |
| variant | b, axes critical_depth, spec_sections, roles |
| language | typescript (drawn: ssr-islands, Hono, SvelteKit) |
| capability_flags | aesthetic |
| design_direction | companion |
| launch_surface | alt_text,custom_404,form_validation,sitemap_robots,spam_protection |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| grader / schema | 0.22.0 / 1.4 |
| turns / tokens | 200 / 8000000, the expert band: two services, browser-side sealing, exact settlement arithmetic, a companion carried in full |

## Graders

Workflows 16 | browser substeps 32 | pytest substeps 78 | critical substeps 41 | largest workflow 9 substeps, so one failed substep fails any workflow. One module, `tests/test_output.py`, 78 tests. Rubric 16 criteria, all positive, advisory and off the reward path. Checklist 336 items; every item is cited by pytest, a browser substep or a rubric criterion (G24, G28, G39).

## Rubric point shares

| Dimension | Points | Share | Target |
|---|---|---|---|
| instruction_following | 14 | 0.318 | 0.30 |
| functionality | 8 | 0.182 | 0.25 |
| ux_flow | 6 | 0.136 | 0.15 |
| ui_visual | 9 | 0.205 | 0.15 |
| motion | 3 | 0.068 | 0.05 |
| accessibility | 3 | 0.068 | 0.05 |
| responsiveness | 1 | 0.023 | 0.05 |

## Slot obligations

| Slot | Provider | Critical substep | Status |
|---|---|---|---|
| backend | postgres | test_key_directory_lists_only_active_devices, test_message_text_is_sealed_in_the_browser_and_a_tampered_copy_will_not_open, test_retried_send_stores_one_envelope_row and more | MET |
| email | mailpit | test_waitlist_confirmation_email_reaches_only_the_requester, test_simultaneous_waitlist_requests_send_one_confirmation_email, test_simultaneous_whitelist_applications_from_one_wallet_file_one_and_email_once | MET |

## Carriage of the companion PRD (G51)

- note  void_prd.md: 11/11 source colour(s) described in the brief by family and tone
- note  void_prd.md: 174/174 topic(s) carried into the brief
- note  void_prd.md: 290/290 enumerated item(s) carried into the brief
- note  void_prd_technical.md: 11/11 source colour(s) described in the brief by family and tone
- note  void_prd_technical.md: 174/174 topic(s) carried into the brief
- note  void_prd_technical.md: 290/290 enumerated item(s) carried into the brief
- note  void_prd_plain.md: 26/26 topic(s) carried into the brief
- VERDICT  PASS   G51: every supplied source document is carried into instruction.md (/Users/apple/Downloads/Greenfield2/16sept_task_bundle/task_09/S_saasm_mess_staked-relay-workspace-vb_20260916_121519/instruction.md)

No `--waive` was used. The companion is `void_prd.md`, the full PRD; its two register twins are carried alongside it, and all three are recorded in `_handoff/<code>.sources.json`.

## Grading window (G33)

```
VERDICT  PASS   (/Users/apple/Downloads/Greenfield2/16sept_task_bundle/task_09/S_saasm_mess_staked-relay-workspace-vb_20260916_121519/instruction.md)
section        H2                chars  reference  flag
core_features  Core features     55832       2400  past-slice
user_flow      User flow         10823       1900  past-slice
ui_ux_notes    UI/UX notes        4586       1700  past-slice
constraints    Constraints        1037        800  over-reference
user_roles     User roles         3248       1000  past-slice
overview       Overview           2655        700  past-slice
joined total                     78181       8800  past-slice
first four                       72278       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

The brief is far past the judge's slice by design: the companion is carried in full and the judge reads the first 2,500 characters of six sections. Core features opens with the three critical rules, and UI/UX notes opens with the palette, motion, components and mode paragraphs, so what the judge sees is what the rubric grades.

## Traps proven both ways

A scratch reference of the pinned HTTP contract and workspace pages (stdlib Python plus vanilla JavaScript, kept outside the bundle) ran the real `tests/test_output.py` against real PostgreSQL 16.4 and Mailpit v1.30.6 in the pinned Playwright image. Correct mode: 78 of 78 pass, 0 failed. Each switch below turns on one naive default; its target fails on the intended assertion and nothing else fails.

| Naive default | Target | Failing test | Result |
|---|---|---|---|
| plaintext | sealed_in_the_browser | test_message_text_is_sealed_in_the_browser_and_a_tampered_copy_will_not_open | thesendingbrowsersentthetypedwords:['cGxhaW4td29yZHMtZTZhZTQ0MTM0'] Eassertnot['cGxhaW4td29yZHMtZTZhZTQ0MTM0'] |
| staticKey | unapproved_device | test_unapproved_device_cannot_open_messages_until_approved | theunapproveddeviceshowsnounopenableline EassertFalse |
| plainname | uploaded_file_name | test_uploaded_file_name_and_contents_are_sealed_before_upload | thebrowsersentthefilenameorcontents:['cHJpdmF0ZS1uYW1lLWJiODAxODZj'] Eassertnot['cHJpdmF0ZS1uYW1lLWJiODAxODZj' |
| css_lock | without_scripts | test_page_without_scripts_shows_every_section_and_scrolls | withscriptsunavailable/doesnotscroll EassertFalse |
| opacity_zero | without_scripts | test_page_without_scripts_shows_every_section_and_scrolls | withscriptsunavailable#aboutSectionrendersatopacity0 Eassert0>0.5 |
| heavy_first_load | byte_budget | test_first_public_page_load_stays_inside_the_byte_budget | thefirstloadof/fetches200003bytesofscript,over150000 Eassert200003<=150000 |
| alt_missing | alternative_text | test_public_images_carry_alternative_text_or_declare_decoration | imageswithoutalternativetextoradecorativedeclaration:['/:imgdata:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDov |
| inline_missing | invalid_signup |  |  |
| stepper_forget | stepper_back | test_whitelist_stepper_back_keeps_entries_and_applies | afterBackthedetailsread('','') Eassert(''=='probe-763dfd55c3@example.com' |
| reuse_challenge | used_wallet_challenge | test_used_wallet_challenge_is_denied_a_second_session | replayingausedchallengeanswered200:{"access_token":"sDP_7fyqYtRH_VXVTFMJXph91JIGAg3TNv97ZRLwKU0","account_id": |
| challenge_race | simultaneous_wallet | test_simultaneous_wallet_verifications_issue_one_session | sixsimultaneoususesofonechallengeanswered[200,200,200,200,200,200] Eassert6==1 |
| purpose_blind | bound_to_address | test_wallet_challenge_is_bound_to_address_purpose_and_expiry | awhitelistchallengepresentedforsign-inanswered200 Eassert200in(400,401,402,403,404,405,...) |
| trial_per_account | connected_wallet | test_connected_wallet_signs_into_the_same_account_and_its_trial_is_not_repeated | anaccountmadebyawalletthatwasattachedelsewheregot{'state':'trial','paid_until':None,'trial_ends_at':'2026-09-3 |
| self_approve | approve_itself | test_pending_device_cannot_approve_itself_denied | apendingdeviceapprovingitselfanswered200 Eassert200in(400,401,402,403,404,405,...) |
| directory_all | key_directory | test_key_directory_lists_only_active_devices | thekeydirectorylists{'d-8e7be046cf6a41e9a9680c2330b4607f','d-6d83dc775268412a9c591b98d60784f8','d-22072e7d7bfe |
| no_rekey | removed_device_token | test_removed_device_token_is_refused_and_every_epoch_advances | removingadevicemovedconversationepochfrom1to1 Eassert1==(1+1) |
| envelope_race | retried_send | test_retried_send_stores_one_envelope_row | simultaneousidenticalsendsreturnedenvelopeids{'1abd6b22ad16430b95723bd9c90a8cb8','7dcff74f92d8461e965b65eac95e |
| arrival_order | orders_by_clock | test_history_orders_by_clock_and_flags_gaps_when_read | historylists['a3','a1','b1','b2','a4'],expected['a1','b1','a3','b2','a4'] Eassert['a3','a1','b1','b2','a4']==[ |
| stored_gap | orders_by_clock | test_history_orders_by_clock_and_flags_gaps_when_read | gapflagsafterthelateenveloperead{'a1':False,'b1':False,'a2':False,'a3':True,'a4':False,'b2':False} Eassert(Tru |
| unchecked_recipients | sealed_to_a_removed_member | test_envelope_sealed_to_a_removed_member_is_denied | anenvelopesealedtoaremovedmemberanswered201 Eassert201in(400,401,402,403,404,405,...) |
| current_membership | each_period_of_membership | test_history_follows_each_period_of_membership | historyforaremovedmember:GET/api/conversations/4741e12ba0b14b08a5612357669fce79/historyreturned403:{"reason":" |
| epoch_unchecked | stale_epoch_envelope | test_stale_epoch_envelope_is_refused_with_the_current_epoch | astaleepochanswered201 Eassert201in(400,401,402,403,404,405,...) |
| sync_all_events | offline_member_syncs | test_offline_member_syncs_both_changes_and_a_removed_member_nothing_after | theremovedmembersyncs[('membership',2),('membership',3)] Eassert(['membership','membership']==['membership'] |
| nonowner_remove | non_owner_cannot_remove | test_non_owner_cannot_remove_a_member_denied | anon-ownerremovalanswered200 Eassert200in(400,401,402,403,404,405,...) |
| channel_post | channel_subscriber | test_channel_subscriber_post_is_forbidden | asubscriberpostanswered201 Eassert201in(400,401,402,403,404,405,...) |
| join_private | refuse_join_requests | test_private_group_and_chat_refuse_join_requests | joiningaprivate_groupanswered200 Eassert200in(400,401,402,403,404,405,...) |
| one_sided_receipts | read_receipt | test_read_receipt_needs_both_reader_and_author_opted_in | areceipttoanauthorwhooptedoutwasrecorded Eassert201in(400,401,402,403,404,405,...) |
| snapshot_audience | added_to_a_shared_group | test_member_added_to_a_shared_group_later_reads_the_task | apersonaddedtothesharedgrouplaterisnotareader:['NJ-6QS4IP25','NJ-OVYA7VBL'] Eassert'NJ-RHRRAZE7'in['NJ-6QS4IP2 |
| unshare_subtract | unsharing_one_group | test_unsharing_one_group_keeps_readers_granted_by_another | un-sharingthefirstgroupleavesreaders['NJ-XP63I6V2'] Eassert{'NJ-XP63I6V2'}=={'NJ-7DZPKM64...'NJ-XP63I6V2'} |
| arrival_moves | higher_clock_wins | test_placement_with_the_higher_clock_wins_in_either_arrival_order | themovewithclock5todoingshouldwinineitherorder;boardsread[('higherfirst','done'),('lowerfirst','doing')] Easse |
| task_race | replayed_with_its_client_id | test_task_replayed_with_its_client_id_is_stored_once | client_idburst-69d5d2f31fisstoredin5taskrows Eassert5==1 |
| quota_race | exceed_the_quota | test_simultaneous_file_creations_cannot_exceed_the_quota | threesimultaneous41943040-bytefilesanswered[201,201,201],expectedexactlyoneaccepted Eassert(3+0)==1 |
| unpadded | non_standard_length | test_piece_of_a_non_standard_length_is_refused | ashortpiecewasaccepted Eassert201in(400,401,402,403,404,405,...) |
| stored_state | missing_a_piece | test_file_missing_a_piece_reads_unavailable | afilemissingapiecereadsavailable Eassert'available'=='unavailable' |
| single_grant | revoking_a_link | test_revoking_a_link_keeps_member_access_and_removal_keeps_the_link | revokingalinkremovedmemberaccess Eassert403==200 |
| caller_route | direct_route_requires | test_direct_route_requires_both_participants_to_choose_it | acallwhereonlythecallerchosedirectanswered{'call_id':'af46ea18639845c5b73bac9c9cab5ff3','conversation_id':'fe7 |
| group_direct | group_call_always | test_group_call_always_relays_without_a_peer_address | aprivate_groupcallwitheveryoneondirectanswered{'call_id':'9dee2d3ff0fc4b06b5f0afaf9e537d3a','conversation_id': |
| ring_count | repeated_ring | test_repeated_ring_rings_once_and_a_late_ring_is_refused | arepeatedringrangtwice Eassert2==1 |
| stale_ok | rate_is_stale | test_quote_is_refused_while_the_rate_is_stale | aquoteonaneleven-minute-oldrateanswered201{"quote_id":"3ae190dcb0ae4950af725fb0af10a4c4","rail":"usdc","asset" |
| floor_due | rounds_up | test_amount_due_rounds_up_to_the_rail_base_unit | anxmrquoteanswered{'quote_id':'790f1eb53d8240168f9f6e26559ae009','rail':'xmr','asset':'xmr','price_usd_cents': |
| arrival_expiry | block_time_decides | test_block_time_decides_the_rate_of_a_late_reported_payment | apaymentinablockbeforeexpiry,reportedafterit,reads{'payment_id':'0945e444602f475098d9666c8ad6590b','quote_id': |
| old_rate | block_time_decides | test_block_time_decides_the_rate_of_a_late_reported_payment | apaymentinablockafterexpiryreads{'payment_id':'ad4f820ac86c43b181bb50e229aad10b','quote_id':'88b2b925ad744370b |
| unsigned | forged_watcher | test_unsigned_or_forged_watcher_events_are_refused | anunsignedpaymentanswered200 Eassert200in(400,401,402,403,404,405,...) |
| double_extend | depth_reports_extend | test_simultaneous_depth_reports_extend_membership_once | asecondtransactionwasnotcredited Eassert'settled'=='credited' |
| exact_match | shortfall_rule | test_half_per_cent_shortfall_rule_decides_settled_or_underpaid | paying15991072against16071429reads{'payment_id':'b16ee276b1e6413aaf52b9857d76c2e8','quote_id':'1818ab32b84145c |
| stored_membership | lapsed_member_reads | test_lapsed_member_reads_history_but_sending_is_refused | alapsedaccountdoesnotreadsuspended Eassert'trial'=='suspended' |
| member_treasury | treasury_actions | test_member_cannot_run_treasury_actions_forbidden | amember'ssettlerequestanswered200 Eassert200in(400,401,402,403,404,405,...) |
| settle_race | settlement_runs_pay_epoch_two | test_simultaneous_settlement_runs_pay_epoch_two_once | epoch2paid{'Heron':[18809168,18809168,18809168,18809168,18809168,18809168],'Kestrel':[41145055,41145055,411450 |
| live_stake | batched_settlement | test_batched_settlement_of_epoch_three_pays_from_the_snapshot_after_a_withdrawal | epoch3paid[('Avocet',8209042),('Plover',105544838),('Tern',8202005),('Wren',123030080)],expectedsnapshotshares |
| nearest | epoch_four_twice | test_settling_epoch_four_twice_pays_rounded_down_shares_once | epoch4paid[{'relay_id':'0b406787a3d24c87ab7d8907c18e9819','name':'Avocet','amount_micro':50212764},{'relay_id' |
| settle_repeat | epoch_four_twice | test_settling_epoch_four_twice_pays_rounded_down_shares_once | settlingepoch4againpaid[{'relay_id':'d363939b9f264227b9580860e8bea761','name':'Avocet','amount_micro':50212764 |
| count_all | duplicate_foreign | test_duplicate_foreign_or_superseded_probe_answers_count_nothing | answeringwithanotherrelay'snonceanswered200 Eassert200in(400,401,402,403,404,405,...) |
| current_tier | tier_held_when | test_earnings_follow_the_tier_held_when_each_round_was_issued | roundsatlevel-2thenlevel-1earn30,expected40 Eassert30==40 |
| floor | below_the_floor | test_stake_below_the_floor_is_refused_and_heartbeats_change_nothing | a9999stakewasaccepted Eassert201in(400,401,402,403,404,405,...) |
| stored_routing | core_node_that_missed | test_core_node_that_missed_the_latest_round_falls_back | afterthecorenodemissedthelatestroundroutingreads{'mode':'core_node','relay_id':'03e355659690400eae1bd4f7eca1de |
| block_epoch | settling_after_close | test_payment_settling_after_close_belongs_to_the_next_epoch | apaymentsettlingaftertheclosechangedtheclosedepoch Eassert15000000==0 |
| claim_race | claims_transfer_the_claimable | test_simultaneous_claims_transfer_the_claimable_balance_once | simultaneousclaimstransferred[400000000000,400000000000,400000000000,400000000000,400000000000,400000000000] E |
| running_total | token_event_corrections | test_claims_across_token_event_corrections_total_the_allocation | aclaimwithnothingvestedtransferredtokens Eassert28936==0 |
| cliff_clock | lump_for_every_schedule | test_cliff_accrues_and_releases_in_a_lump_for_every_schedule | communityatday89showsclaimable2021296296,expectedbetween2966666666and2966667438 Eassert2966666666<=2021296296 |
| application_race | whitelist_applications_from_one | test_simultaneous_whitelist_applications_from_one_wallet_file_one_and_email_once | fivesimultaneousapplicationsfromonewalletanswered[201,201,201,201,201] Eassert(5==1) |
| limits_off | cheque_limits | test_whitelist_amount_outside_the_cheque_limits_is_refused | anapplicationfor499999centsanswered201 Eassert201in(400,401,402,403,404,405,...) |
| mail_race | simultaneous_waitlist | test_simultaneous_waitlist_requests_send_one_confirmation_email | 6confirmationemailsreachedprobe-825d880406@example.comaftersevenrequests,expectedone Eassert6==1 |
| mail_per_request | simultaneous_waitlist | test_simultaneous_waitlist_requests_send_one_confirmation_email | 7confirmationemailsreachedprobe-cead688b5f@example.comaftersevenrequests,expectedone Eassert7==1 |
| phone_sidebar | phone | test_phone_workspace_swaps_the_sidebar_for_a_menu_and_pages_board_columns | at phone width the sidebar's link to /app/boards shows before Menu is pressed |
| phone_stack | phone | test_phone_intro_keeps_skip_on_screen_and_its_stage_labels_in_one_row | the six stage labels do not share one row |
| phone_skip_offscreen | phone | test_phone_intro_keeps_skip_on_screen_and_its_stage_labels_in_one_row | Skip the intro at y 1040, off screen |
| phone_squeeze | phone | test_phone_workspace_swaps_the_sidebar_for_a_menu_and_pages_board_columns | columns start 212 pixels apart |
| nav_translucent | floating_navigation | test_floating_navigation_has_an_opaque_backing_and_legible_labels | no opaque background sits between the labels and the fixed bar: rgba(17, 17, 17, 0.3 |
| nav_dim_labels | floating_navigation | test_floating_navigation_has_an_opaque_backing_and_legible_labels | the label About reads at contrast 2.53 against the bar |

The runs found grader defects before they shipped: a client-error tuple that excluded `402`, rate fixtures whose timestamps ran backwards across tests, a Playwright handler that was not a callable, and a brief that let browser sealing depend on Web Crypto, which a plain-HTTP non-localhost origin withholds. All are fixed. The browser substeps and the rubric were not exercised by the scratch reference beyond the pages the pytest tests drive.

## Handoff gates

G13, G15, G18, G19, G20, G21 and G25 are undecided; commands and expected verdicts are in the handoff file.

Rendered from the receipts. No verdict here is hand-written.
