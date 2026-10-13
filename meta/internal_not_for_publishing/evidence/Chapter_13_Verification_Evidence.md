# Chapter 13: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_13_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1, first paragraph

model solutions and the verification record.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1, Version note (independent review, version 1.1)

**Version note.** Version 1.1 corrects three things found by an independent review of Chapters 12 to 15. (1) The HTTP client's timeout bounded the wait for the response headers and not the whole answer; the client now has a deadline on the whole lookup, and a new stub scenario and test cover a stalled body (Section 7.8). (2) Figure 13.3 showed the count and duration rules before the register was read; the figure now follows the code, and a test pins the order (Section 7.9). (3) Two statements about the simulated release are now explicit. The project version is 0.13.1 and the build runs 232 invocations (it was 0.13.0 and 230). The files that changed are `HttpLegacyDirectoryClient.java`, `DirectoryStub.java`, `DirectoryOutageIntegrationTest.java`, `VisitorAcceptanceTest.java`, `simulate-release.sh`, `ADR-013`, `README.md` and `pom.xml`. The results of Version 1.0 are not rewritten: the 27-fault experiment and the 230-invocation runs are recorded below as the earlier results.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1, input checkpoint (versions and invocation count removed)

**Input checkpoint.** The starting point is the Chapter 11 checkpoint: the Chapter 10 companion (Version 1.1) plus the new and changed files of the Chapter 11 companion (Version 1.1), which together give 159 JUnit invocations. To keep verified listings from being copied a third time, this file lists **only the files that are new or changed**. Every other file is exactly as in those two companions. Chapter 12 changes no code: its companion is not part of the checkpoint.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1, 'Boundary decision (Blueprint D1, interim)' paragraph

**Boundary decision (Blueprint D1, interim).** The chapter's two real boundaries are a local file and a local HTTP stub service built on the JDK. The module leader has not yet decided D1; if a different boundary is chosen later (an embedded database, for example), the policy table of Section 2.3 and the tests stay, and the adapters change.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1.0, Checkpoint manifest (SHA-256 of the prerequisite companions)

### 1.0 Checkpoint manifest

| Item | Value |
|---|---|
| Blueprint | Version 0.4 (the companions say they follow it) |
| Prerequisite 1 | `Chapter_10_Code_Explanations_and_Solutions.md`, Version 1.1, SHA-256 `fc3f7e8aa803a4f65fa5740084291759cff6700401f0c7870ac1e9e478c4ea9e` |
| Prerequisite 2 | `Chapter_11_Code_Explanations_and_Solutions.md`, Version 1.1, SHA-256 `96ee7dc6e8967dd2d669ee0317d8f42309dad254f23069b9da2379332b11cce3` |
| This companion | Version 1.1; project version 0.13.1 |
| Verified build | `mvn --batch-mode verify`: 232 invocations (203 unit, 26 integration, 3 end-to-end), JDK 24.0.2 with `--release 17`, Maven 3.9.11 |

The checksums identify the exact prerequisite files used on 13 October 2026. If either prerequisite is edited later, the checksum above must be refreshed and the reconstruction repeated.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1.1, step 1

Save every listing of the Chapter 10 companion (Version 1.1) at its path.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1.1, step 2

Save the new and changed listings of the Chapter 11 companion (Version 1.1, its Sections 3 to 6) at their paths.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1.1, project version sentence

Surefire 3.5.4); only the project version becomes 0.13.0. Initial builds

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Project README listing, stale project version

Existing dependency and plugin versions are unchanged; only the project version becomes 0.13.0.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1.2, lead-in to the pipeline output

On the verification machine (Section 12.2) the passing run was:

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1.3, reference to Section 12.2

 because the POM sets `failIfNoTests` to true (Section 12.2).

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 1.4, reference to Section 12.2

 Section 12.2 records the result.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: B3, count of faults

Section 12.2 lists twenty-seven faults and the tests that caught them;

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 9, reference to the exact configuration

each applied to its own scratch copy of the final code, on the exact configuration of Section 12.2.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: ADR-013 listing, date and status lines

Date: 13 October 2026 (Asia/Baghdad)
Status: Implemented teaching example; peer review pending. The integration boundary (Blueprint D1) is an interim choice awaiting the module leader.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 7.8 heading

### 7.8 The timeout defect, found in review

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 7.8, first paragraph (Version 1.0 client)

The client of Version 1.0 called the blocking `send` with a request timeout. The JDK documents that timeout as the time within which the response must be *received* and says nothing about a body [8]. The only test of a slow provider used a stub that waits before sending anything, so it exercised the one case the timeout certainly covers.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 7.8, second paragraph (review, OpenJDK 17.0.20 and JDK 24.0.2 measurements)

A review of the chapter tried another: a server that sends the headers and the first byte at once and holds the rest. With the client's timeout at 300 ms and the server holding the body for 1,600 ms, the lookup returned a valid result. The review measured about 1,690 ms on OpenJDK 17.0.20. The same probe on the verification machine (JDK 24.0.2, Version 1.0 client) gave `RESULT=Person[key=B1, kind=S, status=Y]` and `ELAPSED_MS=1725`. I did not run the probe on a Java 17 runtime; the Java 17 figure is the review's.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 7.8, fix paragraph (wording 'the correction')

The correction sends the request asynchronously and waits for the future for at most the configured time. On timeout it cancels the future, which asks the client to drop the exchange and is not guaranteed to be prompt or to take effect [13][14], and fails the lookup with a message that names the wait. The caller does not depend on the cancellation, because it has already stopped waiting. An interrupted wait cancels, restores the interrupt flag and fails. A failed future becomes a `Failure` whose message names the cause's class. The header timeout stays on the request.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 7.8 table, first row

| New test `aStalledBodyIsAFailureWithinTheOverallWait` against the **Version 1.0 client** | Fails: `execution timed out after 5000 ms` (the outer deadline), because the client waits for the stub to release the body and returns it |

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 7.8 table, second row (exact figures and JDK removed)

| The same test against the corrected client | Passes. A probe with the same 300 ms timeout and 1,600 ms stall: `FAILED=...Failure: Directory did not answer within 300 ms.` after 326 ms |

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 7.9, first paragraph (statement about Figure 13.3 of Version 1.0)

Figure 13.3 of Version 1.0 put the count and duration rules before the register was read. The code does the opposite: the gate checks the flag, the item, and (for fewer than one day) steps aside; otherwise it reads the clock and the register; then the coordinator applies the count and duration rules and the availability rule. A four-day visitor request with an unreadable register therefore fails with the register's error and is not rejected for its duration. The test `precedence_theRegisterIsReadBeforeTheCountAndDurationRulesApply` pins both ends: four days with an unreadable register throws the register's exception, and zero days does not read the register and returns the limit rejection. It is not one of the eighteen acceptance examples and is not named `ac<N>_`.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 12.1, 'Alignment with Chapter 12' paragraph

**Alignment with Chapter 12.** Chapter 12 was written separately. Its text refers to a “136-test Chapter 11 suite”, and its acceptance matrix refers to “SD-11 status”; the Chapter 11 companion that this chapter builds on has 159 invocations and four numbered suspected defects (SD-11-1 to SD-11-4), and SD-11-1, the rate for any other kind of borrower, is the one that AC18 now reaches. Its line “SD-11: due-today inclusion preserved; policy unresolved” and its remark that the refactoring removed a duplicated selection rule describe the earlier draft of Chapter 11. In the Chapter 11 of this series a loan due today is *not* listed, and the four suspected defects are about other kinds of borrower (SD-11-1), a loan listed within its grace period (SD-11-2), a null kind (SD-11-3) and the locale of amounts (SD-11-4). These statements need to be reconciled by whoever owns Chapter 12 and the Chapter 11 merge. CR-12 itself, its eighteen acceptance examples and its backlog were used as written, and each example has a test (Section 7.3).

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 12.2, Verification record (environment, reconstruction, results table, timeout probe)

### 12.2 Verification record

This version was verified offline on Windows 11 with **Maven 3.9.11 and JDK 24.0.2**, compiling with `--release 17`, against the **pinned versions** (JUnit Jupiter 5.13.4, Mockito 5.20.0 with ByteBuddy 1.17.7, Compiler Plugin 3.14.1, Surefire 3.5.4, Resources 3.3.1, JAR 3.4.1) in a clean local repository. No JDK 17 was available, and no hosted CI run was made. The listings were extracted from the build that ran.

**Reconstruction.** The listings of the Chapter 10 companion (64), the Chapter 11 companion (26) and this file (31, with four hunks applied by `patch -p1`) were extracted programmatically into a fresh directory, in that order, so that later files replace earlier ones. The result matched the working project file for file (byte for byte), except that the reconstruction also contains the `stages/` directory of the Chapter 11 companion, which is not compiled. `mvn --batch-mode verify` on that reconstruction exited 0 with 232 invocations, no failures, errors or skipped tests, and `bash scripts/pipeline.sh` on it passed all five stages (203, 26 and 3 invocations in stages 2, 3 and 4). This is the reconstruction of Version 1.1; the one of Version 1.0 ran 230 invocations.


| Check | Observed result |
|---|---|
| Full Maven verify | Exit 0; 232 invocations, 0 failures, errors or skipped (159 inherited and 73 new). Version 1.0 ran 230 |
| The pipeline | Exit 0: 203, 26 and 3 invocations in stages 2, 3 and 4; `PIPELINE PASSED` (Version 1.0: 202, 25 and 3) |
| A failing pipeline | Exit 1 with the header check removed: stages 1 and 2 pass; stage 3 fails at `aWrongOrMissingHeaderIsAFailure`; stages 4 and 5 do not start (Section 7.6) |
| A stage that selects nothing | `mvn test -Dgroups=nosuchtag` ends with `No tests were executed!` and `BUILD FAILURE` |
| Command-line tag selection | `-DexcludedGroups=integration,e2e`, `-Dgroups=integration` and `-Dgroups=e2e` selected the 203, 26 and 3 invocations above. The Surefire page documents the parameters in the POM; the command-line form was exercised by running it |
| Timeout probe | Version 1.0 client: 1,725 ms and a result (JDK 24.0.2); corrected client: failure after 326 ms. The review's Java 17 figure (about 1,690 ms) is reported by the review and was not reproduced here |
| Simulated delivery | v1 delivered and smoke-tested (3 journeys passed); v2 delivered and smoke-tested; rollback made v1 current again and smoke-tested it; afterwards `build/staging` held only `current` |
| `javac --release 17 -Xlint:all` | No warnings on the main sources (direct `javac`); the test sources and the two AI files compiled through Maven with the same flag and reported none |
| AI fixture | Baseline: both tests pass. Fault A and fault B: the proposed test passes and the repaired one fails (Section 9) |
| Mockito agent warning | The dynamic-agent warning described in Chapter 7 also appeared on JDK 24; the tests passed |
| Hosted CI, Java 17, real directory, peer review | Not performed or claimed |

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 12.2 lead-in (exact configuration, 232 and the Version 1.0 comparison)

through `mvn test` under the exact configuration, against the final suite of 232 invocations. **Twenty-nine were caught. One survived, and it is an equivalent change** (below). Version 1.0 ran twenty-seven faults against 230 invocations and caught all of them; the HTTP rows have changed because the client changed. The harness reports

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 12.2, note on two mutants that did not compile at first

Two of the HTTP mutants did not compile at first (a `get()` without a timeout makes the `TimeoutException` handler unreachable) and were rerun as `get(Long.MAX_VALUE, ...)`, which is the same fault expressed so that the code still compiles.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Section 12.2, closing paragraph (Version 1.0 wording)

The experiment of Version 1.0 **could not have found** the defect of Section 7.8, because none of its faults concerned the body of the response. A fault experiment finds

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Manuscript line 38

the model answers and the verification record.

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Manuscript source note

were opened on 13 October 2026; the manuscript was written the same day, Asia/Baghdad.

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Manuscript, entry checkpoint (159 invocations)

the Chapter 11 project (159 JUnit invocations) and Chapter 12's

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Manuscript, entry checkpoint (232 invocations)

 The completed checkpoint has 232 invocations. The Chapter 11 listings are not repeated:

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Manuscript 13.2, paragraph about the earlier client, the review, and the JDK 24.0.2 and OpenJDK 17.0.20 figures

An earlier version of this chapter's client relied on that timeout alone and its test used a stub that waits **before** sending anything. That test passed, and it was the only case anyone had thought of. A review of the chapter then ran a different one: a server that sends the headers and the first byte of the body at once, and then holds the rest for 1,600 milliseconds, with the client's timeout set to 300. The lookup **succeeded after about 1,700 milliseconds** (1,725 on JDK 24.0.2 here, and about 1,690 on OpenJDK 17.0.20 in the review). The policy said “a bounded wait” and the client did not keep it, because the timeout bounded the wait for the headers and not the whole answer.

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Manuscript 13.2, fix paragraph (wording 'The client now sends')

The fix is a deadline on the whole lookup. The client now sends the request asynchronously and waits for the result for at most the configured time; if the time runs out it asks the client to drop the exchange and fails the lookup. Asking is all it can do: the documentation says that cancelling the future attempts to cancel the exchange and that the cancellation is not guaranteed to be prompt or to take effect at all [13][14]. The caller does not depend on it, because the caller has already stopped waiting. The header timeout stays as well. Removing the overall deadline is caught by the new test. Removing the header timeout alone cannot be detected by any test, because the overall deadline still bounds the call: the fault experiment records it as an equivalent change.

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Manuscript 13.2, SLOWBODY paragraph ('old client', 'corrected client', 'a review that tries a different one')

A new stub scenario, `SLOWBODY`, sends the headers and the first byte and then holds the rest until the stub is closed. The new test asserts the **outcome**, a failure and not a result, and runs it with a generous outer deadline so that a defect shows as a failed test and not as a hang. Run against the old client, that test failed with `execution timed out after 5000 ms`. Against the corrected client the lookup fails after about 330 milliseconds. The lesson is wider than HTTP: a test of a failure path covers the failure you imagined, and a review that tries a different one is evidence you cannot produce alone.

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Manuscript 13.7, counts 159 and 232

The 159 invocations of the Chapter 11 checkpoint passed unchanged after that edit, and the new tests bring the total to 232.

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Source note ('not opened' wording)

Not re-opened for this chapter; the features were exercised by the project's own build.

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Source note ('not opened' wording)

Not opened for this chapter; publication details come from the module descriptor.

---

## From `Chapter_13_Integration_Delivery_and_Feedback.md`: Source note ('not opened' wording)

The module's recommended reading for Week 12 (selected chapters). Not opened.

---

## From `Chapter_13_Code_Explanations_and_Solutions.md`: Source note ('not opened' wording)

 Sources 10–12 are not re-opened here.

---

