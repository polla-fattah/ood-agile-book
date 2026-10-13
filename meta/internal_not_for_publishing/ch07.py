from cleanup_lib import *
C = "Chapter_07_Code_Explanations_and_Solutions.md"
M = "Chapter_07_Testing_as_a_Design_Practice.md"

replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.1 • 13 October 2026 • reviewed against Blueprint v0.3\n", "*OO Development and Agile Practices*\n", 7, "header version line", evidence=True)
replace_once(C, "model solutions and observed verification evidence.", "model solutions and teaching notes.", 7, "Line 9 (verification evidence wording)", evidence=True)
replace_once(C, "| Java | Java 17 language/API target; author runtime OpenJDK 17.0.20 | Application and test execution |",
             "| Java | Java 17 language/API target | Application and test execution |", 7, "Tool table row (author runtime)", evidence=True)

rewrite_line(C, "The resource does not stop Mockito from loading its ByteBuddy agent.",
  "The resource does not stop Mockito from loading its ByteBuddy agent. On a recent JDK the log shows `WARNING: A Java agent has been loaded dynamically`, with and without the resource, and the tests pass. Passing `-XX:+EnableDynamicAgentLoading` to the test JVM (Surefire's `argLine`) removes the warning. The JVM states that dynamic agent loading will be disallowed by default in a future release, so check the Mockito documentation for the setup recommended for the JDK you use. The behaviour can differ between JDK and Mockito versions.",
  7, "Mockito agent warning paragraph (JDK 24 and Mockito 5.23.0 specifics, and the note that JDK 17 was not available)")

rewrite_line(C, "Sixteen single faults were introduced one at a time into copies of the completed project",
  "Sixteen single faults were introduced one at a time into copies of the completed project, and each copy was run through `mvn test`. Fifteen were rejected by at least one named test: fourteen are in the table below, and the fifteenth, the loan snapshot, follows it. One was not rejected, and it follows as well.",
  7, "Section 6.1 lead-in (counting history removed; totals made consistent with the final tests)")
rewrite_line(C, "Two faults survived the version 1.0 tests.", "Two faults need a closer look.", 7, "Section 6.1 'Two faults survived the version 1.0 tests'")
rewrite_line(C, "**The `loans()` snapshot could be modified.**",
  "**The `loans()` snapshot could be modified.** Replacing `List.copyOf(loans.values())` with a plain `ArrayList` would pass the other tests, although the chapter's rule table says loan snapshots are unmodifiable. An assertion in `checkoutAndReturnUseTheSuppliedClock` rejects that fault.",
  7, "Section 6.1, loans snapshot paragraph (version 1.1 history removed)")
rewrite_line(C, "**An enquiry that adds a temporary record and removes it again.**",
  "**An enquiry that adds a temporary record and removes it again.** This one survives, and it is a good teaching case. With identifiers derived from the list size, a record added and then removed leaves no trace: the records, notices and next identifier all end up exactly as before. In a sequential program, no test can tell this implementation from the correct one. It would matter only if something could observe the list between the add and the remove, such as a concurrent caller. The right response is to reject the design by reading it, as the AI activity does, and to avoid claiming that a test can catch it. The identifier example is still worth keeping, because it protects the promise if identifiers ever come from a separate counter.",
  7, "Section 6.1, add-then-remove paragraph ('still survives' reworded)")

# Section 12: move the verification record, keep two general paragraphs
cut(C, 7, "Section 12 Verification record (versions, cached-versions run, exact-configuration run, results tables)",
    "## 12. Verification record",
    "The 35 JUnit invocations consist of one TDD test, eight additional availability invocations, ten policy table rows, nine loan invocations, three Mockito tests and four legacy wrappers. The count is an execution inventory, not a claim of exhaustive correctness or a quality score.",
    replacement="## 12. What the build establishes\n")

# manuscript
rewrite_line(M, "One practical warning. On newer JDKs, Mockito may still attach",
  "One practical warning. On newer JDKs, Mockito may still attach its ByteBuddy agent when it starts, and the JVM then prints “A Java agent has been loaded dynamically”. This appeared with the Mockito version printed in the companion POM, even with the proxy setting, and the tests still passed; passing `-XX:+EnableDynamicAgentLoading` to the test JVM removed the message. Other JDK and Mockito combinations may behave differently. The JVM states that dynamic loading will be disallowed by default in a future release, so check Mockito's documentation for the setup recommended for your JDK.",
  7, "Manuscript, practical warning about the Mockito agent (JDK 24.0.2 and version comparison removed)")
replace_once(M, "not a claim to use every tool's newest release; the companion records which versions were actually run.", "not a claim to use every tool's newest release.", 7, "Manuscript, source note", evidence=True)

log(7, [
 "Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).",
 "Companion line 9: `observed verification evidence` is now `teaching notes`. Tool table: removed `author runtime OpenJDK 17.0.20` (R8).",
 "Companion section 12 `Verification record` moved to evidence in full: the version 1.0 and version 1.1 paragraphs (OpenJDK 17.0.20; Maven 3.9.16 and the cached versions; the table of differing versions), the exact-configuration run (Maven 3.9.11 with SHA-512 check, JDK 24.0.2, clean repository), the two results tables (red, green and refactor cycle; mutation and restoration; reconstruction), the cached-versions observation table, and the sentence that the author's network needed proxy settings (R3, R8). Section 12 is now `12. What the build establishes` and keeps two paragraphs: the inventory of the 35 invocations (an expected-output statement) and the limits statement that a Maven report does not establish provider behaviour, storage, concurrency, identity or milestone completeness.",
 "Section 6.1, the wider fault experiment: this was a real inconsistency, not just history. The text said `Fourteen were rejected` and listed fourteen rows, and then said the `loans()` snapshot fault is now caught, so the final suite rejects fifteen and one survives. Rewrote the lead-in to say fifteen are rejected (fourteen in the table and the loan snapshot after it) and one is not (the equivalent add-then-remove change). Removed the sentence about an earlier counting error (`version 1.1 said fifteen and thirteen`), `Two faults survived the version 1.0 tests`, and `Version 1.1 adds one assertion...`. Please check this reading of the counts: it follows the experiment results kept in the evidence file.",
 "Companion Mockito warning paragraph: removed JDK 24, Mockito 5.23.0, `JDK 17 was not available for this review` and `5.20.0 was not downloaded`. The advice stands.",
 "Manuscript: the practical warning about the Mockito agent no longer names JDK 24.0.2 or compares two Mockito versions; the source note no longer says that the companion records which versions were run. `Sources checked 12 and 13 October 2026` is an access date and stays. The `Asia/Baghdad` time zone in the manuscript's checkout-date example is teaching content (a local-date example) and stays.",
])
print("chapter 7 done")
