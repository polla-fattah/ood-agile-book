# SE506 — candidates to remove or rewrite before a first-draft publication

*Prepared 13 October 2026. This is a **list for your decision**. Nothing in any chapter, companion or other file has been changed or removed. Every item below needs your yes, no or change before I touch it.*

## 1. What I looked at

All 30 chapter files (15 manuscripts and 15 companions; the Chapter 12 pair is by another author and is listed but not mine to edit). I searched for version stamps, dates, build-environment and test-count statements, verification records, references to the blueprint and its decision IDs, review history, and notes about other chapters or other authors.

The working documents in the folder are a separate question (Section 4).

## 2. The candidates, grouped

Each group says what it is, where it is, what I would do, and what I would keep. “Remove” means delete the text. “Rewrite” means keep the idea and take out the working history. “Move” means keep the content in an internal file, outside the published chapters.

### A. Version stamps and change notes — recommend: remove

A first draft has no version history. These tell the reader about earlier drafts.

| Where | What | Count |
|---|---|---|
| Line 5 of every companion | `Version 1.x • 13 October 2026 (Asia/Baghdad) • reviewed against / written against Blueprint v0.3 or v0.4` | 14 files (Ch1–Ch11, Ch13–Ch15; the Ch12 companion has `Version 1.0 • 13 October 2026`) |
| Ch12 manuscript line 6 | `Version 1.0 • 13 October 2026` | 1 (other author) |
| Companion “Version note” / “What changed in this version” paragraphs | Ch5 (adds the PMD lab), Ch10 (“Version 1.0 carried older copies of nine files”), Ch11 (“merges in material from a second draft”), Ch13 (corrections found by an independent review), Ch14 (rebuilt on the corrected Chapter 13), Ch15 (follows an independent review) | 6 |
| Ch6 manuscript line 334 | “`DemoContainer` ... (version 1.1 of the companion, 13 October 2026)” | 1 |

Keep: the project's own version number (0.13.1, 0.14.0) because it is part of the code example, not a document version.

### B. Authoring dates and time zone — recommend: rewrite

| Where | What |
|---|---|
| Source notes at the end of manuscripts (Ch2–Ch15) | “Sources checked 12 and 13 October 2026”, “the manuscript was written the same day, Asia/Baghdad”, “manuscript revised 13 October 2026, Asia/Baghdad” |
| Companion headers | `(Asia/Baghdad)` |
| Companion verification text | “13 October 2026” on every run |

Rewrite to keep **access dates for web sources** (they are normal in a reference list and help readers judge how current a source is), and remove the sentences about when the manuscript was written. The Asia/Baghdad time zone goes everywhere.

### C. Verification records, build environment and “not run” statements in the companions — recommend: move, and keep a short general note

These are the author's evidence, and they are specific to this machine: `Windows 11`, `Maven 3.9.11`, `JDK 24.0.2`, “exact-configuration run”, “no JDK 17 was available”, “reconstruction ... matched byte for byte”, “Mermaid 10.9.1 rendered in the browser pane”, “N web sources were opened”.

| Companion | Section(s) |
|---|---|
| Ch1 | §4 Verification and use in later chapters (“Verified on 13 October 2026 (review of version 1.0)”, and a paragraph about an earlier run on OpenJDK 17.0.20) |
| Ch2 | §12 Verification record (“Re-verified on 13 October 2026 (review of version 1.0)”) |
| Ch3 | §12 Instructor guidance and verification record (“Re-verified on 13 October 2026 (review of version 1.0)”) |
| Ch4 | §10 Verification record and teaching notes |
| Ch5 | §12 Verification record and teaching notes |
| Ch6 | §13 Verification record |
| Ch7 | §12 Verification record, including “Exact-configuration run (13 October 2026)” |
| Ch8 | “Exact-configuration run” paragraph near the end |
| Ch9 | §12 Verification record, including the exact-configuration run |
| Ch10 | §11.2 Verification record |
| Ch11 | §12.2 Verification record |
| Ch12 | §8 Verification record and limits (other author) |
| Ch13 | §12.2 Verification record (and its “Reconstruction” paragraph) |
| Ch14 | §10.2 Verification record (and its “Reconstruction” paragraph) |
| Ch15 | §10.2 Verification record (and its “Reconstruction” paragraph) |

**Two things in these sections are not working notes and should be kept:**

1. The **fault experiments** (Ch13 §12.3, Ch14 §10.3, Ch15 §10.3, and similar tables in earlier chapters). The manuscripts point to them as teaching evidence. If you keep them, the “Verification” heading and the machine details around them should go and the tables stay.
2. Honest **limits** that a reader needs: that a check covers certain inputs only, that an experiment used a small set of faults. These are general and belong in the text.

What I would **not** publish: the JDK and OS of one machine, the “not verified on Java 17” sentences tied to that machine, run-by-run results, and reconstruction paragraphs.

Dependency to resolve before moving them: several manuscripts and companions say “and the verification record” (for example Ch11, Ch13, Ch14 and Ch15 manuscripts, line 38 or 47) or point to a companion section number by name. Those references would need to change.

### D. Test counts and “Tests run” figures — recommend: keep once per chapter, remove elsewhere

The counts are useful where a reader reproduces the build (the “Expected output” section of a companion). They go stale the moment a test is added, and they are repeated in many places.

| Place | Examples |
|---|---|
| Manuscript entry checkpoint | Ch11 line 28 (121 invocations), Ch13 line 28 (159, 232), Ch14 line 28 (232, 235) |
| Manuscript body | Ch13 line 276; Ch14 lines 89–93, 112, 207, 236–238, 334; Ch7 line 105 (not a count, a description of reporting) |
| Companion “Expected output” | Ch7, Ch8, Ch9, Ch10, Ch11, Ch13, Ch14, Ch15 (keep) |
| Handover, README and release-notes text inside the Ch14 project | HANDOVER.md, RELEASE-NOTES-0.14.0.md, and `scripts/handover-check.sh` (the check is meant to hold the numbers, so keep these) |
| Experiment results with counts | “73 of 235”, “4 of 232”, “45 of 159” in Ch14 |

My proposal: remove the counts from **manuscript prose** (leave “the project's build passes”), keep them in each companion's *Expected output* and in the handover check, and keep the experiment counts only as results in the companion tables, labelled with the checkpoint they came from.

### E. Checkpoint manifests with SHA-256 — recommend: remove for the first draft

Ch13 §1.0 and Ch14 §1.0 list SHA-256 of the prerequisite companions. They were added for traceability in review. Each is invalid the moment any prerequisite is edited, which will happen in the consistency review. Remove now and add back when the text is frozen, or generate them as part of a release step.

### F. History, review and other-author material — recommend: rewrite or remove

| Where | What | Action |
|---|---|---|
| Ch13 manuscript §13.2 (line 117) | “An earlier version of this chapter's client ... A review of the chapter then ran...” (with the Java 17 figure from the review) | Rewrite as a neutral lesson: a request timeout bounds the wait for the headers, here is the probe and the fix. Drop “earlier version”, “review”, and the reviewer's measurement |
| Ch13 companion §7.8 (“The timeout defect, found in review”) | Same story, with the old client's results | Rewrite the same way |
| Ch14 companion §5.2 (end of E3 notes), §5.3, §5.4 | “the first version of this chapter described it as...”, “Version 1.0 figures were...” | Remove the history; keep the lesson |
| Ch13 companion §12.1 “Alignment with Chapter 12”; Ch14 companion §10.1 “Alignment with the other chapters” | Notes about mismatches with Chapter 12 and the Ch13 scripts | Remove. These are for you and the Chapter 12 author, and they already sit in the register |
| Ch11 companion “Version note” | “merges in material from a second draft” | Remove |
| Ch15 companion §10.2 | The reviewer's Java 17 results of the lab | Remove or move with the verification record |
| Ch14 manuscript §14.1 “Review feedback” and companion §5.4 | A **constructed** review of the visitor change | **Keep.** It is labelled as constructed and is a teaching device, not history |
| Ch1 manuscript, Ch2 and others | “the alignment review” statements | none found in manuscripts; the companions mention “reviewed against Blueprint” (see A) |

### G. Blueprint and decision IDs and interim decisions — recommend: rewrite

| Where | What |
|---|---|
| Companion §1 of Ch13 | “Boundary decision (Blueprint D1, interim)... The module leader has not yet decided D1” |
| Ch6, Ch7, Ch13, Ch14 companions | Direct mentions of G-rules and D-decisions (about 14 hits in Ch14, mostly in the dated header and verification text) |
| Ch7 manuscript | One mention of the blueprint |

Rewrite “interim decision” statements as plain description (“this chapter uses a local HTTP stub and a local file as the two boundaries”). Remove ID references. If D1 is later decided differently, the chapter changes then.

### H. Forward references to material that is not written — recommend: keep the pointer, remove “not written yet”

| Where | What |
|---|---|
| Ch9 manuscript line 433 | “Appendix E is planned ... but is not written yet” |
| Ch14 manuscript §14.5 | “Appendix C will supply ... Appendix E will give...” |
| Ch15 manuscript summary | “The appendices that follow collect...” |
| Ch1, Ch2, Ch3 and others | Pointers to Appendices A, B, C, D, E |

A first draft that is published without the appendices needs these pointers reconciled: either the appendices exist at that point, or the references say “see the appendix” without a status. Appendix A is being written by someone else, so I would leave these for that decision.

### I. “Not opened” source notes — recommend: decide

Several source lists say things like “Martin (2002) ... Not opened for this chapter; publication details come from the module descriptor” (Ch11, Ch13, Ch14, Ch15 and others). They are honest, and they are also author process notes. Options: keep (honesty about what was consulted), reword to “Reading from the module descriptor”, or remove the “not opened” part. I need your preference.

### J. Tool-specific and machine-specific statements in student text — recommend: rewrite

| Where | What |
|---|---|
| Ch7 manuscript line 241 | “On JDK 24.0.2 this appeared with the Mockito 5.20.0 pri...” (the dynamic-agent warning) |
| Ch13, Ch14, Ch15 manuscripts | Specific remarks about JDK 24.0.2 and “OpenJDK 17.0.20” |
| Ch14 HANDOVER.md text | “the checks recorded here used JDK 24.0.2” |

Rewrite to “on a recent JDK”. The warning itself is useful to students, so keep it.

## 3. What I would deliberately keep

- Every label saying that sample AI output is **constructed to illustrate** (G11). This is a rule of the book.
- Statements of what a check does not show, written generally (“a green pipeline is evidence about the checks it contains”).
- Access dates for web sources.
- The project's own version numbers and its handover documents.
- The fault-experiment tables, if you agree with Section C.

## 4. Working documents in the folder — not part of a book release

These are not chapters and should not be published with them. I would leave them where they are and list them so they are not shipped by accident:

- `SE506_Textbook_Blueprint_and_Authoring_Instructions.md`
- `SE506_Blueprint_Alignment_Review_and_Chapter_Change_Plan.md`
- `SE506_Chapters_12_to_15_Assessment_and_Change_Plan.md`
- `Unresolved_Items_Chapters_1-3.md` (the register)
- `Remaining_Chapters_Todo.md`
- this file
- the module descriptor (`.docx`) if it is not to be redistributed

## 5. Decisions I need from you

1. **Section C:** move the verification records to an internal file (my recommendation), delete them, or keep a trimmed version? And keep the fault-experiment tables?
2. **Section D:** remove counts from manuscript prose and keep them in companions only?
3. **Section E:** remove the SHA-256 manifests for now?
4. **Section F:** rewrite the Chapter 13 and 14 incident narratives as neutral lessons?
5. **Section I:** how to word “not opened” source notes?
6. **Scope:** shall I do the whole list in one pass after your answers, chapter by chapter with a report of each change, or only Chapters 1–11 and 13–15 (leaving Chapter 12 to its author)?
7. **Copy:** make the changes in place, or write the cleaned versions to a separate folder (for example `publish/`) so the working files stay intact? I recommend the separate folder, because it removes the risk of losing the evidence and lets you compare.

## 6. Commands I used, in case you want to rerun the counts

```bash
grep -c -i '^Version [0-9]\|Version note\|What changed in this version' Chapter_NN_*.md
grep -c '13 October 2026\|Asia/Baghdad' Chapter_NN_*.md
grep -c 'JDK 24\|24\.0\.2' Chapter_NN_*.md
grep -c -i 'invocations' Chapter_NN_*.md
grep -n -i 'verification record' Chapter_NN_Code_Explanations_and_Solutions.md
```
