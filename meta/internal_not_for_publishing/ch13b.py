from cleanup_lib import *
C = "Chapter_13_Code_Explanations_and_Solutions.md"
M = "Chapter_13_Integration_Delivery_and_Feedback.md"

replace_once(C, "Surefire 3.5.4); only the project version becomes 0.13.0. Initial builds", "Surefire 3.5.4); only the project version changes. Initial builds", 13, "Section 1.1, project version sentence", evidence=True)
replace_once(C, "Existing dependency and plugin versions are unchanged; only the project version becomes 0.13.0.", "Existing dependency and plugin versions are unchanged; only the project version changes (to 0.13.1).", 13, "Project README listing, stale project version", evidence=True)
replace_once(C, "On the verification machine (Section 12.2) the passing run was:", "A passing run looks like this:", 13, "Section 1.2, lead-in to the pipeline output", evidence=True)
replace_once(C, " because the POM sets `failIfNoTests` to true (Section 12.2).", " because the POM sets `failIfNoTests` to true.", 13, "Section 1.3, reference to Section 12.2", evidence=True)
replace_once(C, " Section 12.2 records the result.", "", 13, "Section 1.4, reference to Section 12.2", evidence=True)
replace_all(C, "Section 12.3", "Section 12.2", 5)
replace_once(C, "Section 12.2 lists twenty-seven faults and the tests that caught them;", "Section 12.2 lists thirty faults and the tests that caught them;", 13, "B3, count of faults", evidence=True)
replace_once(C, "each applied to its own scratch copy of the final code, on the exact configuration of Section 12.2.", "each applied to its own scratch copy of the final code.", 13, "Section 9, reference to the exact configuration", evidence=True)

# ---- ADR-013 listing
replace_once(C, "Date: 13 October 2026 (Asia/Baghdad)\nStatus: Implemented teaching example; peer review pending. The integration boundary (Blueprint D1) is an interim choice awaiting the module leader.",
             "Date: 13 October 2026\nStatus: Implemented teaching example; peer review pending.", 13, "ADR-013 listing, date and status lines", evidence=True)

# ---- section 7.8 and 7.9: neutral lessons
rewrite_line(C, "### 7.8 The timeout defect, found in review",
  "### 7.8 A timeout that does not cover the body", 13, "Section 7.8 heading")
rewrite_line(C, "The client of Version 1.0 called the blocking `send` with a request timeout.",
  "A client that calls the blocking `send` with a request timeout relies on a timeout that the JDK documents as the time within which the response must be *received*. The documentation says nothing about a body [8]. A test that uses a stub which waits before sending anything exercises the one case the timeout certainly covers.",
  13, "Section 7.8, first paragraph (Version 1.0 client)")
rewrite_line(C, "A review of the chapter tried another:",
  "A different case: a server that sends the headers and the first byte at once and holds the rest. With the client's timeout at 300 ms and the server holding the body for 1,600 ms, a client that relies on the request timeout alone returned a valid result after about 1.7 seconds. The policy said “a bounded wait” and that client did not keep it, because the timeout bounded the wait for the headers and not for the whole answer.",
  13, "Section 7.8, second paragraph (review, OpenJDK 17.0.20 and JDK 24.0.2 measurements)")
rewrite_line(C, "The correction sends the request asynchronously",
  "The client in this chapter therefore sends the request asynchronously and waits for the future for at most the configured time. On timeout it cancels the future, which asks the client to drop the exchange and is not guaranteed to be prompt or to take effect [13][14], and fails the lookup with a message that names the wait. The caller does not depend on the cancellation, because it has already stopped waiting. An interrupted wait cancels, restores the interrupt flag and fails. A failed future becomes a `Failure` whose message names the cause's class. The header timeout stays on the request.",
  13, "Section 7.8, fix paragraph (wording 'the correction')")
rewrite_line(C, "| New test `aStalledBodyIsAFailureWithinTheOverallWait` against the **Version 1.0 client** |",
  "| New test `aStalledBodyIsAFailureWithinTheOverallWait` against a client that relies on the request timeout alone | Fails: `execution timed out after 5000 ms` (the outer deadline), because the client waits for the stub to release the body and returns it |",
  13, "Section 7.8 table, first row")
rewrite_line(C, "| The same test against the corrected client |",
  "| The same test against the client in this chapter | Passes. A probe with the same 300 ms timeout and 1,600 ms stall fails the lookup after about 330 ms: `Directory did not answer within 300 ms.` |",
  13, "Section 7.8 table, second row (exact figures and JDK removed)")
rewrite_line(C, "Figure 13.3 of Version 1.0 put the count and duration rules before the register was read.",
  "The order of the checks is observable when more than one thing is wrong. The gate checks the flag, the item, and (for fewer than one day) steps aside; otherwise it reads the clock and the register; then the coordinator applies the count and duration rules and the availability rule. A four-day visitor request with an unreadable register therefore fails with the register's error and is not rejected for its duration. The test `precedence_theRegisterIsReadBeforeTheCountAndDurationRulesApply` pins both ends: four days with an unreadable register throws the register's exception, and zero days does not read the register and returns the limit rejection. It is not one of the eighteen acceptance examples and is not named `ac<N>_`.",
  13, "Section 7.9, first paragraph (statement about Figure 13.3 of Version 1.0)")

# ---- section 12
replace_once(C, "## 12. Instructor notes and verification", "## 12. Instructor notes")
cut_prefix(C, 13, "Section 12.1, 'Alignment with Chapter 12' paragraph", "**Alignment with Chapter 12.**", "### 12.2 Verification record")
cut(C, 13, "Section 12.2, Verification record (environment, reconstruction, results table, timeout probe)",
    "### 12.2 Verification record", "### 12.3 Do the tests detect faults?")
replace_once(C, "### 12.3 Do the tests detect faults?", "### 12.2 Do the tests detect faults?")
replace_once(C, "through `mvn test` under the exact configuration, against the final suite of 232 invocations. **Twenty-nine were caught. One survived, and it is an equivalent change** (below). Version 1.0 ran twenty-seven faults against 230 invocations and caught all of them; the HTTP rows have changed because the client changed. The harness reports",
             "through `mvn test`. **Twenty-nine were caught. One survived, and it is an equivalent change** (below). The harness reports", 13, "Section 12.2 lead-in (exact configuration, 232 and the Version 1.0 comparison)", evidence=True)
replace_once(C, "Two of the HTTP mutants did not compile at first (a `get()` without a timeout makes the `TimeoutException` handler unreachable) and were rerun as `get(Long.MAX_VALUE, ...)`, which is the same fault expressed so that the code still compiles.\n\n", "", 13, "Section 12.2, note on two mutants that did not compile at first", evidence=True)
replace_once(C, "The experiment of Version 1.0 **could not have found** the defect of Section 7.8, because none of its faults concerned the body of the response. A fault experiment finds",
             "Before the stalled-body test existed, no fault in the experiment concerned the body of the response, so the experiment could not have found the problem of Section 7.8. A fault experiment finds", 13, "Section 12.2, closing paragraph (Version 1.0 wording)", evidence=True)

log(13, [
 "Companion: removed the `Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4` line and the whole `Version note` (the three corrections found by the independent review). The files-changed list in that note went to evidence (R1, R2, R4, R7).",
 "Section 1: first paragraph, `and the verification record` is now `and teaching notes`; the input checkpoint paragraph no longer names `Version 1.1` of the Chapter 10 and 11 companions or `159 JUnit invocations`; reconstruction steps 1 and 2 no longer say `(Version 1.1)`; `only the project version becomes 0.13.0` is now `only the project version changes`.",
 "Section 1: the paragraph `Boundary decision (Blueprint D1, interim)` is now `The two boundaries`, a plain description. It keeps the point that a different boundary would change the adapters and keep the policy table and tests, and drops the Blueprint ID and `The module leader has not yet decided D1`. The same interim sentence was in the ADR-013 listing's `Status` line, now `Implemented teaching example; peer review pending`, and its date line lost `(Asia/Baghdad)`. **Note:** the working project folder still has the old ADR-013 text. It is not published.",
 "Section 1.0 `Checkpoint manifest` (Blueprint version, SHA-256 of the Chapter 10 and Chapter 11 companions, verified build line) moved to evidence (R6, R8).",
 "Section 1.2: `On the verification machine (Section 12.2) the passing run was:` is now `A passing run looks like this:`. Removed the references to the old Section 12.2 (empty-stage check, simulated release). `Section 12.3` references now say `Section 12.2` (three places), and B3 says the fault table lists thirty faults (it said twenty-seven).",
 "Section 7.8 was `The timeout defect, found in review`; it is now `A timeout that does not cover the body`, a neutral lesson. Removed: the Version 1.0 client, `A review of the chapter`, the review's OpenJDK 17.0.20 figure, the JDK 24.0.2 probe figures and `I did not run the probe on a Java 17 runtime`. Kept: the JDK documentation point, the 300 ms and 1,600 ms case, the asynchronous fix with cancellation [13][14], the table of what the new test shows (fails against a client that relies on the request timeout alone with `execution timed out after 5000 ms`; passes against the chapter's client, which fails the lookup after about 330 ms), and the list of what did not change. Please read it once: it is the main narrative change in this chapter.",
 "Section 7.9: removed `Figure 13.3 of Version 1.0 put the count and duration rules before the register was read`; the paragraph now starts from the observable order of checks. The test and the point that a different precedence needs a contract change are unchanged.",
 "Section 12 retitled `Instructor notes`. Removed from 12.1 the paragraph `Alignment with Chapter 12` (notes about the mismatch with the other author's chapter and the scripts of Chapter 13 versus 14; also in the register). Section 12.2 `Verification record` (Windows 11, Maven 3.9.11, JDK 24.0.2, the reconstruction paragraph, the results table, the timeout probe, the review's Java 17 figure) moved to evidence. The fault experiment became 12.2.",
 "Kept: the 30-fault table and its notes. Removed `Version 1.0 ran twenty-seven faults against 230 invocations`, the `exact configuration` and `232 invocations` wording, the note that two mutants did not compile at first, and the closing sentence about what the experiment of Version 1.0 could not find (now: `Before the stalled-body test existed, ...`).",
 "Manuscript: see the manuscript entry below.",
])

# ---- manuscript
replace_once(M, "the model answers and the verification record.", "the model answers and teaching notes.", 13, "Manuscript line 38", evidence=True)
replace_once(M, "were opened on 13 October 2026; the manuscript was written the same day, Asia/Baghdad.", "were opened on 13 October 2026.", 13, "Manuscript source note", evidence=True)
print("chapter 13 companion done; manuscript pending")
