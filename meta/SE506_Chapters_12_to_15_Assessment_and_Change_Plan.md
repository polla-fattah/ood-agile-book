# SE506: Chapters 12–15 assessment and change plan

**Review date:** 13 October 2026  
**Scope:** the eight supplied Markdown files: Chapters 12–15 and their code, explanation and solution companions.  
**Purpose:** specify corrections without editing the chapters or deciding module policy.

## 1. Overall judgement

**The direction is sound, and these chapters should be retained. Targeted corrections are needed before they form a consistent student release.**

The intended progression is clear: Chapter 12 measures and plans the change; Chapter 13 implements and verifies it; Chapter 14 evaluates and hands it over; Chapter 15 supplies reusable AI-assistance practices. The Book/Team distinction, offline alternatives, evidence limits and practical solutions are substantial improvements. A wholesale rewrite would lose useful work.

The most important corrections are:

1. Reconcile the Chapter 11 baseline used by Chapter 12 with the revised baseline required by Chapters 13–14.
2. Fix the HTTP client's incomplete timeout protection on Java 17.
3. Correct the visitor-decision diagram to match the actual order of checks.
4. Distinguish independently derived acceptance tests from tests withheld from an assistant.
5. Complete cumulative Java 17 verification and repair the remaining instructions and cross-references.

### Review boundary

The available blueprint is **Version 0.3, revised 12 October 2026**. The later companions say they follow **v0.4**, but that version was not supplied with these files. Alignment below is therefore against the available blueprint and the previous alignment review. The v0.4 claim needs reconciliation, not an assumption that the authors used the wrong plan.

Chapters 13–14 require Chapter 10 and Chapter 11 companions **Version 1.1**. Those exact prerequisites are not in the supplied review set. Their full 230- and 233-test projects were consequently **not reconstructed or rerun in this review**. The supplied companions' historical results remain attributed to their authors.

This review did reconstruct and run the standalone Chapter 15 lab on **OpenJDK 17.0.20 and Maven 3.9.11**, using its printed dependency versions. It also compiled the supplied Chapter 13 HTTP client unchanged and ran a focused slow-body probe. Results appear in Section 7. The full mutation experiments, hosted workflow and Mermaid rendering were not rerun.

## 2. Priority conventions

| Priority | Meaning |
|---|---|
| **P1: Fix before release** | A continuity, behaviour, teaching or reproducibility issue affects the intended learning path. |
| **P2: Fix at consolidation** | A bounded instruction, navigation or explanation correction; retain the surrounding material. |
| **Decision** | Select and record an authoritative version or teaching route. Do not invent institutional policy. |
| **Retain** | The material already serves the revised direction. |

## 3. Shared corrections

### S1. Select one cumulative baseline: P1 / Decision

This is a semantic mismatch, not merely a stale test count.

| Item | Chapter 12 supplied here | Chapters 13–14 supplied here |
|---|---|---|
| Chapter 11 checkpoint | 136 JUnit invocations | 159 invocations from revised companions |
| Suspected report defect | SD-11: due-today inclusion | SD-11-1 to SD-11-4: unknown-kind rate, grace-period inclusion, null kind and amount locale |
| Due-today result | Inclusion preserved pending a policy decision | Chapter 13 companion §12.1 says due-today loans are not listed |
| AC18 preservation target | Existing report mapping and the earlier SD-11 boundary | A late visitor's fine under the existing unknown-kind rule, SD-11-1 |

Chapter 13 companion §12.1 already identifies this mismatch accurately. An end-of-companion warning is useful, but it does not make the sequence coherent for a student reading forward.

**Required change:** confirm the authoritative Chapter 10/11 v1.1 files and distribute that exact prerequisite set. If those are the intended baseline, revise both Chapter 12 files to it. Update defect identifiers, preserved behaviour, AC18's concrete input/result and all checkpoint references. Keep the earlier 136-test run identified as historical if it remains in a verification record; do not relabel it as a 159-test run.

Add a compact checkpoint manifest listing the blueprint version, companion versions, project version and verified build command. A checksum or repository commit would make the exact source unambiguous. Explain once how the retained-reservation issue SD-12 relates to the report issues.

**Completion evidence:** a reader can assemble Chapters 10 → 11 → 13 → 14 from the delivered Markdown listings and patches, while Chapter 12 describes that same starting behaviour. No reader must resolve the merge themselves.

### S2. Verify the cumulative project on its stated runtime: P1

Chapters 13–15 honestly disclose verification on JDK 24.0.2 with `--release 17`, rather than on a Java 17 runtime. Preserve that disclosure. Compiling for Java 17 and running on Java 17 are different checks; the HTTP defect below demonstrates why the distinction matters here.

**Required change:** after S1, run the exact printed cumulative build, pipeline, demo and handover on a full Java 17 JDK, including `jdk.jdeps`. Record OS, JDK, Maven, pinned versions, commands and results. Update counts only after the new runs. Append evidence rather than rewriting the history of earlier checks.

Chapter 15 now has an independent Java 17 lab check from this review; its main results are reproducible. That does not verify the Chapter 13/14 project or every Chapter 15 mutation experiment.

A hosted GitHub Actions run remains a separately unperformed check. The available blueprint permits a local pipeline and labelled deployment simulation, so a public deployment is **not** required to close this review.

## 4. Chapter-by-chapter changes

### Chapter 12: Measuring Progress, Flow and Technical Health

**Judgement:** largely aligned; repair its connection to the revised cumulative project.

| File / location | Priority | Change to make | Completion check |
|---|---|---|---|
| `Chapter_12_Measuring_Progress_Flow_and_Technical_Health(1).md`, §§12.6–12.7 | P1 | Apply S1 to the 136-test reference, SD-11 discussion and preservation row. Identify the approved report behaviour rather than leaving a generic “retain SD-11” instruction. | The chapter agrees with the selected Chapter 11 source and Chapter 13 AC18. |
| `Chapter_12_Code_Explanations_and_Solutions(1).md`, CR-12 notes, acceptance matrix, baseline check and verification record | P1 | Reconcile the due-today statement, SD identifiers, AC18, 136-test references and preservation-record template. Give AC18 a concrete late-visitor input and expected output if the revised fine-report baseline is adopted. | AC18 can be implemented without guessing which report version is meant. |

**Retain:** the synthetic issue history, explicit metric definitions, distinction between throughput and velocity, actual repository-data exercise, cautious interpretation, change-impact plan and separation of metrics-tool checks from project-suite counts. These provide the Week 11 work requested by the available blueprint. The metrics chapter does not need to become an implementation chapter.

### Chapter 13: Integration, Delivery and Feedback

**Judgement:** strong teaching structure and useful executable boundaries; one confirmed runtime defect and one misleading diagram need correction.

| File / location | Priority | Change to make | Completion check |
|---|---|---|---|
| `Chapter_13_Code_Explanations_and_Solutions.md`, §3.12 `HttpLegacyDirectoryClient`, §4.6.1 outage tests | P1 | Bound the complete HTTP operation, including response-body receipt; add a slow-body case as well as the existing delayed-response case. See C13-1 below. | A response whose headers arrive promptly but whose body stalls fails within the chosen overall budget. |
| `Chapter_13_Integration_Delivery_and_Feedback.md`, Figure 13.3 / §13.7 | P1 | Correct the order of visitor checks. The diagram currently puts count and 1–3-day validation before the approval read; the implementation generally does the approval read first. See C13-2 below. | Trace the figure against four-day, count-limit and unavailable-register examples. |
| Both files, entry checkpoint / companion §§1 and 12.1 | P1 | Apply S1 and make the exact v1.1 prerequisites available. Replace the unresolved alignment warning with the final resolution once completed. | Fresh reconstruction succeeds from the released prerequisite set. |
| Companion §§5.3 and 7.7, simulated release | P2 | State explicitly that delivery assumes a successful gate run for the same candidate: the script packages with `-DskipTests` and then runs E2E smoke tests. State that rollback currently assumes the same version-derived jar filename. | A learner does not mistake the script for enforcement of every pipeline gate, or the same-build exercise for tested cross-version rollback. |

#### C13-1. Confirmed timeout defect

The client calls synchronous `HttpClient.send` with `BodyHandlers.ofString` and an `HttpRequest` timeout. The existing `SLOW` stub waits **before sending response headers**, so it exercises only that scenario.

For this review, the unchanged client was given a **300 ms** request timeout. A local server sent HTTP 200 headers and the first body byte promptly, then waited **1,600 ms** before completing the valid `S\tY` response. On OpenJDK 17.0.20 the lookup **succeeded after approximately 1,690 ms**:

```text
RESULT=Person[key=B1, kind=S, status=Y]
ELAPSED_MS=1690
```

This contradicts the chapter's general “one attempt, a bounded wait” guarantee. A check against a newer JDK does not settle Java 17 behaviour.

**Fix:** introduce an overall completion deadline that includes reading the body. One possible implementation route is a timed wait on the asynchronous operation, with explicit cancellation and correct interruption/error translation; whichever approach is chosen must be verified on Java 17. Preserve the existing distinction between unavailable and not-found, one logical lookup attempt, and no reservation/notice after failure.

Add a deterministic stub scenario that flushes headers and a partial body, then holds the remainder. Release/close it in cleanup. Assert the timeout outcome as well as a generous outer test deadline. Merely checking that a successful result arrives in less than five seconds would miss the reproduced defect.

Update the main chapter's boundary discussion and Chapter 14's known-issues/evidence records after the fix. Do not add retries or fallback categories to solve a timeout.

#### C13-2. Diagram and code disagree about decision order

The actual path is: directory lookup; for a visitor, flag and item checks; if `days < 1`, leave duration rejection to the coordinator; otherwise read the clock, read and validate approval; then call the coordinator, which applies count/duration and availability rules.

Therefore, a four-day visitor request can encounter an unavailable approval register before the duration rule rejects it. Figure 13.3 currently shows the opposite.

**Preferred small correction:** keep the current responsibility split and revise the Mermaid diagram to represent the real gate/coordinator sequence, including the nonpositive-duration branch. Explain that rejection precedence is observable when more than one condition is wrong. If a different precedence is required, change the contract, implementation and tests together rather than changing the picture alone.

**Retain:** real temporary-file tests, the local HTTP service, contract tests with explicitly limited scope, separate-process journeys, failure-versus-rejection distinction, one default-off flag, rollback limitations and clearly labelled deployment simulation.

### Chapter 14: Responding to Change and Handing Over

**Judgement:** well aligned with the handover goal; retain the chapter and correct inherited evidence plus navigation.

| File / location | Priority | Change to make | Completion check |
|---|---|---|---|
| Both Chapter 14 files; handover and known-issues listings | P1 | Apply S1/S2 and carry forward the timeout correction. The unchanged production-code claim remains valid only relative to the final, corrected Chapter 13 checkpoint. | The released Chapter 14 project inherits the corrected client and its tests; evidence tables and counts match the new run. |
| `Chapter_14_Responding_to_Change_and_Handing_Over.md`, §14.1 assumptions; companion §5.3 | P2 | Replace “the directory cannot fail” as the earlier assumption. Chapter 8 already defines provider `Failure`, translates it to `DirectoryException` and distinguishes outage from absence. Say Chapter 13 adds real HTTP transport and observed timeout/failure cases. | The retrospective describes the actual evolution without erasing earlier failure handling. |
| Main chapter and companion cross-references | P2 | Repair the references listed below, then check the remaining companion section links. | Each reference lands on the promised evidence. |
| Main §14.1 small-diff example and companion §5.2 E3 | P2 | Explain that the passing unit stage exposes a missing direct visitor-code mapping case in this suite. A focused adapter unit test could catch `V → STAFF`; network integration is not intrinsically required to discover that mapping defect. | The lesson distinguishes this suite's coverage gap from a limitation of unit testing itself. |

**Confirmed navigation corrections:**

| Current reference | Correct destination |
|---|---|
| Main §14.1, one-line mapping experiment: companion §7.2 | Companion §5.2, experiment E3 |
| Main §14.3, traceability fault experiment: companion §12.3 | Companion §10.3 |
| Companion §1, unchanged production-code verification: §12.2 | §10.2 |
| Companion §5.2, verification configuration: §12.2 | §10.2 |
| Companion §6.1 B4 and §8, fault experiments: §12.3 | §10.3 |
| Companion §10.1, Chapter 13 alignment discussion: Chapter 13 companion §10.1 | Chapter 13 companion §12.1 |

**Retain:** the requirements-to-evidence table, explicit limits of its structural checker, fresh-copy handover exercise, decisions on known issues, bounded flag-removal rehearsal, separate individual reflection and qualitative contribution evidence. The incomplete documentation after the optional removal patch is already disclosed and used as an exercise; it is not an undisclosed defect in the released checkpoint.

### Chapter 15: AI as a Software Engineering Assistant

**Judgement:** the standalone lab works as intended on Java 17. Correct the central explanation of test independence and several bounded instructions.

| File / location | Priority | Change to make | Completion check |
|---|---|---|---|
| `Chapter_15_AI_as_a_Software_Engineering_Assistant.md`, §15.2 and Figure 15.1 caption; companion §§6.2, 6.4 and 7.3 | P1 | Distinguish independent derivation of an expected result from keeping a test hidden. Sharing human-reviewed examples does not remove their value as requirement-based acceptance tests. See proposed wording below. | No model answer marks an otherwise sound process weak solely because acceptance examples were shared. |
| Main §15.4; companion §§1.3, 9.1 and 10.1 | P2 | Make the plain-`javac` comparison conditional on a newer installed JDK. Under Java 17 both plain compilation and `--release 17` reject `getFirst()`; the advertised one-error/two-error contrast requires Java 21 or later for the unrestricted compile. | The Java 17-only learner gets the expected result without installing another JDK; the newer-JDK comparison is optional. |
| Companion §3.7 `check-record.sh` | P2 | Fail clearly, or report an explicit “no records to check” result, when only the template exists. It currently exits 0 with `RECORD CHECK PASSED` without checking any record. | Template-only and zero-record fixtures cannot be reported as successful record verification. |
| Main §15.7 and common-mistakes table | P2 | Scope “a prompt leaves your machine” to remotely hosted tools. Locally executed tools may keep processing local; students should check the actual deployment and policy. Preserve the minimal-context and synthetic-data guidance. | The statement remains vendor-neutral and accurate for both local and remote tools. |
| Main reading route / §15.11 | P2 / Decision | Explain when the “minimum required” B1–B4 and T1–T3 work is used across the existing weeks. This is a reference chapter with no separate teaching week or assessed AI outcome. | The route consolidates existing activities without silently adding a new assessed submission. |
| Main Figure 15.1 | P2 | Change the six-step left-to-right Mermaid layout to a compact top-down layout, retaining the feedback loop. | Readable at normal document width; no ASCII replacement or unnecessary new diagram. |
| Companion §10.2 | P2 | Append the independent Java 17 results from Section 7 with their scope. Retain the historical JDK 24 record and its date. | New evidence is distinguished from the original verification and from unrerun mutation experiments. |

**Suggested replacement for the acceptance-example advice:**

> Derive acceptance examples from the requirement before reviewing the candidate implementation. You may share reviewed examples to clarify the task. They remain useful acceptance checks, but a pass on examples the assistant has seen does not demonstrate behaviour beyond those examples. Add independently derived boundary cases or properties, and keep selected cases undisclosed when evaluating generalisation. Avoid deriving both expected results and implementation from the same unexamined assumption.

**Retain:** visible rejected attempts, the invented-method and newer-API example, the off-by-one fault, the distinction between generated tests and requirement-derived examples, explicit constructed-output provenance, the compact assistance record, offline routes and deference to the module leader's assessment rules.

## 5. Blueprint alignment summary

| Blueprint requirement | Assessment |
|---|---|
| Change introduced in Week 11, implemented in Week 12, evaluated in Week 13 | Correct sequence; reconcile the underlying checkpoint. |
| Repository-metrics exercise using real data as well as synthetic teaching data | Present in Chapter 12; retain. |
| Genuine integration boundary, contracts, feature flag and modest pipeline | Present in Chapter 13; repair timeout protection and the decision-order diagram. |
| Labelled simulation; public deployment not required | Correctly handled. |
| Reproducible handover and qualitative contribution evidence | Strong Chapter 14 coverage; complete target-runtime evidence and fix cross-references. |
| AI assistance distinguished from an AI/data component inside the application | Explicitly addressed. The directory illustrates a data-component boundary; do not imply the project trains or evaluates an ML model. |
| Vendor-neutral reference chapter, offline alternative and no invented assessment policy | Substantially satisfied; clarify Chapter 15's scheduling and test-independence advice. |
| Revised blueprint version | v0.4 not supplied; final sign-off against that version remains open. |

No module-description edits, new assessment weights or institutional AI permissions are proposed.

## 6. Recommended editing order

1. Confirm and supply the authoritative blueprint and Chapter 10/11 v1.1 prerequisites.
2. Reconcile Chapter 12's baseline and acceptance example AC18.
3. Fix and test Chapter 13's complete-response timeout; correct Figure 13.3.
4. Carry the corrected checkpoint into Chapter 14 and refresh its actual build/handover evidence.
5. Correct Chapter 15's independence explanation, runtime-specific compiler instructions and empty-record check.
6. Repair cross-references, append verification records and check the final reading routes and Mermaid layouts.

These changes belong in the existing two-file chapter format. A separate companion application, production deployment platform or additional diagram collection is unnecessary.

## 7. Execution evidence from this review

The Chapter 15 files were extracted from the supplied fenced listings. Maven 3.9.11 was invoked through an environment-specific proxy-settings wrapper; the lab's POM, pinned dependency versions and Java source were unchanged. The runtime was OpenJDK 17.0.20.

| Check run during this review | Observed result |
|---|---|
| Accepted Chapter 15 lab, `mvn --batch-mode test` | **Pass:** 9 tests; zero failures, errors or skips. |
| `try-attempt.sh 1` | **Expected compile failure:** two unresolved symbols. |
| `try-attempt.sh 2 generated` | **Pass:** all 7 generated tests. |
| `try-attempt.sh 2` | **Expected compile failure:** ambiguous `AvailabilityFinder(null)` constructor call. |
| `try-attempt.sh 2 adapted` | **Expected failure:** 9 tests run, 2 failures, matching the window-boundary teaching example. |
| `check-record.sh` with the supplied filled record | **Pass:** record checked. |
| `check-record.sh` in a fresh copy containing only the template | **Defect reproduced:** exit 0, `RECORD CHECK PASSED`, no record checked. |
| Unchanged Chapter 13 HTTP client; 300 ms timeout; partial response held for 1,600 ms | **Defect reproduced:** valid result returned after approximately 1,690 ms. |

**Not established by these runs:** the full cumulative Chapter 13/14 results, all mutation scores, hosted CI, real institutional services, concurrency, or the suitability of any assessment policy. Successful lab reproduction does not certify every statement in a chapter.

### Source basis

The principal evidence is the eight supplied chapter files, the available blueprint v0.3 and the previous `SE506_Blueprint_Alignment_Review_and_Chapter_Change_Plan.md`. Chapter 8's supplied companion was checked for the earlier provider-failure contract.

Official technical references consulted on 13 October 2026:

- [Java SE 17: HttpRequest.Builder.timeout](https://docs.oracle.com/en/java/javase/17/docs/api/java.net.http/java/net/http/HttpRequest.Builder.html#timeout(java.time.Duration)). The timeout finding above rests on the reproduced Java 17 behaviour, not an assumption that the brief API description proves complete-body coverage.
- [actions/checkout releases](https://github.com/actions/checkout/releases) and [actions/upload-artifact releases](https://github.com/actions/upload-artifact/releases). The printed `v7` major versions exist; they were not treated as invented dependencies. Existence of the actions does not establish that the supplied hosted workflow has run.

## 8. Release checklist

- [ ] One authoritative blueprint and prerequisite checkpoint set is identified and supplied.
- [ ] Chapter 12's report behaviour, defect identifiers and AC18 agree with that set.
- [ ] The HTTP slow-body case fails safely within the overall timeout on Java 17.
- [ ] The visitor-decision Mermaid diagram matches the implementation.
- [ ] Chapter 13/14 builds, stages, demo and handover are verified on the stated runtime.
- [ ] Chapter 15 separates requirement-derived tests from withheld evaluation cases.
- [ ] Compiler instructions work as stated on a Java 17-only setup.
- [ ] An empty assistance-record set cannot be reported as verified.
- [ ] Cross-references, evidence counts and reading routes are reconciled.

