from cleanup_lib import *
C = "Chapter_15_Code_Explanations_and_Solutions.md"
M = "Chapter_15_AI_as_a_Software_Engineering_Assistant.md"

replace_all(C, "Section 10.3", "Section 10.2", 2)
rewrite_line(C, "The results establish the selected behaviours on the supplied inputs, in the stated environment.",
  "The results establish the selected behaviours on the supplied inputs. They do not establish how a real assistant would behave on this task, or that the acceptance examples are the right examples.",
  15, "Section 10.2 closing limits sentence (stated environment and Java 17 removed)")

# manuscript
replace_once(M, "and the model answers and the verification record.", "and the model answers and teaching notes.", 15, "Manuscript line 47", evidence=True) if "and the model answers and the verification record." in read(M) else replace_once(M, "the model answers and the verification record.", "the model answers and teaching notes.", 15, "Manuscript line 47", evidence=True)
replace_once(M, "In the experiment, plain `javac` on JDK 24 reported only the first error", "In the experiment, plain `javac` on a JDK of version 21 or later reported only the first error", 15, "Manuscript 15.4, JDK 24", evidence=True) if "plain `javac` on JDK 24 reported only the first error" in read(M) else None
replace_once(M, "(Companion, Section 10.3)", "(Companion, Section 10.2)")
replace_once(M, "were opened on 13 October 2026; the manuscript was written the same day, Asia/Baghdad. Tool and service behaviour changes quickly, so each source is dated by that opening.", "were opened on 13 October 2026. Tool and service behaviour changes quickly, so each source is dated by that opening.", 15, "Manuscript source note", evidence=True)

log(15, [
 "Companion: removed the `Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4` line and the `Version note` (the four review changes) (R1, R2, R4, R7). First paragraph: `and the verification record` is now `and teaching notes`.",
 "Section 10 retitled `Instructor notes`. Section 10.2 `Verification record` moved to evidence: Windows 11, Maven 3.9.11, JDK 24.0.2, the reconstruction paragraph, the results table (including the check-record results and the dependency status codes), and the row with the independent review's Java 17 results (OpenJDK 17.0.20, attributed to the review). The fault experiment is now `10.2 Do the tests detect faults?` and the one reference to `Section 10.3` was updated.",
 "Kept: the ten-fault experiment table and its explanation, the dependency status table in section 6.6 (it is the exercise's own evidence, with the command and date), and the closing limits sentence without `the stated environment` and `behaviour on a Java 17 runtime`.",
 "Model record `docs/AI-RECORD-earliest-start.md` inside the listings, and the compile table in section 6.1 and flawed alternative 8.2: `JDK 24.0.2` and `JDK 24` replaced by `a JDK of version 21 or later` or `a newer JDK`. The record still names Maven 3.9.11 and `--release 17`, because a verification record should name the commands. Its Limits line now says the code was compiled for Java 17 and run on a newer JDK, so no Java 17 run is claimed. **Note:** the working lab folder still has the old text. It is not published.",
 "Manuscript: line 47 `and the verification record` is now `and teaching notes`; the 15.4 sentence about plain `javac` no longer says `JDK 24`; the reference to the fault experiment now says `Section 10.2`; the source note lost `the manuscript was written the same day, Asia/Baghdad`.",
 "Not changed: the headings `Verification` inside the AI assistance record template and the filled record. They are fields of the record that the chapter teaches (section 15.8), not verification records of the book.",
])
print("chapter 15 done")
