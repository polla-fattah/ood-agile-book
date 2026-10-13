from cleanup_lib import *
M = "Chapter_13_Integration_Delivery_and_Feedback.md"

# formatting repair: the heading had been appended to the end of the policy paragraph
replace_once(M, "and neither is assumed now. ### A timeout that covers less than you think\n", "and neither is assumed now.\n\n### A timeout that covers less than you think\n")

replace_once(M, "the Chapter 11 project (159 JUnit invocations) and Chapter 12's", "the Chapter 11 project and Chapter 12's", 13, "Manuscript, entry checkpoint (159 invocations)", evidence=True)
replace_once(M, " The completed checkpoint has 232 invocations. The Chapter 11 listings are not repeated:", " The Chapter 11 listings are not repeated:", 13, "Manuscript, entry checkpoint (232 invocations)", evidence=True)

rewrite_line(M, "An earlier version of this chapter's client relied on that timeout alone",
  "A client that relies on that timeout alone, tested with a stub that waits **before** sending anything, passes its test. That is the only case the test imagines. Try another: a server that sends the headers and the first byte of the body at once, and then holds the rest for 1,600 milliseconds, with the client's timeout set to 300. The lookup **succeeds after about 1,700 milliseconds**. The policy said “a bounded wait” and the client did not keep it, because the timeout bounded the wait for the headers and not the whole answer.",
  13, "Manuscript 13.2, paragraph about the earlier client, the review, and the JDK 24.0.2 and OpenJDK 17.0.20 figures")
rewrite_line(M, "The fix is a deadline on the whole lookup.",
  "The fix is a deadline on the whole lookup. The client sends the request asynchronously and waits for the result for at most the configured time; if the time runs out it asks the client to drop the exchange and fails the lookup. Asking is all it can do: the documentation says that cancelling the future attempts to cancel the exchange and that the cancellation is not guaranteed to be prompt or to take effect at all [13][14]. The caller does not depend on it, because the caller has already stopped waiting. The header timeout stays as well. Removing the overall deadline is caught by the new test. Removing the header timeout alone cannot be detected by any test, because the overall deadline still bounds the call: the fault experiment records it as an equivalent change.",
  13, "Manuscript 13.2, fix paragraph (wording 'The client now sends')")
rewrite_line(M, "A new stub scenario, `SLOWBODY`,",
  "A new stub scenario, `SLOWBODY`, sends the headers and the first byte and then holds the rest until the stub is closed. The new test asserts the **outcome**, a failure and not a result, and runs it with a generous outer deadline so that a defect shows as a failed test and not as a hang. Run against a client that relies on the request timeout alone, that test fails with `execution timed out after 5000 ms`. Against the client of this chapter the lookup fails after about 330 milliseconds. The lesson is wider than HTTP: a test of a failure path covers the failure you imagined, so try a different one. A second reader, or a fault experiment that applies a different fault, can find what you could not.",
  13, "Manuscript 13.2, SLOWBODY paragraph ('old client', 'corrected client', 'a review that tries a different one')")
replace_once(M, "The 159 invocations of the Chapter 11 checkpoint passed unchanged after that edit, and the new tests bring the total to 232.", "The inherited Chapter 11 tests passed unchanged after that edit.", 13, "Manuscript 13.7, counts 159 and 232", evidence=True)
log_add([
 "Project README listing inside the companion: `only the project version becomes 0.13.0` was stale (the project is 0.13.1) and is now `only the project version changes (to 0.13.1)`.",
 "Manuscript 13.2: **formatting repair.** The heading `A timeout that covers less than you think` had been joined to the end of the policy paragraph on one line. It is a heading again, on its own line.",
 "Manuscript 13.2, `A timeout that covers less than you think`, rewritten as a neutral lesson, with the same arguments: removed `An earlier version of this chapter's client`, `A review of the chapter then ran`, the JDK 24.0.2 and OpenJDK 17.0.20 figures, `the old client`, `the corrected client`, and `a review that tries a different one is evidence you cannot produce alone` (now `A second reader, or a fault experiment that applies a different fault, can find what you could not`). Please read it once.",
 "Manuscript: entry checkpoint no longer says `159 JUnit invocations` or `The completed checkpoint has 232 invocations` (R5); line 38 `the verification record` is now `teaching notes`; in 13.7 `The 159 invocations ... passed unchanged ... total to 232` is now `The inherited Chapter 11 tests passed unchanged after that edit`; the source note lost `the manuscript was written the same day, Asia/Baghdad`.",
])
print("chapter 13 manuscript done")
