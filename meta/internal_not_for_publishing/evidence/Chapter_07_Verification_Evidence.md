# Chapter 7: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_07_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3

---

## From `Chapter_07_Code_Explanations_and_Solutions.md`: Line 9 (verification evidence wording)

model solutions and observed verification evidence.

---

## From `Chapter_07_Code_Explanations_and_Solutions.md`: Tool table row (author runtime)

| Java | Java 17 language/API target; author runtime OpenJDK 17.0.20 | Application and test execution |

---

## From `Chapter_07_Code_Explanations_and_Solutions.md`: Mockito agent warning paragraph (JDK 24 and Mockito 5.23.0 specifics, and the note that JDK 17 was not available)

The resource does not stop Mockito from loading its ByteBuddy agent. On JDK 24 with Mockito 5.23.0, the log showed `WARNING: A Java agent has been loaded dynamically`, with and without the resource, and the tests passed. Passing `-XX:+EnableDynamicAgentLoading` to the test JVM (Surefire's `argLine`) removed the warning. The JVM states that dynamic agent loading will be disallowed by default in a future release, so check the Mockito documentation for the setup recommended for the JDK you use. This behaviour was not observed on JDK 17, which was not available for this review, or with the pinned Mockito 5.20.0, which was not downloaded.

---

## From `Chapter_07_Code_Explanations_and_Solutions.md`: Section 6.1 lead-in (counting history removed; totals made consistent with the final tests)

Sixteen single faults were introduced one at a time into copies of the completed project, and each copy was run through `mvn test`. Fourteen were rejected by at least one named test, and the table below lists exactly those fourteen. The two that were not rejected follow it. (Version 1.1 of this file said fifteen and thirteen; the table has always held fourteen caught rows plus two survivors, so the earlier totals were a counting error.)

---

## From `Chapter_07_Code_Explanations_and_Solutions.md`: Section 6.1 'Two faults survived the version 1.0 tests'

Two faults survived the version 1.0 tests.

---

## From `Chapter_07_Code_Explanations_and_Solutions.md`: Section 6.1, loans snapshot paragraph (version 1.1 history removed)

**The `loans()` snapshot could be modified.** Replacing `List.copyOf(loans.values())` with a plain `ArrayList` passed everything, although the chapter's rule table says loan snapshots are unmodifiable. Version 1.1 adds one assertion to `checkoutAndReturnUseTheSuppliedClock`, and the fault is now caught. The invocation count stays at 35.

---

## From `Chapter_07_Code_Explanations_and_Solutions.md`: Section 6.1, add-then-remove paragraph ('still survives' reworded)

**An enquiry that adds a temporary record and removes it again.** This one still survives, and it is a good teaching case. With identifiers derived from the list size, a record added and then removed leaves no trace: the records, notices and next identifier all end up exactly as before. In a sequential program, no test can tell this implementation from the correct one. It would matter only if something could observe the list between the add and the remove, such as a concurrent caller. The right response is to reject the design by reading it, as the AI activity does, and to avoid claiming that a test can catch it. The identifier example is still worth keeping, because it protects the promise if identifiers ever come from a separate counter.

---

## From `Chapter_07_Code_Explanations_and_Solutions.md`: Section 12 Verification record (versions, cached-versions run, exact-configuration run, results tables)

## 12. Verification record

**Version 1.0 (12 October 2026)** was run on OpenJDK 17.0.20 with Maven 3.9.11 and the exact POM versions above. That run was not repeated. The author's network then required runtime-specific Maven proxy settings, which are not part of the learner project, and a dependency-resolution problem during setup was corrected before the behavioural TDD observation; it is not counted as the red stage.

**Version 1.1 (13 October 2026)** was re-verified offline on Windows 11 with **Maven 3.9.16, JDK 24.0.2** (compiling with `--release 17`), and the dependency versions already present in the local Maven cache. **The pinned versions in the POM were not run in this first pass of version 1.1**: JUnit Jupiter 5.13.4, Mockito 5.20.0, Compiler Plugin 3.14.1 and Surefire 3.5.4 were not in the cache, and nothing had been downloaded. The copy used for that build differed from the POM in this file only in these versions:

| Component | POM in this file | Version used in the 1.1 run |
|---|---|---|
| Maven | 3.9.11 | 3.9.16 |
| JUnit Jupiter | 5.13.4 | 6.0.3 |
| Mockito | 5.20.0 | 5.23.0 (with ByteBuddy 1.18.11, the cached version) |
| Compiler Plugin | 3.14.1 | 3.15.0 |
| Surefire Plugin | 3.5.4 | 3.5.6 |
| Resources and JAR plugins (not pinned in this file) | Maven defaults | 3.5.0 and 3.5.1 |

All 36 listings (34 project files and the two stage snapshots of Section 5) were extracted programmatically from this file, so the sources that ran are the sources printed here. The results below therefore verify the code, the tests and the configuration files, and the first pass did not verify the exact pinned versions.

**Exact-configuration run (13 October 2026).** The unmodified POM from this file was run with **Maven 3.9.11** (downloaded from Maven Central and checked against its published SHA-512) on **JDK 24.0.2** (`--release 17`), against a clean local repository, so that nothing already cached could stand in for a pinned version. The versions that ran were JUnit Jupiter 5.13.4, Mockito 5.20.0 (which brought ByteBuddy 1.17.7), Compiler Plugin 3.14.1 and Surefire 3.5.4, plus the plugins that Maven 3.9.11 binds by default (Resources 3.3.1 and JAR 3.4.1). `mvn verify` exited 0 with 35 tests and no failures. The recorded cycle was replayed on the exact pins: the red snapshot gave one test run and one behavioural failure (the assertion “An overlapping item must be unavailable”, not a compilation error), the green snapshot passed that test, and the final coordinator passed the five-case refactor run. The wrong-boundary experiment of Section 6 failed one test with `expected: <true> but was: <false>` and passed again after restoring `LoanPeriod`. The dynamic-agent warning described in Section 7.5 of the chapter also appears with the pinned Mockito 5.20.0 on JDK 24; passing `-DargLine=-XX:+EnableDynamicAgentLoading` removed it (three Mockito tests passed). **Still not verified:** behaviour on a Java 17 runtime (no JDK 17 was available) and a hosted CI run. The fault experiments in this file were run in the earlier pass and were not repeated under the exact configuration.

| Stage | Observed result |
|---|---|
| Availability red | 1 test; 1 assertion failure; 0 errors; nonzero exit |
| Availability green | Same test; 0 failures; exit 0 |
| Refactor plus legacy bridge | 5 JUnit cases; 0 failures; exit 0 |
| Completed Maven verify | 35 invocations; 0 failures; 0 errors; 0 skipped; exit 0 |
| Legacy checks inside the bridge | Earlier 34 checks, five groups, 44 checks and 28 checks passed |
| Mockito examples | All three passed with interface proxy configuration |
| Loan tests | Nine invocations passed with controlled time |
| Deliberate inclusive-boundary mutation | Selected adjacency test failed: expected true, actual false |
| Restored boundary | Selected adjacency test passed again |
| MVP demonstration | Query/reserve/checkout/return output matched the documented transcript |
| Reconstruction from this Markdown file | All 35 file listings matched their source; the reconstructed project passed 35 JUnit invocations and reproduced the demonstration transcript |
| Hosted CI and independent peer review | Not performed or claimed in this author verification |

**Version 1.1 observations (cached versions, offline).**

| Observation | Result |
|---|---|
| `mvn -o verify` | Exit 0; 35 tests (1 TDD, 8 availability, 10 policy rows, 4 legacy bridges, 9 loan, 3 Mockito), 0 failures, 0 errors |
| TDD red (red snapshot, `-Dtest=AvailabilityTddTest`) | 1 test, 1 failure, 0 errors, exit 1; the assertion message was `An overlapping item must be unavailable ==> expected: <false> but was: <true>` |
| TDD green (green snapshot) | Same test passes, exit 0 |
| Refactor (final coordinator, TDD test plus legacy bridge) | 5 tests, 0 failures, exit 0 |
| Differences between the green snapshot and the final coordinator | Only the extracted `hasConflict` helper and its two callers, as the chapter says |
| Fault experiment | 16 faults introduced one at a time; 14 caught, 2 survived in the version 1.0 tests (Section 6.1). The `loans()` snapshot gap is closed in 1.1; the add-then-remove shortcut is behaviourally invisible |
| `javac -Xlint:all` on the main sources | Version 1.0's embedded `NotificationException` gave one `[serial]` warning; fixed in 1.1 by refreshing it from Chapter 6, and the main sources are now warning-free |
| Mockito mock maker | With the `mock-maker-proxy` resource the mock was a JDK dynamic proxy; Mockito still loaded its ByteBuddy agent and the JVM printed a dynamic-agent warning, with or without the resource. `-DargLine=-XX:+EnableDynamicAgentLoading` removed the warning and the tests passed |
| Embedded copies | Version 1.0 carried Chapter 6's earlier 26-check runner, `NotificationException` without `serialVersionUID`, and Chapter 3's earlier narrower AC-03. Version 1.1 refreshes all three from the Chapter 6 version 1.1 files, and adds `.gitattributes` |
| Midterm practice solution (Section 11.5) | Built in a scratch Maven project: 3 tests, 0 failures. Four faults (inclusive due date, system clock instead of the supplied one, wrong subject, no send) were each rejected. The original class, run directly, returned `false` for a future due date and failed with `IllegalStateException` on the overdue path |

---

## From `Chapter_07_Testing_as_a_Design_Practice.md`: Manuscript, practical warning about the Mockito agent (JDK 24.0.2 and version comparison removed)

One practical warning. On newer JDKs, Mockito may still attach its ByteBuddy agent when it starts, and the JVM then prints “A Java agent has been loaded dynamically”. On JDK 24.0.2 this appeared with the Mockito 5.20.0 printed in the companion POM and also with the newer 5.23.0, even with the proxy setting, and the tests still passed; with 5.20.0, passing `-XX:+EnableDynamicAgentLoading` to the test JVM removed the message. Other JDK and Mockito combinations may behave differently. The JVM states that dynamic loading will be disallowed by default in a future release, so check Mockito's documentation for the setup recommended for your JDK.

---

## From `Chapter_07_Testing_as_a_Design_Practice.md`: Manuscript, source note

not a claim to use every tool's newest release; the companion records which versions were actually run.

---

## From `Chapter_07_Testing_as_a_Design_Practice.md`: Manuscript line 422, Blueprint D4 reference

 (Blueprint D4);

---

