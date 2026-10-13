---
title: "Appendix E: Critical Reading and Project Evidence"
description: "A method for the individual critical book review, and guides to contribution evidence, the final handover and the individual reflection. It follows the module descriptor and adds no rubric or policy."
weight: 250
---

*OO Development and Agile Practices*  
*Designing, Testing and Evolving Software with AI Assistance*

## How to use this appendix

Two pieces of work in this module ask you to show your own thinking and your own evidence. The **individual critical review** of a software-design book asks you to read carefully and judge what you read. The **final project** asks your team to hand over a system someone else can run, and asks each of you to explain, with evidence, what you contributed. This appendix gives a method for each. Sections E.1 to E.3 are about the review; E.4 to E.6 are about the project.

> **This appendix is guidance, not a rule.** The module descriptor and your module leader's assignment brief decide the deadlines, lengths, formats, approved reading list, rubrics and the rules on the use of AI tools. Where they differ from this appendix, they are right. Nothing here adds a requirement or changes how any work is marked.

Start the reading method in Week 1. Chapter 1 introduces the reading record and Chapter 9 gives a checkpoint to compare with your progress; this appendix develops both.

## E.1 What the review asks

The descriptor describes the first assessment this way. Each student selects a software design or agile engineering book from a list approved by the module leader and writes an individual critical review of 1,500 to 2,000 words. The review summarises the book's purpose and audience, critically evaluates its principles and examples, discusses the trade-offs and limits of its advice and reflects on how it applies to engineering AI-enabled systems, supported by concrete code or project examples and at least three additional sources. It is due in Week 8 and is submitted as a PDF through Moodle, which checks it for similarity. The descriptor's rubric lists the criteria and their weights; read it before you start, and again before you submit.

**The book comes from the approved list.** The list is the module leader's. The descriptor gives examples of the kind of book that may be on it (Clean Code, Refactoring, Design Patterns, Working Effectively with Legacy Code and Accelerate). This appendix does not supply or change the list. Check the current one on Moodle and choose in the first two weeks, because a careful review cannot be written from a late start.

**This textbook is not the book you review.** Reading it does not satisfy the assignment. It can help in one way: the Campus Equipment Lending project gives you concrete code to test a book's advice against (see E.2).

## E.2 A method for reading

### Read for claims, then test them

Technical books recommend practices that suit particular circumstances. Treat each recommendation as a claim to understand and then evaluate. Take the strongest reasonable reading of the advice and not an exaggerated one. Keep a reading record as you go, with the six entries of Chapter 1, Section 1.7:

| Entry | Question |
|---|---|
| Claim and location | What exactly does the author recommend, and where? (chapter and page, or a stable section) |
| Context | What problem and assumptions surround the advice? |
| Supporting example | How does the example demonstrate the claimed benefit? |
| Limitation | Under what conditions might the cost outweigh the benefit? |
| Project application | What would change if we applied it to our system? |
| Further evidence | Which independently checked source or experiment helps evaluate it? |

Add one habit from Chapter 9: keep three things apart in your notes, and label each. **What the author claims.** **What you infer.** **What a tool suggested**, if you used one. A review that mixes them cannot be checked, and your reader cannot tell whose idea an argument is.

### Ask a question for each part of the task

The prompts below follow the parts of the descriptor's task. They are questions to think with and are not a template for headings.

| Part of the task | Questions to ask |
|---|---|
| Purpose and audience | What problem was the author answering, and for whom? What did the author assume the reader already knew? When was it written, and what has changed? |
| Principles and examples | Does the argument follow from its premises? Are the examples realistic, or small enough to hide the difficult cases (persistence, concurrency, failure)? Does the author claim a rule applies everywhere when it depends on context? |
| Trade-offs and limits | What does the advice cost: more files, more indirection, slower change in some other direction? When does it fail, and does the author say so? What simpler alternative did the author consider? |
| AI-enabled systems | Which assumptions break when part of the system is a model or a data pipeline: repeatable outputs, requirements that are exact, code that changes only when someone edits it? Which of the book's techniques still help (boundaries, test doubles, seams, flags), and what do they leave out? Appendix F works one example of software around a model |
| Concrete examples | Which piece of code or project decision shows the advice working or failing? |
| Additional sources | What independent source, a study, a competing view or a standard, supports or challenges the claim? |

### Test the advice on code you can run

The lending project is a small, checked system. Pick one claim from your book and apply it. For a claim about interfaces, look at `NotificationSender` (Chapter 6). For a claim about small classes and responsibilities, look at the coordinator before and after Chapter 5. For a claim about patterns, compare a Strategy with the plain conditional it replaces (Chapter 9). For a claim about legacy code, use the characterisation tests of Chapter 11. For a claim about delivery, use the pipeline of Chapter 13. Then write what you saw: where the advice simplified the code, and where it added weight. A concrete case, honestly examined, is worth more than a catalogue of definitions.

### Check every source you cite

For each additional source, answer these before you rely on it:

1. Who wrote it, and what is their basis for the claim: a study, an experience report, an opinion?
2. Have you opened it yourself? Do not cite a source you have only seen quoted. If you are citing a summary, say so.
3. Does the source support the exact claim you make, and not a nearby one?
4. How old is it, and has the field moved?
5. Is it independent of the book, or does it repeat the author?
6. For a web page, have you recorded the address and the date you opened it?

Use short quotations only, in quotation marks, with the location. Put the rest in your own words.

### A suggested plan

The descriptor sets the deadline and nothing else. This plan is a suggestion for a part-time reader:

| Weeks | Do |
|---|---|
| 1 and 2 | Choose a book from the approved list. Read its introduction and decide what its central claim is. Start the reading record |
| 3 to 5 | Read and record. Choose one claim to test on the lending project |
| 5 and 6 | Run the test on the code; write down what you saw. Find and open your additional sources |
| 7 | Draft. Check every claim against your record. Check the word count and the references |
| 8 | Read the rubric once more, correct, and submit |

### AI tools and the review

An AI summary of a book you have not read is not evidence about that book, and a critique built from one will repeat what the summary left out. Whether and how you may use an AI tool for this assignment is set by your module's rules, which apply here. If you are allowed to use one and do, Chapter 15 shows how to record what it was asked, what it returned and what you checked; the record format of Appendix C is one way to do that.

## E.3 A reading record, filled in

The entries below are **constructed to illustrate**. The claim is invented for the exercise and is not a quotation from any book. The book, chapter and page are shown as fields for you to fill in with your own.

**Book:** *your chosen book*  **Chapter and page:** *your chapter and page*  **Date:** *date you read it*

| Entry | Record |
|---|---|
| Claim and location | *(Constructed claim.)* “Every collaborator of a class should be reached through an interface.” Location: *[chapter and page in your book]* |
| Context | The author is arguing about code that changes often and is replaced in tests. The assumption is that more than one implementation will exist |
| Supporting example | The author replaces a concrete sender with an interface so a test can supply a recorder, and the test becomes simple |
| Limitation | For a class with exactly one implementation and no test that needs a substitute, the interface adds a file and a name and removes nothing. The author does not say when to stop |
| Project application | `BorrowingPolicy` has a student and a staff implementation and `NotificationSender` has test substitutes, so the interface earns its place in both (Chapters 5 and 6). `LoanPeriod` has one, and an interface for it would add nothing |
| Further evidence | *To find:* an independent source on the cost of premature abstraction; the description of the over-abstraction cost in Chapter 6, Section 6.7, is a starting point and is not independent evidence |
| Who said what | Claim: the author. Application to the lending project: my inference. Search terms for further evidence: suggested by a tool, then checked by me |

## E.4 Evidence of individual contribution

The descriptor says that individual contribution on the project is assessed through commits, pull-request reviews and peer evaluation, and that the marks for the final project are moderated by individual contribution. Each of those is an input. None of them is the answer, and this book never ranks people by counts. Chapter 14, Section 14.5 explains why; this section shows how to gather evidence that does the job.

### What each kind of evidence can and cannot show

| Evidence | What it can show | What it cannot show |
|---|---|---|
| Commits | That a change was made, by which author identity, when, and what it touched | Effort, difficulty or importance. Size is a habit. Pair work is recorded under one author unless the other is named in a `Co-authored-by` line [2]. Formatting and regenerated files inflate counts. A squash merge turns many commits into one |
| Pull-request reviews | That someone read a change and what they said. A review can be a comment, an approval or a request for changes [3] | Whether the review was careful. An approval says the changes look ready to merge, and nothing about how thoroughly they were checked |
| Peer evaluation | How teammates experienced each other's work, including what no tool records | Objectivity. It is affected by friendship, conflict and what people happened to see |

A contribution count can also be wrong for a plain reason. A commit appears in a person's contribution graph only when its author address is linked to their account, and only when it is on the default branch or reaches it through a merged pull request. Commits made in a fork do not count until they are merged [1]. A person whose commits carry the wrong address can appear to have done nothing.

### Counts describe habits

Chapter 14 gives a constructed team of three. Its last iteration finished with these figures:

| | Commits | Of which formatting only | Lines changed | Reviews given | Reviews that asked for changes |
|---|---|---|---|---|---|
| P1 | 38 | 17 | 410 | 4 | 1 |
| P2 | 9 | 0 | 1,150 | 11 | 5 |
| P3 | 24 | 3 | 620 | 7 | 0 |

Ranked by commits the order is P1, P3, P2. By lines changed it is P2, P3, P1; by reviews given, P2, P3, P1; by reviews that asked for changes, P2, P1, P3. Four rankings give three different orders. The numbers describe habits and the artefacts describe contributions. The honest use of a count is as a pointer to an artefact to read: “Why did P2 have so few commits?” is a question to ask, and the answer is in the diff and the review.

### Build an evidence index

Write your contribution as claims, each with evidence that a reader can open. A short index is more useful than a long list:

| Claim | Where to see it | What it shows | What it does not show | Who can confirm |
|---|---|---|---|---|
| *(what you did, in one sentence)* | *(a pull request, a file, a test, a review comment, a decision record)* | *(the part of the claim it supports)* | *(its limit)* | *(a teammate or the reviewer)* |

A constructed row, for the team above:

| Claim | Where to see it | What it shows | What it does not show | Who can confirm |
|---|---|---|---|---|
| P2 wrote the approval-file adapter and found two defects in review | The adapter's pull request and its review thread | The code, the nine commits behind it and the two comments that led to fixes | How much of the design came from discussion before the first commit | P1 and P3, who reviewed it |

Habits that make the index easy to write: name your co-author in the commit when you pair [2]; keep review comments and the replies to them; record decisions in decision records (Appendix C); note the work that leaves no commit, such as a design session or a debugging session, and who can confirm it. Peer evaluation is collected as your module sets it. When you give one, say what you saw and where, and keep to the work.

## E.5 The final handover and submission

The descriptor says that teams submit and present the complete system built across the sprints, together with a short technical report and an individual reflection. Each team gives a demonstration and a presentation followed by questions. The submission is made through Moodle as a repository link, the technical report and the individual reflection. The demonstrations and the final submission fall in Weeks 15 and 16. Week 13 is the final sprint, the retrospective, polish and the handover, and Week 14 has no classes. Follow the dates your module leader publishes.

### What the submission must show

The descriptor says the submission must show clean object-oriented design, justified use of design patterns and architecture, automated tests with continuous integration, evidence of safe refactoring, and adaptability to the injected change in requirements. Use those five phrases as the headings of an **evidence index** for your own team. For each, name the evidence a reader can open and say what it does not show. Chapter 14, Section 14.6 gives the index for the book's project as a model.

| The submission must show | Evidence to point at | What it may not show |
|---|---|---|
| Clean object-oriented design | Your responsibilities, dependencies and architecture checks | That it is the best design, or that anyone else reviewed it |
| Justified patterns and architecture | Your decision records, with alternatives considered | A pattern that you did not use |
| Automated tests with CI | Your test suite and pipeline; a run you can link to | A hosted run that has never happened; a workflow file is not a run |
| Evidence of safe refactoring | Characterisation tests, small steps, a record of what you ran | Behaviour on inputs your tests did not produce |
| Adaptability to the change | The footprint of the change, the tests that pin it and the requirements table | That the rule you implemented is the right policy |

### The handover bundle

A handover is the material that lets someone else set the project up, trust what it says and understand who did what. Chapter 14, Section 14.3 describes six documents, each answering a different question:

| Document | The question it answers | A template |
|---|---|---|
| `README.md` | What is this, and where do I start? | |
| `docs/HANDOVER.md` | How do I set it up, run it and understand it in an hour? | |
| `docs/REQUIREMENTS-TO-EVIDENCE.md` | Which test checks each requirement? | C.10 |
| `docs/KNOWN-ISSUES.md` | What is wrong or missing, and what was decided? | C.10 |
| `docs/ADR-0NN-*.md` | Why is it built this way? | C.5 |
| `docs/RELEASE-NOTES-*.md` | What changed in this version? | C.11 |

Keep each document true by a check wherever you can: the book's project has a test that fails when a name in the requirements table disappears, and a script that follows the handover in a fresh copy and compares what it finds with what the document promises (Chapter 14, Sections 14.3 and 14.4). A script can check that a name exists; only a reviewer can check that it is the right evidence. Then ask someone outside your team to follow the handover while you watch and say nothing, and write down every place they hesitate.

### A sequence

1. **Week 13.** Finish. Run the retrospective (C.12) and decide what the handover must say.
2. **Freeze.** Agree a time after which only fixes to the handover and blockers are allowed. Run your handover check on the frozen version.
3. **Week 14.** There are no classes. Review the whole bundle as a stranger would, fix what the dry run finds, and ask someone outside the team to follow it.
4. **Before Weeks 15 and 16.** Prepare the demonstration and the report from the evidence index, and write your reflection from your own artefacts.

The descriptor does not prescribe the format or length of the technical report. Follow the assignment brief. The evidence index above is a sound spine for it.

## E.6 The individual reflection

The descriptor lists an individual reflection among the items submitted with the final project and does not give its length or format. Your assignment brief does. What follows are prompts for thinking, taken from Chapter 14, Section 14.5, and are not a rubric.

| Part | Prompts |
|---|---|
| What I did | Three to five specific pieces of work, each with a link or path: a pull request, a file, a test, a review comment |
| What I decided | A design or process decision, the alternatives and why |
| What went wrong and what I did about it | A real fault or misjudgement, how it was found, the fix and what changed afterwards |
| How I used AI | Where, with what input, what you accepted or rejected and how you verified it |
| What I did not do | Honest limits: work you started and did not finish, work you relied on others for |
| What I would change | One thing about your own practice |

A reflection makes claims and gives the evidence for each. It does not say “I did a lot.” A constructed excerpt, for the team of Section E.4, shows the habit. It is invented and it is not a model to copy:

> *(Constructed.)* I wrote the approval-file adapter. The pull request and its review thread are the evidence: nine commits, and two review comments from a teammate that changed my code. The first was that a row with an unknown status must be an operational failure and not a rejection; I had treated it as a rejection, which would have let a damaged register look like a sponsor's “no”. I changed the adapter and added a test for the damaged row. I did not write the pipeline script; P1 did, and I relied on it without reading it closely. Next time I will read the scripts that gate my own work.

Notice what is in it: a named artefact, a specific fault and how it was found, what changed, and an honest limit. Notice also what is not in it: any count.

## E.7 Sources

1. GitHub Docs, [Why are my contributions not showing up on my profile?](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-contribution-settings-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile). The author email, the default branch and the fork conditions for a commit to count.
2. GitHub Docs, [Creating a commit with multiple authors](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors). The `Co-authored-by` trailer.
3. GitHub Docs, [About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews). A review can be a comment, an approval or a request for changes.

All three were opened on 13 October 2026. The module descriptor is the source for the assessments, deadlines and submission described in E.1, E.4 and E.5. Chapters 1, 9 and 14 are the source for the reading record, the reading checkpoint, the contribution table, the handover documents and the reflection prompts.
