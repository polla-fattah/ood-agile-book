---
title: "Chapter 12 Companion: Code, Explanations and Solutions"
weight: 120
description: "Code explanations and solutions for Chapter 12 Companion: Code, Explanations and Solutions."
---

*Measuring Progress, Flow and Technical Health*  
*OO Development and Agile Practices: Campus Equipment Lending*  

This companion supplies a small executable metrics exercise, worked calculations, the required repository-analysis method, a precise change specification and model answers. It follows the Week 11 syllabus. The application remains at Chapter 11; the Java calculator is a separate teaching tool, not a new lending feature or an analytics service.

The issue history is synthetic. The repository-lab template is blank by design: no real student repository has been inspected for this chapter, and no sample numbers are represented as real results. Complete that part with actual team evidence or an instructor-provided real export.

## 1. Files, toolchain and execution

The complete files appear under `File: lab/...` headings in the appendix. Create a directory named `lab` and copy each following fenced block into its named file. The TSV data uses actual tab characters and preserves empty fields, including trailing empty fields. Do not replace tabs with spaces or insert Markdown fences into the files.

| Tool or method | Pinned choice |
|---|---|
| Calculator | `FlowMetrics` v1.0, complete source in this file |
| Repository method | RM-12 v1.0, defined in Section 4 below |
| Java | Full JDK 17; locally checked with 17.0.20 |
| Build/test | Plain JDK compilation and explicit Java checks; no new dependencies |
| Optional Git provenance command | Git 2.51.1 syntax and locally inspected version |
| Running lending project | Chapter 11's Java 17 / Maven 3.9.11 version, unchanged |

From `lab`:

```bash
mkdir -p out
javac --release 17 -d out FlowMetrics.java FlowMetricsChecks.java
java -cp out FlowMetricsChecks
java -cp out FlowMetrics issues.tsv 2026-10-01T00:00:00Z 2026-10-11T00:00:00Z --scope
```

These commands use a POSIX-style terminal, including Git Bash on Windows. In another terminal, create `out` using its normal directory command; the `javac` and `java` arguments remain the same. A JRE alone is insufficient. The assertions throw explicitly, so the `-ea` option is not required.

Expected checks: `FlowMetricsChecks: 17 checks passed`.

Expected report:

```text
Completions in [from, until): 5
Completed points: 16
Mean lead days: 4.60
Mean cycle days: 2.80
Median cycle days: 3.00
WIP at until (after events at that instant): 2
Age E: 4.00 days
Age H: 3.00 days
at,scope_points,done_points,remaining_points,wip
2026-10-01T00:00:00Z,20,0,20,1
2026-10-02T00:00:00Z,20,0,20,2
2026-10-03T00:00:00Z,20,3,17,2
2026-10-04T00:00:00Z,23,5,18,1
2026-10-05T00:00:00Z,23,5,18,2
2026-10-06T00:00:00Z,25,10,15,2
2026-10-07T00:00:00Z,25,10,15,3
2026-10-08T00:00:00Z,23,13,10,3
2026-10-09T00:00:00Z,23,13,10,3
2026-10-10T00:00:00Z,23,16,7,2
2026-10-11T00:00:00Z,23,16,7,2
```

The `--scope` output samples every 24 hours from `from` through `until` when aligned. It is suitable for this midnight-UTC example. It is not a business-calendar or local-midnight plotting engine. Real PR data normally uses the summary without `--scope` because point estimates are unavailable or inappropriate.

## 2. Data contract and code explanation

### Schema

Each TSV line has exactly six fields. There is no quoting or escaping syntax; use stable IDs without tabs or newlines. The file must have the exact header shown in the appendix.

| Field | Meaning | Missing value |
|---|---|---|
| `id` | Unique work-item ID within this input | Invalid |
| `points` | Nonnegative integer estimate held fixed in this example | Blank means unknown, not zero |
| `accepted` | Timestamp admitted to tracked scope | Invalid |
| `started` | Timestamp at the chosen start boundary | Blank means not started |
| `done` | Timestamp at the chosen finish boundary | Blank means not completed |
| `removed` | Explicit cancellation/removal timestamp | Blank means not removed |

Use ISO-8601 instants such as `2026-10-06T00:00:00Z`, with a timezone offset if converting an original timestamp. Do not submit a bare local time. Preserve original timestamps and their timezone in the evidence record as well as any normalised UTC value.

`Item` rejects start-before-acceptance, completion without a start, completion before start, and contradictory done/removed states. `read` rejects duplicate IDs and the wrong number of fields. Unknown points produce `NA` for completed points if any completed item lacks an estimate; they do not prevent duration calculations. Scope-point output rejects missing estimates rather than inventing them.

The model permits a removed item to have been started; that item leaves WIP at removal but never counts as Done. It does not model reopening, multiple blocked intervals, changing estimates, parent/child aggregation or completed work later removed from the product. Use an event-history model for those cases rather than forcing them into these six columns. Input validity does not prove that the source population is complete or the timestamps reflect the claimed workflow.

### Calculation responsibilities

`completed` selects Done instants in `[from, until)`. `summarize` uses that cohort for count, points, lead and cycle statistics, and separately inspects all supplied rows for WIP at `until`. This deliberately permits carried-in work: an item can start before the window and finish within it.

`inProgress` treats an item as open once its Started event has occurred and until Done or Removed occurs. Events exactly at the snapshot instant are already applied. A completion at `until` is therefore excluded from that interval's throughput and also excluded from WIP at that snapshot. There is no contradiction: one is a count over a half-open period, the other a state after boundary events.

`days` uses elapsed seconds and nanoseconds divided by 86,400 seconds. It does not call `Duration.toDays`, which would truncate partial days. This matters for real PR timestamps: a one-hour interval is approximately 0.041667 days, not zero. Output is rounded to two decimals for reading; calculations retain unrounded doubles.

An empty completion cohort yields zero completions and `NA` durations, because an average over no observations is not a measured zero-day average. Completed points for that empty cohort are zero as a sum. The median sorts completed cycle times and uses the middle value, or the average of the two central values for an even-sized cohort.

`scopePoints` and `donePointsAt` support this example's fixed estimates and explicit removals. The first includes accepted items not removed as of the snapshot; the second includes completion events at or before it. They do not infer scope from Git commits.

### Meaningful checks

The 17 checks protect independently useful properties: correct example totals and durations; scope addition/removal; completion-window boundaries; WIP at a completion instant; fractional elapsed days; empty-cohort handling; unknown estimates; and invalid event order. They are plain-Java teaching checks, not additions to the running application's JUnit count.

For an optional fault experiment, use a separate copy. In `completed`, replace:

```java
i.done().isBefore(until)
```

with:

```java
!i.done().isAfter(until)
```

Recompile and run `FlowMetricsChecks`. The check named `Exclusive upper bound` must fail: B at 6 October is incorrectly counted in the first window. Restore the expression and rerun. This experiment concerns a reporting interval, not a change to `LoanPeriod` or the overdue policy.

## 3. Worked calculations and interpretation

### Finished cohort

| ID | Lead calculation | Lead days | Cycle calculation | Cycle days |
|---|---|---:|---|---:|
| A | 03 − 01 | 2 | 03 − 01 | 2 |
| B | 06 − 01 | 5 | 06 − 02 | 4 |
| C | 04 − 01 | 3 | 04 − 03 | 1 |
| D | 08 − 01 | 7 | 08 − 05 | 3 |
| G | 10 − 04 | 6 | 10 − 06 | 4 |
| Total | | 23 | | 14 |

Mean lead = `23 / 5 = 4.6` elapsed days. Mean cycle = `14 / 5 = 2.8` elapsed days. Sorted cycles are `1, 2, 3, 4, 4`, so the median is three. Waiting before start totals nine days and averages 1.8, consistent with `4.6 − 2.8` for this same cohort.

B's blocked interval `[03,05)` contributes two elapsed days within its four-day cycle. Subtracting those two days would make the cohort total 12 and mean 2.4, not two. Even 2.4 is not the defined cycle-time statistic and cannot be called coding time without further evidence.

### Scope and completion reconciliation

Initial scope = `3 + 5 + 2 + 3 + 5 + 2 = 20` points. Added scope = `G(3) + H(2) = 5`. Removed scope = `F(2)`. Final scope = `20 + 5 − 2 = 23`. Completed points = `A(3) + B(5) + C(2) + D(3) + G(3) = 16`. Remaining = `23 − 16 = 7`, exactly `E(5) + H(2)`.

Throughput is five items in ten elapsed days, or 0.5 item per elapsed day as a rate over this interval. It is not 16 items and not six items. A and C finish in `[01,06)`; B, D and G finish in `[06,11)`. There is no double counting at the shared boundary.

At 11 October, E has age `11 − 07 = 4` days and H has age `11 − 08 = 3` days. Neither has a known completed cycle time. F was removed before starting, so it is neither WIP nor Done. A daily WIP count is a snapshot; it is not an average WIP over all instants.

### Cautious interpretation example

“The synthetic iteration finished five items and 16 points. Scope grew by five points and later lost two, leaving seven points across two open items. The remaining-work rise on day 04 reflects a scope addition despite a completion. Completed cycle time averages 2.8 days, while the current open items have ages four and three days. B has a recorded two-day wait for clarification, but this small history cannot establish the causes of all delays. Before forecasting the approval change, inspect E's unresolved issue and agree the approval data contract.”

This paragraph distinguishes facts, limitations and a next action. It does not claim real team performance or assign responsibility to a person.

## 4. RM-12 v1.0: required real repository lab

This is the pinned repository-metrics method for this chapter. It uses genuine issue/PR events and the same Java 17 calculator; no paid dashboard, API account or repository-analysis library is necessary. A hosting provider's UI or an authorised export can supply the data. The source must be real even when an instructor prepares the export.

### Route A: PR open-to-merge duration: minimum route

1. **Choose a source and rule.** Record repository URL, target branch, fixed UTC interval, extraction timestamp and inclusion rule. For a small exercise, select the first five qualifying merged PRs ordered by merge time and then PR number within the interval; if fewer exist, use all and report the actual count. State whether bots, draft PRs and documentation changes are included before selection. This is a bounded duration sample, not repository throughput.
2. **Keep provenance.** For each selected PR retain its URL/ID, original opened timestamp, merged timestamp and target branch. Inspect its event history. Exclude or separately document reopened PRs because the supplied one-interval model cannot express multiple open/closed episodes. Use actual precise timestamps; if the UI only gives relative dates, obtain an export with exact timestamps or report that precise calculation is blocked. Do not guess midnight.
3. **Map the data.** Set `accepted` and `started` both to the PR opened instant; set `done` to its actual merged instant. Leave `points` and `removed` blank. Give it a stable ID such as `PR-42`. These boundaries intentionally make printed lead and cycle equal; report the result as PR open-to-merge duration, not issue lead time. Do not infer acceptance into a backlog from PR opening.
4. **Calculate.** Save the normalised six-column file as `repository.tsv`. Run the calculator with the chosen interval and without `--scope`. Manually verify the longest selected duration using its two timestamps. Record count, median and mean for the sample, plus the observed range if helpful.
5. **Interpret and review.** State that coding may begin before a PR opens; draft/review waiting remains included; a merge need not be deployed or accepted by a user; the sample may differ from the full population. Ask a peer to trace one row back to the source, or label a solo provenance check accurately.

Example command shape, using your actual interval:

```bash
java -cp out FlowMetrics repository.tsv 2026-10-01T00:00:00Z 2026-10-11T00:00:00Z
```

Those dates are the book example's window, not a required window for a real repository. Replace them if they do not match your selection. If the input contains only merged sample PRs, do not interpret the displayed WIP as repository WIP: open PRs were not supplied.

### Route B: complete-window throughput and open work

To report repository PR throughput, enumerate **all** qualifying merged PRs in the chosen branch and `[from, until)` interval. Check pagination and filters; record the number of results and any exclusions. Do not filter by opened date, because that would lose carried-in work. The completion count then measures merges of the stated PR unit, not finished user stories or deployments.

To report WIP at `until`, also include every qualifying PR opened at or before that instant that had neither merged nor closed at that instant. Historical snapshots require event history: a PR merged after `until` was still open at `until`. The calculator can retain the later Done event and correctly treat it as open at the snapshot. A PR closed without merging maps to `removed`, not `done`. Capture such rows where needed to reconstruct historical state. Record any reopened cases separately or use a richer event model.

Only a complete population supports full-window throughput/WIP claims. A small verified duration sample is sufficient for Route A and fulfils the required repository-duration exercise; do not mislabel it as Route B. Issue exports are an alternative when they include genuine Started/Done transition history and the same explicit completeness checks. In that route, define what “accepted” actually means before using it.

### Optional Git cross-check

For a local repository, Git 2.51.1 can provide a compact provenance inventory without collecting names or emails:

```bash
git --version
git rev-parse HEAD
git log --first-parent -20 --format='%H%x09%cI'
```

`%H` is the commit hash and `%cI` the strict ISO committer timestamp. First-parent traversal changes the history being inspected. These records may help match a PR to a revision, but they do not supply PR-open times or prove deployment. The last 20 commits are not a complete interval export, and commit counts are not substituted for the required PR/issue measure.

### Evidence template: fill with observed data

| Field | Your record |
|---|---|
| Repository and target branch | |
| Source interface/export and extraction timestamp | |
| Interval and timezone convention | |
| Unit; accepted/start/finish meanings | |
| Inclusion rule; excluded event histories | |
| Route A sample rule or Route B completeness evidence | |
| Raw IDs/URLs and exact timestamps | |
| Normalised file and command | |
| Number analysed; mean; median; longest manual check | |
| Throughput/WIP, only if supported by complete input | |
| One uncertainty; one defensible next question | |
| Reviewer and actual feedback, or solo review | |

A zero-completion interval is a valid result; report it and retain `NA` durations. If the team has no usable history, use an instructor-provided real repository export or inspect a suitable public repository. Do not manufacture commits or PRs to claim historical evidence. Synthetic data may be used to practise the commands while arranging the real input, but the real-data lab remains unfinished until that input is examined.

## 5. CR-12: worked change specification for Chapter 13

**Status:** specified teaching change; implementation pending. It is not institutional policy and does not substitute for the team's separately released assessment variant. These choices make the example concrete enough to implement and verify without reopening its basic scope in Chapter 13.

### Behaviour and data decisions

| ID | Book contract |
|---|---|
| CR12-1 | Add a recognised `VISITOR` borrower category. Legacy directory code `V` maps to it. Existing `S`/`T`, inactive and unknown-code behaviour stays as documented; unknown codes never default to STUDENT. |
| CR12-2 | Visitors may request only CAM1 or CAM2, for one, two or three calendar days. Use the existing half-open loan period. Zero/negative duration and four or more days are rejected. |
| CR12-3 | Reuse the student count limit: fewer than three retained reservations for that borrower before adding one. This is the existing repository-count convention, not an active-loan count. |
| CR12-4 | A visitor needs one matching trusted approval record for the exact tuple `(borrowerId, itemId, start, endExclusive)`. The record must have a nonblank sponsor ID and status APPROVED. Approval for another borrower, item or period is insufficient. |
| CR12-5 | Capture one request-time instant from an injected `Clock`. A record is valid when `validFrom <= now < validUntil`. Equality at expiry is invalid. The loan period need not lie inside the approval-validity window; that window governs when the reservation may be requested. |
| CR12-6 | A missing match, DENIED status or an out-of-window record is an expected rejection. It creates no reservation and sends no confirmation. |
| CR12-7 | An unreadable register, malformed row, duplicate request key, unknown status or invalid validity interval is an operational failure. It also creates no reservation and sends no confirmation, but is distinguishable from sponsor rejection. No fallback approval or empty-success response. |
| CR12-8 | Once approval and existing checks succeed, create the reservation and use existing confirmation behaviour. Retain the current rule that an expected notification failure leaves an already-created reservation in place. |
| CR12-9 | The initial release has one `visitingResearchersEnabled` flag, default false. Disabled visitor requests are explicitly rejected without reading the approval register. Student/staff requests use their existing path under either setting and never require sponsor approval. |
| CR12-10 | Approval is checked at reservation time only. Expiry or disabling the flag later does not cancel an existing reservation or block its normal checkout/return. Revocation after reservation is outside this exercise. |

The current direct category-taking entry point and the older overload that defaults to STUDENT are trusted teaching APIs, not authentication boundaries. Directory-backed requests obtain their category from the directory; arbitrary caller-supplied categories do not establish real-world identity. Do not claim this exercise prevents hostile impersonation. A production authorisation system would need separate requirements and evidence.

**SD-12: count semantics:** `ReservationCoordinator` calls its variable `activeCount` but counts all stored reservations. Returning a loan does not remove its reservation. Preserve this behaviour for the worked change and record the question: should a future authorised rule count active loans, future reservations, or all retained reservations? Renaming the local variable for clarity is possible as a separate structural edit; changing the count is a functional decision. SD-11's due-today report behaviour also remains unresolved and unchanged.

### Planned approval-register boundary

Choose a local UTF-8 TSV file with exactly eight columns:

```text
borrowerId	itemId	start	endExclusive	sponsorId	status	validFrom	validUntil
```

Each column is separated by a tab; the example data below contains actual tabs. IDs cannot contain tabs or newlines. Dates are ISO local dates; validity timestamps are ISO instants. Status is exactly APPROVED or DENIED. Require `start < endExclusive` and `validFrom < validUntil`. Reject a malformed register as a whole, including an invalid unrelated row; do not silently skip bad records. Require unique request keys within one read. The file is treated as a trusted, sequential example, not an atomic concurrent approval database.

**Synthetic valid example for the future implementation:**

```tsv
borrowerId	itemId	start	endExclusive	sponsorId	status	validFrom	validUntil
V1	CAM1	2026-10-20	2026-10-22	S1	APPROVED	2026-10-18T00:00:00Z	2026-10-20T00:00:00Z
```

At request instant `2026-10-19T12:00:00Z`, this approves V1's two-day CAM1 request starting 20 October. At `2026-10-20T00:00:00Z`, the same approval has expired. The row is a specification example, not input to `FlowMetrics`, and there is no approval parser implemented in Chapter 12.

A candidate application port can obtain the approval decision for a request; its file adapter performs actual I/O and validation. Keep deterministic membership/duration rules apart from source access and time. Do not force identity/approval information into `BorrowingPolicy.mayRequest(count, days)` through a global flag. Chapter 13 should decide the smallest interface shape that satisfies these examples and fits the existing orchestration.

### Acceptance matrix

In visitor success/rejection rows assume a recognised active V1, flag enabled, fewer than three retained reservations, available equipment, valid identifiers and an ordinary working notification sender, except where the row changes one condition. Construct every example independently so one failure does not mask another.

| Example | Input difference | Expected observation |
|---|---|---|
| AC1 | CAM1, two days, matching approved record valid at request time | One new reservation; existing confirmation format; one notice |
| AC2 | CAM2, three days with its own matching record | Allowed; upper duration boundary preserved |
| AC3 | Four days, otherwise matching approval | Reject; no state or notice change |
| AC4 | Zero or negative days | Reject; no state or notice change |
| AC5 | Item MIC1 with matching approval | Reject because item is outside visitor allowlist |
| AC6 | Missing approval or DENIED record | Expected rejection; no state or notice change |
| AC7 | Approval belongs to V2, CAM2 or a different end date | Does not authorise the V1/CAM1/requested-period tuple |
| AC8 | `now == validFrom` | Valid if all other conditions hold |
| AC9 | `now == validUntil`, or before validFrom | Rejected as invalid at request time |
| AC10 | Unreadable file, malformed row or duplicate matching key | Distinct operational failure; no state or notice change |
| AC11 | Three retained reservations already exist | Reject count limit even if loans have been returned |
| AC12 | Visitor feature disabled | Explicit disabled result; approval source not called |
| AC13 | Existing student/staff request, either flag setting | Existing result and notification behaviour; approval source not called |
| AC14 | Visitor's approved item overlaps an existing reservation | Existing availability rejection; no extra reservation or notice |
| AC15 | Valid visitor succeeds but expected notification failure occurs | Reservation retained; existing notification-failure outcome |
| AC16 | Visitor reservation created, then approval expires or flag turns off | Existing checkout/return flow remains available |
| AC17 | Unknown directory code or inactive visitor | Existing unknown/inactive semantics; never default to student |
| AC18 | Report generated after a visitor loan exists | Existing report mapping and SD-11 boundary retained |

These are planned examples, not claims that new tests have run. Existing policy tests, directory tests, command tests and the 159-test Chapter 11 suite remain relevant. Some test setups that enumerate every category will require explicit updates because adding an enum value changes their setup; document that necessary example change without weakening old assertions.

### Ordered backlog and impact note

| ID | Ordered work | Dependency | Exit evidence |
|---|---|---|---|
| C12-1 | Preserve baseline and confirm CR12/SD12 examples | Chapter 11 source | Passing baseline result; retained revision/copy; reviewed contract |
| C12-2 | Add recognised visitor path, policies and explicit wiring | C12-1 | Valid visitor with controlled approval source; old categories still behave correctly |
| C12-3 | Implement and test actual approval-file adapter | C12-1 data contract; connect after C12-2 | Temporary-file success, malformed/missing/duplicate failures; no mock replacing the reader under test |
| C12-4 | Complete matching/time/failure and no-mutation protection | C12-2, C12-3 | AC boundary and operational-failure evidence |
| C12-5 | Introduce one flag and integrate CLI/demo | C12-2–4 | Both settings; old path; existing reservations usable after disable |
| C12-6 | Run full regression, real boundary checks and delivery workflow | C12-2–5 | Observed pipeline/local gate, repeatable demonstration and retrospective for Chapter 13 |

Status of C12-2–6 in this chapter: **planned, not implemented**. C12-1's source preservation is supplied here; the learner records their actual baseline result and review. Do not assign owners, dates or points as if a real team had agreed them. Add those during the team planning activity, using its capacity and dependencies.

**Impact rationale:** category recognition reaches the directory and wiring; the coordinator enforces every-category policy availability; sponsor approval requires request identity/time that the existing count/duration interface lacks; the file reader needs integration checks; failures must be distinguished before a new reservation is added. The existing repository, loan lifecycle and report do not need a broad redesign for this narrow requirement. Concurrent approval updates and revocation remain outside scope.

**Flag plan:** default off; enable only for the controlled demonstration after both paths pass. Disabling prevents new visitor reservations, but does not erase existing data or roll back arbitrary side effects. Keep the pre-change revision for code comparison. Record a removal decision during Chapter 14 once the intended release path is accepted; do not let an unnamed temporary flag become permanent by default. No public production deployment is required.

## 6. Preserve the pre-change version

The supplied Chapter 11 code is the baseline; this chapter makes no edits to its production classes, tests or build file. Its last delivered full run passed 159 JUnit invocations. The metrics tool lives outside that Maven project and has its own checks; do not add its check count to the baseline's count.

For your working project, first run its documented gate from its project root:

```bash
mvn --batch-mode verify
```

Retain the command, actual result, Java/Maven versions and any failure explanation. In a Git project inspect:

```bash
git status --short
git rev-parse HEAD
```

A commit ID is a sufficient source reference only when the intended baseline files are committed. If the working tree includes changes or untracked files, retain them in a separate complete source copy or make a deliberate scoped commit before recording the baseline. A tag alone does not capture uncommitted work. Avoid resetting the project or overwriting unrelated work to make this record look clean.

For learners assembling source from Markdown without Git, copy the complete Chapter 11 project directory as `pre-change-ch12` before making Chapter 13 changes. Keep `src`, build configuration, resources and scripts. Generated `target` files are reproducible and need not be preserved as source. Keep a record of the copied file set and the successful command.

Suggested record:

```text
Baseline: Chapter 11 cumulative project
Source revision or complete-copy location:
Uncommitted/untracked source accounted for:
Java and Maven versions:
Command and actual result:
SD-11: due-today inclusion preserved; policy unresolved
SD-12: retained-reservation count preserved; policy unresolved
CR-12: specified; implementation pending
Reviewer or explicitly labelled solo review:
```

## 7. Model answers and lab reasoning

### Chapter 12.8: AI review

| Candidate claim | Judgement and correction |
|---|---|
| Six items / 18 points delivered | Contradicted: F is removed, not Done. Five items and 16 points completed. |
| Mean cycle is two after subtracting blocking | Contradicted: defined mean is 2.8. Subtracting B's two days would give 2.4, and would change the measure. |
| Day 04 rise proves productivity declined | Not established: G adds three points while C completes two. The remaining line rises by one. |
| Day 08 fall proves five points delivered | Contradicted: D completes three; F removes two. |
| Legacy architecture caused waiting | Not established: one mapping clarification is recorded; broad causality needs more evidence. |
| Remaining work definitely finishes in 0.44 iterations | Unsupported forecast: the division is approximately right, but comparability, capacity and uncertainty are missing. |
| Rank members by commits | Reject the recommendation: commits do not measure individual value or identify the cause of delay. |

A corrected response can use the cautious interpretation in Section 3. A useful next step is to inspect E's unresolved problem and settle the approval data contract. That is actionable without inventing a productivity diagnosis.

### Chapter 12.11: concept questions

**1. Lead versus cycle.** Accepted-to-Done includes the pre-start queue; Started-to-Done does not. B has lead five and cycle four. Another team's “lead time” might begin at a customer request rather than admission to scope, so the number cannot travel without its event definition and elapsed/business-time convention.

**2. Falling burn-down.** Removing F reduces remaining scope by two while delivering nothing. Re-estimation could also move a line under another data model. Keep a scope event record and distinguish the completed and scope lines in a burn-up.

**3. Equal throughput.** Two periods can each finish two items whose earlier start dates differ. A carried-in seven-day item and a newly completed one-day item can contribute equally to the period's count. Recipients experience different waiting even when completion totals match.

**4. Old versus new behaviour.** The existing tests describe selected existing contracts. They do not contain sponsor-approval requirements and cannot establish those requirements by passing. Keep them, add new acceptance/unit/integration checks for CR-12, and examine any changes to test setups required by the new category.

### Chapter 12.11: applied diagnosis

**5. Biased cohort.** Filtering on both start and finish being within the week excludes long-running carried-in work that finished this week. Define the completion cohort by the finish event and compute durations from actual start timestamps, even before the window. Report unfinished-item age separately. A start-cohort study is possible, but it answers another question and includes censored unfinished observations.

**6. Global approval Boolean.** Approval belongs to a specific borrower/item/period at a specific time. A static flag loses that identity and can leak across requests and tests. The current `BorrowingPolicy` contract deliberately handles count/duration only. Obtain a typed approval decision through an application boundary; validate its match and time using explicit inputs before reservation creation. Retain a pure count/duration policy. A global “approved” state is not an adequate record or security mechanism.

### Chapter 12.11: ML serving transfer

Choose a unit such as one requested release of a named model version to a stated serving environment. Define Done as the approved version being demonstrably served at that boundary with required checks, not merely a successful build. Keep build, approval and activation timestamps separate. An unavailable approval registry must not be treated as permission to serve.

Plan a narrow valid activation path, mismatched/expired/denied approval outcomes if those concepts are required, and registry failure evidence. Test the genuine registry boundary separately from orchestration doubles. Preserve the old serving path and record how disabling the new release path affects already active versions. Model accuracy concerns predictive behaviour under an evaluation design; build success concerns construction checks; approval is a governance decision. None substitutes for the others.

### Chapter 12.10: lab completion reasoning

the book's project produces the calculations, corrected interpretation, CR-12 plan and baseline reference. your team's project contributes real repository evidence and an impact note for its actual released change. Accept different task splits and interfaces when they preserve the observation boundaries and have defensible dependencies. Do not assess by number of commits, charts or AI prompts.

A good impact note identifies the concrete touchpoints, uncertainty and first experiment. A weak note merely lists class names or repeats “add tests.” A good repository result includes traceable timestamps and honest population scope; an attractive chart with guessed timestamps is not an acceptable replacement.

## 8. Verification record and limits

The supplied calculator was compiled at Java release 17 and its 17 checks passed. The exact synthetic report above was executed. A separate boundary-mutant copy was checked to confirm the exclusive-window assertion detects the deliberately inclusive upper bound; restoration returned the checks to green. The Markdown file listings were reconstructed and run before delivery.

An independent calculation also reconciled the eight source rows, five completions, 16 completed points, 23 final scope points, seven remaining points, the five-item duration means and the daily chart table. Chapter 11's source was retained without modification. Its prior 159-test result is a baseline reference, not a newly implemented CR-12 result.

No student repository or actual PR history has been analysed in this authoring run. RM-12 supplies the procedure and blank evidence record for that required learner activity. No sponsor approval, stakeholder acceptance, hosted pipeline or peer review is claimed. CR-12's adapter, tests and feature flag are specifications for Chapter 13. The calculator does not handle reopened histories, revised estimates or business calendars.

Sources and assigned reading are listed in the main chapter. All sample records, contracts, code and answers here are original teaching material.

## Appendix: Complete isolated Java exercise

Keep these files outside the running lending application's source roots. The two Java classes have no package declaration so the plain-JDK commands above work as written.

### File: lab/issues.tsv

````tsv
id	points	accepted	started	done	removed
A	3	2026-10-01T00:00:00Z	2026-10-01T00:00:00Z	2026-10-03T00:00:00Z	
B	5	2026-10-01T00:00:00Z	2026-10-02T00:00:00Z	2026-10-06T00:00:00Z	
C	2	2026-10-01T00:00:00Z	2026-10-03T00:00:00Z	2026-10-04T00:00:00Z	
D	3	2026-10-01T00:00:00Z	2026-10-05T00:00:00Z	2026-10-08T00:00:00Z	
E	5	2026-10-01T00:00:00Z	2026-10-07T00:00:00Z		
F	2	2026-10-01T00:00:00Z			2026-10-08T00:00:00Z
G	3	2026-10-04T00:00:00Z	2026-10-06T00:00:00Z	2026-10-10T00:00:00Z	
H	2	2026-10-06T00:00:00Z	2026-10-08T00:00:00Z		
````

### File: lab/FlowMetrics.java

````java
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Objects;

/** Chapter 12 teaching tool v1.0. TSV input, UTC instants, elapsed 24-hour days. */
public final class FlowMetrics {
    public record Item(String id, Integer points, Instant accepted, Instant started,
                       Instant done, Instant removed) {
        public Item {
            if (id == null || id.isBlank()) throw new IllegalArgumentException("Blank id");
            if (points != null && points < 0) throw new IllegalArgumentException("Negative points");
            Objects.requireNonNull(accepted, "accepted");
            if (started != null && started.isBefore(accepted))
                throw new IllegalArgumentException("Start before acceptance: " + id);
            if (done != null && (started == null || done.isBefore(started)))
                throw new IllegalArgumentException("Invalid completion: " + id);
            if (removed != null && (done != null || removed.isBefore(accepted)
                    || (started != null && removed.isBefore(started))))
                throw new IllegalArgumentException("Invalid removal: " + id);
        }
    }

    public record Summary(int completed, String completedPoints, double meanLeadDays,
                          double meanCycleDays, double medianCycleDays, int wip) { }

    private FlowMetrics() { }

    public static List<Item> read(Path path) throws Exception {
        var lines = Files.readAllLines(path);
        String header = "id\tpoints\taccepted\tstarted\tdone\tremoved";
        if (lines.isEmpty() || !lines.get(0).equals(header))
            throw new IllegalArgumentException("Expected exact TSV header");
        List<Item> result = new ArrayList<>();
        var ids = new HashSet<String>();
        for (int line = 1; line < lines.size(); line++) {
            if (lines.get(line).isBlank()) continue;
            String[] f = lines.get(line).split("\t", -1);
            if (f.length != 6) throw new IllegalArgumentException("Six fields required at line " + (line + 1));
            if (!ids.add(f[0])) throw new IllegalArgumentException("Duplicate id: " + f[0]);
            result.add(new Item(f[0], f[1].isEmpty() ? null : Integer.valueOf(f[1]),
                    parse(f[2]), parse(f[3]), parse(f[4]), parse(f[5])));
        }
        return List.copyOf(result);
    }

    private static Instant parse(String text) {
        return text.isEmpty() ? null : Instant.parse(text);
    }

    public static double days(Instant start, Instant end) {
        Duration d = Duration.between(start, end);
        return d.getSeconds() / 86400.0 + d.getNano() / 86400_000_000_000.0;
    }

    public static List<Item> completed(List<Item> items, Instant from, Instant until) {
        if (!from.isBefore(until)) throw new IllegalArgumentException("Empty or reversed window");
        return items.stream().filter(i -> i.done() != null && !i.done().isBefore(from)
                && i.done().isBefore(until)).toList();
    }

    public static boolean inProgress(Item i, Instant at) {
        return i.started() != null && !i.started().isAfter(at)
                && (i.done() == null || i.done().isAfter(at))
                && (i.removed() == null || i.removed().isAfter(at));
    }

    public static Summary summarize(List<Item> items, Instant from, Instant until) {
        List<Item> cohort = completed(items, from, until);
        double[] cycles = cohort.stream().mapToDouble(i -> days(i.started(), i.done())).sorted().toArray();
        double lead = cohort.stream().mapToDouble(i -> days(i.accepted(), i.done())).average().orElse(Double.NaN);
        double cycle = java.util.Arrays.stream(cycles).average().orElse(Double.NaN);
        double median = cycles.length == 0 ? Double.NaN : cycles.length % 2 == 1
                ? cycles[cycles.length / 2] : (cycles[cycles.length / 2 - 1] + cycles[cycles.length / 2]) / 2;
        String points = cohort.stream().anyMatch(i -> i.points() == null) ? "NA"
                : Long.toString(cohort.stream().mapToLong(i -> i.points()).sum());
        return new Summary(cohort.size(), points, lead, cycle, median,
                (int) items.stream().filter(i -> inProgress(i, until)).count());
    }

    public static long scopePoints(List<Item> items, Instant at) {
        return items.stream().filter(i -> !i.accepted().isAfter(at)
                && (i.removed() == null || i.removed().isAfter(at))).mapToLong(i -> {
                    if (i.points() == null) throw new IllegalArgumentException("Scope point missing: " + i.id());
                    return i.points();
                }).sum();
    }

    public static long donePointsAt(List<Item> items, Instant at) {
        return items.stream().filter(i -> i.done() != null && !i.done().isAfter(at)).mapToLong(i -> {
            if (i.points() == null) throw new IllegalArgumentException("Done point missing: " + i.id());
            return i.points();
        }).sum();
    }

    private static String number(double n) {
        return Double.isNaN(n) ? "NA" : String.format(Locale.ROOT, "%.2f", n);
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 3 && args.length != 4)
            throw new IllegalArgumentException("Usage: FlowMetrics file.tsv fromInstant untilInstant [--scope]");
        if (args.length == 4 && !args[3].equals("--scope")) throw new IllegalArgumentException("Unknown option");
        List<Item> items = read(Path.of(args[0]));
        Instant from = Instant.parse(args[1]);
        Instant until = Instant.parse(args[2]);
        Summary s = summarize(items, from, until);
        System.out.println("Completions in [from, until): " + s.completed());
        System.out.println("Completed points: " + s.completedPoints());
        System.out.println("Mean lead days: " + number(s.meanLeadDays()));
        System.out.println("Mean cycle days: " + number(s.meanCycleDays()));
        System.out.println("Median cycle days: " + number(s.medianCycleDays()));
        System.out.println("WIP at until (after events at that instant): " + s.wip());
        for (Item i : items) if (inProgress(i, until))
            System.out.println("Age " + i.id() + ": " + number(days(i.started(), until)) + " days");
        if (args.length == 4) {
            System.out.println("at,scope_points,done_points,remaining_points,wip");
            for (Instant at = from; !at.isAfter(until); at = at.plus(Duration.ofDays(1))) {
                long scope = scopePoints(items, at);
                long done = donePointsAt(items, at);
                Instant sample = at;
                long wip = items.stream().filter(i -> inProgress(i, sample)).count();
                System.out.println(at + "," + scope + "," + done + "," + (scope - done) + "," + wip);
            }
        }
    }
}
````

### File: lab/FlowMetricsChecks.java

````java
import java.nio.file.Path;
import java.time.Instant;
import java.util.List;

/** Plain Java checks throw explicitly; -ea is not required. */
public final class FlowMetricsChecks {
    private static int checks;
    private static Instant day(int n) { return Instant.parse("2026-10-%02dT00:00:00Z".formatted(n)); }
    private static void check(boolean value, String description) {
        checks++;
        if (!value) throw new AssertionError(description);
    }
    private static void invalid(Runnable operation, String description) {
        checks++;
        try { operation.run(); } catch (IllegalArgumentException expected) { return; }
        throw new AssertionError(description);
    }
    public static void main(String[] args) throws Exception {
        var data = FlowMetrics.read(Path.of("issues.tsv"));
        var s = FlowMetrics.summarize(data, day(1), day(11));
        check(s.completed() == 5 && s.completedPoints().equals("16"), "Count and points differ");
        check(Math.abs(s.meanCycleDays() - 2.8) < 1e-9, "Mean cycle");
        check(Math.abs(s.meanLeadDays() - 4.6) < 1e-9, "Mean lead");
        check(s.medianCycleDays() == 3, "Median cycle");
        check(s.wip() == 2, "Open items remain WIP");
        check(FlowMetrics.scopePoints(data, day(4)) == 23, "Added scope counted");
        check(FlowMetrics.scopePoints(data, day(8)) == 23, "Removed scope excluded");
        check(FlowMetrics.donePointsAt(data, day(8)) == 13, "Removal is not completion");
        check(FlowMetrics.completed(data, day(1), day(6)).size() == 2, "Exclusive upper bound");
        check(FlowMetrics.completed(data, day(6), day(11)).size() == 3, "Inclusive lower bound");
        check(!FlowMetrics.inProgress(data.get(1), day(6)), "Done at snapshot is not WIP");
        check(Math.abs(FlowMetrics.days(day(1), day(1).plusSeconds(3600)) - 1.0 / 24) < 1e-9,
                "Do not truncate fractional days");
        var empty = FlowMetrics.summarize(List.of(), day(1), day(2));
        check(empty.completed() == 0 && Double.isNaN(empty.meanCycleDays()), "No completions is not zero duration");
        var unknown = new FlowMetrics.Item("PR1", null, day(1), day(1), day(2), null);
        check(FlowMetrics.summarize(List.of(unknown), day(1), day(3)).completedPoints().equals("NA"), "Unknown points");
        invalid(() -> new FlowMetrics.Item("X", 1, day(2), day(1), null, null), "Invalid ordering rejected");
        invalid(() -> new FlowMetrics.Item("X", 1, day(1), day(1), day(2), day(3)), "Done plus removed rejected");
        invalid(() -> FlowMetrics.summarize(data, day(3), day(3)), "Invalid window rejected");
        System.out.println("FlowMetricsChecks: " + checks + " checks passed");
    }
}
````