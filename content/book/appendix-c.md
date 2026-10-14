---
title: "Appendix C: Engineering Templates"
description: "Thirteen templates that follow the chapters' own records, each with a purpose, a blank form, a worked example and the usual mistakes, and a script that checks their structure."
weight: 230
---

*OO Development and Agile Practices*  
*Designing, Testing and Evolving Software with AI Assistance*

*OO Development and Agile Practices*  
*Designing, Testing and Evolving Software with AI Assistance*

## How to use this appendix

A template is a set of questions that a team agrees to answer every time. It saves you from forgetting the question that matters at the moment you are tired. It is not evidence. A story card with every field filled in shows that someone wrote down a story, a retrospective form shows that a meeting was held, and neither shows that the story was understood or that anything changed afterwards. The Chapter 3 companion says it plainly: a template is not evidence that a review occurred.

This appendix collects the thirteen templates that the chapters use, in the order you will meet them. Each section gives the purpose of the template, when to use it, the blank template, a small worked example and the mistakes to avoid. The examples are **constructed to illustrate**. They belong to an invented team and are labelled as such in the first line of the file. They are not real evidence, and you should not copy their contents into your own record.

Your approved instructions say what your module requires. The templates add no assessment requirement. If your instructions name a different form, use that form; the questions in these templates will still help you fill it in.

The Appendix C companion lists the same 26 files, each under its path, together with a small script that checks the structure of a filled-in template, the experiments that show what it catches, the answers to the activity in C.15 and notes for instructors. Each template and each example in this appendix is introduced by its path. Saved at those paths, the 26 blocks and the script form the kit that the script checks.

Each template uses the headings of the record that the chapters themselves use, so a document made from it follows the chapter that introduced it. A decision record has the headings of the project's ADR-010, ADR-013 and ADR-014, and the AI assistance record has the eight headings that the Chapter 15 lab checks. The script accepts those records unchanged.

## C.1 Using a template well

1. **Start from the question, not from the form.** Decide what the document must let a stranger do (re-run a check, understand a choice, find the evidence), and write for that person.
2. **Replace every `{{placeholder}}`.** A placeholder left in a document is a promise you did not keep. The script in the companion looks for them.
3. **Write “none yet” rather than invent.** An empty evidence field is honest. A made-up run address or review comment is not. Say what is missing and what the next action is.
4. **Keep the headings.** Other people and the script find things by heading. Add a heading if you need one; do not rename or delete one.
5. **Say what is constructed.** An example, a sample or a model answer is labelled as one, as the examples here are.
6. **Keep it with the work.** A template filled in and left in a chat message is lost. Commit it beside the code it describes, so that a change to one prompts a change to the other.

A script can check the shape of a filled-in template. It cannot check that the content is true.

| The script can check | Only a reviewer can check |
|---|---|
| Every required heading is present | That the answer under it is correct |
| No heading is empty | That “reviewed and verified” describes a real review |
| No `{{placeholder}}` is left | That the evidence named is the right evidence |
| An example is labelled as constructed | That a hosted run, a reviewer or a date exists |

## C.2 Story card

**Purpose.** A story card records one piece of value for one kind of user, with its boundaries, so that two people reading it expect the same thing. **Use it** when you refine a backlog item (Chapter 3), and again when the item is finished, to add the evidence.

Save as `templates/story-card.md`:

```markdown
# {{ID}}: {{short outcome}}

## Actor and value
{{Who needs this, and why. One or two sentences.}}

## Scope
{{What this item includes, and the boundary of the demonstration.}}

## Rules and assumptions
{{Confirmed decisions first. Then assumptions, each marked as temporary.}}

## Acceptance examples
{{Inputs, action, expected result and state effects. Link each to its acceptance-example file.}}

## Current support
{{Existing code or evidence, or "none".}}

## Dependencies and questions
{{Blocking decisions, related items, and who follows them up.}}

## Estimate
{{Optional: a relative size, its assumptions and the date it was discussed.}}

## Completion evidence
{{Links or notes for checks, review, integration and demonstration. Say "not started" until something exists.}}
```

Save as `examples/story-card.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# US-02: Inspect availability without reserving

## Actor and value
As an equipment officer, I want to see whether one item is free for a stated period, so that I can discuss a possible reservation without creating one.

## Scope
One item and one period per enquiry. No reservation is created or changed. Searching several items at once is outside this item.

## Rules and assumptions
Confirmed: a period includes its start day and excludes its end day (Chapter 2). Assumption, to be confirmed with the officer: whether a damaged item should appear available is a separate story, not this one.

## Acceptance examples
AQ-01 an empty store reports the item available. AQ-02 an overlapping reservation reports it unavailable. AQ-03 an adjacent reservation does not block it. AQ-04 another item's reservation does not block it. AQ-05 equal or reversed dates are reported as an invalid period. Every enquiry leaves the stored reservations unchanged.

## Current support
None. The only operation today is `reserve`, which stores a record.

## Dependencies and questions
How an invalid period is reported (an exception or a result value) must be decided before building. Owner: the pair that refines this item.

## Estimate
Medium, assuming no catalogue lookup. Discussed at the planning meeting.

## Completion evidence
Not started. The evidence will be the acceptance checks, a review note and the passing run on the integrated revision.
```

**Common mistakes.** Writing the story as a feature name with no actor and no value. Listing rules as if all were confirmed when some are guesses (separate them, as the example does). Filling in “Completion evidence” before anything exists. Marking a story done because the code exists, without the evidence the team agreed.

## C.3 Acceptance example

**Purpose.** An acceptance example turns a criterion into one concrete case that two people can check the same way. It names the observation and the state that must remain unchanged. **Use it** for each important criterion of a story (Chapter 3), including rejection paths.

Save as `templates/acceptance-example.md`:

```markdown
# {{AC-ID}}: {{the criterion in one sentence}}

## Given
{{The starting state, with concrete values.}}

## When
{{The one action, with concrete values.}}

## Then
{{What the caller observes: a result, a message or an error.}}

## State afterwards
{{What stored data must be unchanged or changed. Write "unchanged" when it is.}}

## Evidence
{{The check that runs this example, and the run that executed it.}}
```

Save as `examples/acceptance-example.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# AC-02: An overlapping request is rejected and changes nothing

## Given
CAM1 is reserved for B1 from 20 October to 22 October (start included, end excluded).

## When
B2 requests CAM1 from 21 October for one day.

## Then
The request is rejected as unavailable.

## State afterwards
The original reservation is the only stored record. Nothing was added or changed.

## Evidence
The AC-02 check in `Chapter03AcceptanceExamples`, and the run of the check script that printed it.
```

**Common mistakes.** Describing only the visible result and not the state afterwards: a program that prints the right rejection and still stores a record has not met the criterion. Using vague values (“a long period”) instead of concrete dates. Putting two actions in “When”. Pointing “Evidence” at a check that does not run this example.

## C.4 Definition of Done

**Purpose.** A Definition of Done is the quality standard that every increment must meet, whatever the story. It differs from acceptance criteria, which belong to one story, and from a Ready policy, which says when work may start. The Scrum Guide makes the Definition of Done a commitment attached to the increment [1]. **Use it** from the first iteration (Chapters 3 and 4), and extend it when the team gains a check, such as an automated gate.

Save as `templates/definition-of-done.md`:

```markdown
# Definition of Done: {{team or project}}

## Applies to
{{What counts as an increment, and the version or date of this definition.}}

## Conditions
1. {{A condition that another person could check.}}
2. {{Another condition.}}

## Not covered
{{What meeting this definition does not promise.}}

## Ready policy
{{Optional: what the team needs to know before it starts an item.}}

## Agreement and review
{{Who agreed it, when, and what would make the team revisit it.}}
```

Save as `examples/definition-of-done.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# Definition of Done: equipment lending team

## Applies to
Each increment of the controlled teaching baseline, from the first iteration.

## Conditions
1. The relevant acceptance examples have been checked, including the important rejection paths and the state effects.
2. The code compiles and runs with the documented commands in the agreed environment.
3. Another team member has reviewed the change, and findings that block acceptance are resolved.
4. The work is integrated into the shared codebase, and the existing checks still pass.
5. Usage notes, domain decisions and known limitations are current.
6. Another team member can repeat the demonstration within its stated scope.
7. The agreed automated check has passed on the integrated revision, and the team can find its result.

## Not covered
Approval by a product owner, performance, and any grading rule of the module. Condition 7 applies only from the day the automated check exists.

## Ready policy
An item is ready to start when its scope, its example inputs and any blocking question are written down. It is a conversation aid, not an extra gate.

## Agreement and review
Proposed by the team for the controlled increment. Revisit it when the automated check or the review practice changes.
```

**Common mistakes.** Listing conditions nobody could check (“good quality”). Claiming a condition that does not exist yet, such as a passing pipeline before there is one; the example says when condition 7 starts to apply. Weakening the definition to move a card across the board. Treating a team's definition as a grading policy.

## C.5 Decision record

**Purpose.** A decision record captures a decision and the reasons for it, not a description of the code. Nygard proposes short numbered records kept in the repository, with a title, context, decision, status and consequences, and says that a reversed decision is kept and marked superseded, not deleted [2]. The project's records add alternatives considered, how the decision was validated and what would reopen it. **Use it** whenever a choice will be hard to explain later: the storage choice at kickoff (Chapter 4), the application structure (Chapter 10), the visitor flag (Chapters 13 and 14).

Save as `templates/decision-record.md`:

```markdown
# ADR-{{NNN}}: {{the question and the choice}}

Date: {{date}}
Status: {{proposed, accepted, or superseded by ADR-NNN}}

## Context
{{The forces at play: the problem, the constraints, and what must not change.}}

## Decision
{{What was decided, in full sentences.}}

## Alternatives considered
- {{An alternative, and why it was not chosen.}}

## Consequences
{{What becomes easier, what becomes harder, and what is still unsolved.}}

## Validation and review
{{How the decision was checked, and by whom. Do not claim a review that did not happen.}}

## Revisit triggers
{{The conditions that would reopen this decision.}}
```

Save as `examples/decision-record.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# ADR-002: Keep reservations in memory for the kickoff baseline

Date: 13 October 2026
Status: Accepted for the kickoff baseline.

## Context
The kickoff demonstration judges reservation decisions in one session. The team has no storage requirement yet, and adding a database would hide the rules under test.

## Decision
Keep one in-memory coordinator. A restart loses every record, and identifiers start again from the beginning.

## Alternatives considered
- A file or database store: it would survive a restart, but no selected outcome needs that, and it adds setup and failure cases.
- Do nothing explicit: the behaviour would be a surprise to the first user who restarts the program.

## Consequences
The demonstration is simple and fast to run. The officer must be told that records do not persist. Any story that needs a restart to keep data will need a new decision record that supersedes this one.

## Validation and review
Discussed at the team meeting. No independent review has taken place.

## Revisit triggers
A selected outcome requires a session to survive a restart, or two users need the same data at once.
```

The numbers in the examples belong to the example team. They are not the book's project's ADR-010, ADR-013 and ADR-014. Once a record is accepted, change only its status. A new decision gets a new record that says which one it supersedes.

**A smaller form.** For a small choice, such as accepting or rejecting a proposed criterion, a one-row table can be enough:

| Proposal | Accept, reject or clarify | Reason and evidence | Follow-up or related item |
|---|---|---|---|
| Treat an enquiry as read-only | Accept | An enquiry must not create a record (AC for US-02) | Add AQ-05 for equal dates |

The check script covers the full record and not this table.

**Common mistakes.** Recording a decision after the fact without saying so. Editing an old record to match what happened. Listing only the option that was chosen. Writing “reviewed” under validation when nobody reviewed it.

## C.6 Iteration plan

**Purpose.** An iteration plan makes capacity visible next to the work, so that the team plans what it can verify and not what it hopes. It shows the goal, the hours available, the forecast and what would make the team replan. **Use it** at the start of an iteration (Chapter 4).

Save as `templates/iteration-plan.md`:

```markdown
# Iteration plan: {{team}}, {{dates}}

## Iteration goal
{{One sentence naming an outcome a user could observe.}}

## Capacity
| Person | Hours available |
|---|---:|
| {{name or initials}} | {{hours}} |

Reserved for coordination, integration and administration: {{hours}}.
Planning budget: {{hours}}.

## Forecast work
| Work | Person-hours |
|---|---:|
| {{task}} | {{hours}} |

Selected work: {{total}}. Unallocated: {{budget minus selected work}}.

## Calendar and skill constraints
{{Who is available when, who knows what, and when the review can happen.}}

## When to replan
{{The evidence that would make the team change the forecast, and who decides.}}
```

Save as `examples/iteration-plan.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# Iteration plan: example team, next iteration

## Iteration goal
Let the officer inspect availability for one item and period without changing reservations.

## Capacity
| Person | Hours available |
|---|---:|
| P1 | 6 |
| P2 | 6 |
| P3 | 5 |
| P4 | 5 |

Reserved for coordination, integration and administration: 4.
Planning budget: 18 (22 available, less 4).

## Forecast work
| Work | Person-hours |
|---|---:|
| Resolve the query contract and update the examples | 2 |
| Implement the read-only enquiry | 4 |
| Add the thin interaction and the invalid-input response | 3 |
| Add and run the query checks beside the regression checks | 3 |
| Review, integrate, update notes and rehearse the demonstration | 2 |

Selected work: 14. Unallocated: 4, kept as room for uncertainty and not as a promise to add a feature.

## Calendar and skill constraints
Only P1 can explain the coordinator, and the reviewer is free only at the start. Hold an early pairing session on the query contract and agree a review window before the demonstration.

## When to replan
If an estimate rises by more than two hours, discuss the scope at the next meeting. Reduce an optional part before skipping a check. The team decides, and the product owner is told of any change to the goal.
```

The figures are invented for reasoning. They are not official contact hours and not measured productivity. Review and correction consume capacity, so they appear in the forecast; calling them “after development” does not make them free. A total that fits does not make the plan feasible, which is why the example names the constraints on people and time.

**Common mistakes.** Allocating every available hour to features. Converting story points into hours as if they were the same thing. Hiding an overrun by postponing checks. Treating the unallocated hours as a promise to add scope.

## C.7 Team agreement

**Purpose.** A team agreement answers the practical questions that otherwise become arguments: where requirements live, how work moves, who reviews, which check runs and what happens when evidence is unavailable. **Use it** when the team forms and revisit it at each retrospective (Chapter 4).

Save as `templates/team-agreement.md`:

```markdown
# Team agreement: {{team}}

## Where things live
{{Where requirements, questions, decisions and evidence are kept.}}

## How work moves
{{The board columns, the limit on work in progress, and what blocked work does.}}

## Branches and review
{{How big a branch may be, who reviews, and what a reviewer looks at.}}

## Checks
{{Which check the author runs, when, and where its result is recorded.}}

## Gaps and unavailable evidence
{{What the team does when a review or a hosted run is not available.}}

## Review of this agreement
{{When the team rereads this, and how a change is recorded.}}
```

Save as `examples/team-agreement.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# Team agreement: example team

## Where things live
Stories and acceptance examples are in the shared project notes, with their identifiers kept when the wording changes. Questions are raised in the team channel and copied to the story if they block it.

## How work moves
Backlog, Ready, Building, Review, Done. Building plus Review holds at most two items, and a blocked item counts.

## Branches and review
A branch is small enough that a reviewer can explain its purpose and effects. Reviewers inspect behaviour, state effects and evidence, not only style.

## Checks
The author runs the check script before review and again after corrections. The result on the integrated branch is recorded in the evidence note.

## Gaps and unavailable evidence
If a review or a hosted run is not available, the team writes the gap and a next action in the evidence note. It never writes an invented result.

## Review of this agreement
Reread at each retrospective. A change is recorded with its reason in the project notes.
```

A repository does not enforce a policy because a document requests it. Where the platform allows, configure the shared branch to require the agreed check and review; where it does not, say that the team follows a manual policy and keep the review evidence. Do not describe a requested policy as enforced unless it is.

**Common mistakes.** Copying another team's agreement without adapting it. Leaving the gaps section empty and then inventing a result when evidence is missing. Never rereading it.

## C.8 Pull-request description

**Purpose.** A pull request, or merge request, asks a hosting platform to bring one branch into another so that others can review it. It is not a commit. Its description tells the reviewer what to look at before they open the diff. **Use it** for every change you ask someone to review (Chapters 2 and 4, and B.8).

Save as `templates/pull-request.md`:

```markdown
# {{short title of the change}}

## Problem
{{What is wrong or missing, and for whom.}}

## Change
{{What this change does, and what it deliberately does not do.}}

## Checks run
{{The commands, the results, and where the output is kept.}}

## Review focus
{{What the reviewer should look at first, and why it is the risk.}}

## Limits
{{What the checks do not show, and what was not run.}}
```

Save as `examples/pull-request.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# Extract reservation confirmation formatting

## Problem
The request method mixes storing a reservation with assembling the confirmation text, so a change to the wording risks the storage.

## Change
Moves the text assembly into a private helper. The messages and the stored records are unchanged. It does not change any rule or any public method.

## Checks run
The check script before and after the change printed the same results. The output is attached to this request.

## Review focus
Confirm that the helper changes no state, and that the record is still added before the confirmation is returned.

## Limits
Only the supplied checks were run. No hosted check has run on this branch yet.
```

On GitHub, a file named `pull_request_template.md` in the repository fills the description of every new pull request with your headings [3]. Other platforms have their own equivalents.

**For the reviewer.** Start from the claimed behaviour, then trace the code or text that is supposed to deliver it, then ask whether the evidence supports the claim. “Looks good” does not say which risk was examined. “The helper changes no state, and the record is still stored before the confirmation is returned” does. Write what you inspected.

**Common mistakes.** A description that restates the diff. A change that mixes a functional change with a workflow change, which is hard to review. Quoting a check result that was not run on this revision. Inventing a review exchange to complete a milestone template: keep the real comments and the real response, or write that none exist.

## C.9 Evidence note

**Purpose.** An evidence note collects what the team can show, with the gaps visible, so that a reader can tell a result from a hope. **Use it** at each milestone (Chapter 4); the repository-metrics lab of Chapter 12 has its own record with different fields.

Save as `templates/evidence-note.md`:

```markdown
# Evidence note: {{team}}, {{date}}

## Repository and baseline revision
{{The repository and the exact revision this note describes.}}

## Implemented behaviour
{{Only the behaviour present at that revision.}}

## Local environment and command
{{The Java version, the shell, and the command that was run.}}

## Local check result
{{The observed exit status and the relevant output.}}

## Hosted passing run
{{The run address or retained log, the revision it tested, and the date. Or "none yet" and the next action.}}

## Deliberate failure
{{The practice revision, the failed assertion, and the failed run. Or "not done yet".}}

## Restored pass
{{The restored revision and its passing run. Or "not done yet".}}

## Independent review
{{The actual reviewer, the finding, the correction and the follow-up. Or "none yet".}}

## Unresolved questions
{{Each with an owner, its impact and the next decision point.}}

## Known limitations
{{Scope boundaries that matter for reading the demonstration.}}
```

Save as `examples/evidence-note.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# Evidence note: example team, week 2

## Repository and baseline revision
The team repository, at the revision tagged for the first iteration. The revision identifier is copied here when the note is committed.

## Implemented behaviour
US-01 only: an eligible request for an available item creates one stored reservation. No availability enquiry exists yet.

## Local environment and command
A full JDK of version 17 or later, Git Bash, and `bash scripts/check.sh`.

## Local check result
Exit status 0, ending with the success line of the script. Output saved with this note.

## Hosted passing run
None yet. The workflow file is in the repository but has not run. Next action: push the branch, open the run page, and keep its address and the tested revision.

## Deliberate failure
Not done yet. Planned for the next meeting on a practice branch.

## Restored pass
Not done yet.

## Independent review
None yet. A self-review was written for practice and is labelled as a self-review.

## Unresolved questions
How an invalid period is reported (owner: P2; decide before US-02 is built). Who may cancel a reservation (owner: product owner; blocks a later item).

## Known limitations
Records live in memory and vanish on restart. Requests are handled one at a time.
```

Look at the example's hosted-run field. It says “none yet” and gives the next action. That is the right way to record a gap. A passing workflow file in the repository is not a passing run, and a hosted run you did not do cannot be written down.

**Common mistakes.** Writing the planned behaviour as if it were implemented. Citing the check result of one revision for another. Copying an example's “restored pass” into a note when no failure was ever introduced. Leaving the template's guidance text in place of an answer.

## C.10 Requirements to evidence, and known issues

**Purpose.** Two tables carry a project through a handover (Chapter 14). The **requirements-to-evidence** table follows each requirement to the class that decides it and the test that checks it, so that a reviewer can find the evidence. The **known-issues** list says what is wrong or missing and, for each row, what was decided. **Use them** when you prepare a release and when you hand a project to someone else.

Save as `templates/requirements-to-evidence.md`:

```markdown
# Requirements to evidence: {{project}}

## Table
| Requirement or example | Class that decides it | Test that checks it | Stage that runs it |
|---|---|---|---|
| {{ID and one line}} | {{class}} | {{test class and method}} | {{script or pipeline stage}} |

## How this table is kept true
{{The script or test that fails when a name in the table no longer exists.}}

## What this table cannot show
{{For example: that a named test is the right test for its requirement.}}
```

Save as `examples/requirements-to-evidence.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# Requirements to evidence: example project

## Table
| Requirement or example | Class that decides it | Test that checks it | Stage that runs it |
|---|---|---|---|
| AC-01 an eligible request creates one reservation | `ReservationCoordinator` | `Chapter03AcceptanceExamples`, AC-01 | `scripts/check.sh` |
| AC-02 an overlapping request is rejected and changes nothing | `ReservationCoordinator`, `LoanPeriod` | `Chapter03AcceptanceExamples`, AC-02 | `scripts/check.sh` |

## How this table is kept true
A reviewer reads it at each release. A script that fails when a named class or test disappears is planned and does not exist yet.

## What this table cannot show
That each named test is the right evidence for its requirement. A name can exist and still check the wrong thing; only a reviewer can judge that.
```

Save as `templates/known-issues.md`:

```markdown
# Known issues: {{project}}

## Issues
| ID | What is wrong or missing | Effect | Decision | Owner | Review trigger |
|---|---|---|---|---|---|
| {{KI-n}} | {{description}} | {{who is affected, how}} | {{fix, accept or defer, and why}} | {{name}} | {{what would reopen it}} |

## How this list is kept true
{{Who reads it, and when. Every row needs a decision, not only a description.}}
```

Save as `examples/known-issues.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# Known issues: example project

## Issues
| ID | What is wrong or missing | Effect | Decision | Owner | Review trigger |
|---|---|---|---|---|---|
| KI-1 | Reservations are kept in memory | A restart loses every record | Accept for the kickoff baseline (ADR-002) | P1 | A story needs data to survive a restart |
| KI-2 | The hosted workflow has never run | No hosted result exists for any revision | Defer until the team pushes to a hosted repository | P3 | The first push to the hosted repository |

## How this list is kept true
Read by the team at each retrospective. A row without a decision is not finished.
```

A table that was true once rots. The cheapest way to keep a statement true is a script that fails when it stops being true, as the book's project's traceability test does. Even then, a script can check that a named test exists; only a reviewer can check that it is the right test. The example says so.

**Common mistakes.** A known-issues row with a description and no decision. Listing a test that exists but checks something else. Deleting a known issue to make the list shorter instead of resolving it.

## C.11 Release notes

**Purpose.** Release notes tell a person what changed in a version. Keep a Changelog groups changes as Added, Changed, Deprecated, Removed, Fixed and Security, gives each version its own dated entry and puts the newest first [4]. The template keeps three of those headings and adds two that a handover needs: behaviour a reader could misread, and what was not verified. **Use it** at each release (Chapter 14).

Save as `templates/release-notes.md`:

```markdown
# Release notes {{version}}

Date: {{date}}

## Summary
{{One or two sentences. Say whether production behaviour changed.}}

## Added
{{New behaviour, or "nothing".}}

## Changed
{{Changed behaviour, or "nothing".}}

## Fixed
{{Defects fixed, or "nothing".}}

## Behaviour you should know about
{{Behaviour a user or a maintainer could misread.}}

## Not verified
{{What was not run or not checked for this version.}}
```

Save as `examples/release-notes.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# Release notes 0.2.0

Date: 20 October 2026

## Summary
Adds a read-only availability enquiry. The existing reservation behaviour is unchanged.

## Added
An enquiry that reports whether one item is free for a stated period, without creating a reservation.

## Changed
Nothing.

## Fixed
Nothing.

## Behaviour you should know about
An item can be reported available even when a borrower cannot reserve it, because that borrower has reached the limit. Availability and eligibility are separate questions.

## Not verified
No hosted run of the workflow exists for this version. Behaviour on a Java 17 runtime was not run.
```

Add a heading for Deprecated, Removed or Security when a release has such a change. One file per version, written at the release.

**Common mistakes.** A summary that says “various improvements”. Saying production behaviour did not change without checking. Leaving “Not verified” empty because nothing seemed missing.

## C.12 Retrospective

**Purpose.** A retrospective plans ways to increase quality and effectiveness. The Scrum Guide describes the team inspecting how the last sprint went with regard to individuals, interactions, processes, tools and its Definition of Done, and identifying the most helpful changes [1]. Make it about evidence and not mood: for each thing the team wants to say, ask which artefact shows it. **Use it** at the end of each iteration (Chapter 14).

Save as `templates/retrospective.md`:

```markdown
# Retrospective: {{team}}, {{period}}

## Period and evidence brought
{{The dates, and the artefacts the team brought: board, runs, reviews, defects.}}

## What the evidence shows
| Observation | Evidence | Action | Owner and date |
|---|---|---|---|
| {{what the team says}} | {{the artefact that shows it}} | {{one change}} | {{name, next iteration}} |

## Process note
{{Which adaptations of the process helped, which hurt, and what to change.}}

## Actions agreed
{{At most three, each with an owner and a date.}}

## Last retrospective's actions
{{What happened to each action agreed last time.}}
```

Save as `examples/retrospective.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# Retrospective: example team, first iteration

## Period and evidence brought
The first iteration. The team brought the board with its timestamps, the list of check runs and the review comments.

## What the evidence shows
| Observation | Evidence | Action | Owner and date |
|---|---|---|---|
| Reviews were slow | Two requests waited more than two days (board timestamps) | Review before starting a new item | P2, next iteration |
| The checks were unreliable | One of ten runs failed with no code change (run list) | Find and fix or isolate the unstable check | P3, next iteration |
| We rushed the end | Seven items moved to Done on the last day | Plan a smaller scope and freeze two days before the demonstration | Whole team |

## Process note
Our iterations end at the module's milestone weeks, not at a fixed interval. That helped us plan to a real date and hurt when the milestone fell in a short week. Next time we plan the short week with a smaller scope.

## Actions agreed
1. Review before starting a new item (P2, next iteration). 2. Fix or isolate the unstable check (P3, next iteration). 3. Plan a freeze two days before the demonstration (whole team).

## Last retrospective's actions
None. This was the first retrospective.
```

Keep the number of actions small. Two actions with owners that get done are worth more than ten that do not. The process note closes the commitment from Chapter 3: say which adaptations of the process helped, which hurt and what you would change. The last field makes the team look at what became of last time's actions, which is where most retrospectives fail.

**Common mistakes.** An observation with no evidence. Actions with no owner or no date. Naming a person as the cause of a problem; look at the work and the process, not at blame.

## C.13 AI assistance record

**Purpose.** An AI assistance record says what was asked, what was received, what was accepted or rejected, and what checks were run, so that a reader can judge the result without trusting it. **Use it** whenever an assistant contributes something you will rely on (Chapter 15). The lab in Chapter 15 supplies a script that checks the same eight headings.

Save as `templates/ai-assistance-record.md`:

```markdown
# AI assistance record: {{task}}

## Task
{{What was asked, in one or two sentences, and who owns the requirement.}}

## Tool and model
{{The tool and model, or "none: constructed example", and the date. If no tool was available, how the exercise was done instead.}}

## Context given
{{What the assistant was shown, and what was left out and why. No secrets or personal data.}}

## Output received
{{Each candidate in order, marked accepted or rejected. Keep the rejected ones.}}

## Decision
{{What was accepted or rejected, and the reason for each.}}

## Changes made
{{What you changed by hand, and why.}}

## Verification
{{The checks, the commands, the results and the date. Say which checks are independent of the assistant.}}

## Limits
{{What the verification does not show, and what was not run.}}
```

Save as `examples/ai-assistance-record.md`:

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# AI assistance record: explain the overlap rule

## Task
Ask for an explanation of `LoanPeriod.overlaps`, so that a teammate can review it. The developer owns the rule: a period includes its start and excludes its end.

## Tool and model
None: constructed example. The candidate below was written by the author of this example and stands in for an assistant's answer.

## Context given
The source of `LoanPeriod` and one sentence about the half-open convention. The existing checks were not shown, so that they could be used to judge the answer.

## Output received
1. Candidate explanation: **rejected**. It said two periods overlap when the first one's end is on or after the second one's start, so adjacent periods overlap.

## Decision
Rejected. The sentence contradicts the convention that an end day is excluded.

## Changes made
Wrote the explanation by hand from the code: two periods overlap only when each starts before the other ends.

## Verification
Traced the periods 20 to 22 October and 22 to 24 October by hand: they do not overlap. Ran the Appendix A lab, whose check that adjacent periods do not overlap passes. Independent of the assistant: the hand trace and the lab check.

## Limits
Only the overlap rule was checked, on a few dates. Nothing here shows that the explanation covers every case.
```

Keep the rejected output. Say which checks are independent of the assistant, such as the compiler, a hand trace and examples written beforehand. A second assistant's opinion is not verification. A record that says only “reviewed and verified” is the ritual version; the useful one says what was run, with what result, and what remains unchecked.

**Common mistakes.** Writing the record after the details are forgotten. Leaving out the context, so that nobody can tell what the assistant saw. Including secrets or personal data. Treating a passing check as proof of more than it covers.

## C.14 What is not here

The individual reflection and the guide to contribution evidence belong to Appendix E (E.4 to E.6). The record for the repository-metrics lab and the change specification used in Chapter 13 are in Chapter 12, where their fields are explained. The handover documents (the README and the setup document) are specific to a project and are described in Chapter 14.

## C.15 A short verification activity

Do these in a copy of the kit, in a throwaway folder.

1. In a copy of the kit from the companion, run `bash scripts/check-templates.sh`. It should end with a pass for all 26 files.
2. Copy `templates/pull-request.md` to a new file and fill it in for a real change you made. Run `bash scripts/check-templates.sh --file pull-request YOUR-FILE`. Fix whatever it reports.
3. Break your file three ways, one at a time: delete a heading, empty a section, leave a `{{placeholder}}`. Note what the script says each time, then restore it.
4. Choose one template from this appendix that your team does not yet use and say, in two sentences, what question it would force you to answer.
5. Fill in an evidence note for your own team, writing “none yet” where something does not exist.

**Optional AI activity, with an identical offline route.** The companion lists a complete evidence note that an assistant might produce when asked to “fill in the template”. It is author-constructed, not a captured model response. Its key entries read:

> Hosted passing run: run 1432, passed on revision a3f9c21 on 12 October. Independent review: reviewed and approved by the team. Deliberate failure: introduced and fixed, all checks green. Known limitations: none.

Run the script on it. Does it pass? Which entries could a reviewer verify, and how? Which entries look like inventions? A live assistant may produce a different candidate if your course allows one, but it is not required. Record the claim, your check and your conclusion. What you hand in at the end is your filled note; it adds no assessment requirement.

## Sources and further reading

Opened on 13 October 2026. The explanations, templates and examples are original; source text has not been reproduced.

1. Schwaber, K. and Sutherland, J., [The Scrum Guide](https://scrumguides.org/scrum-guide.html), November 2020. The Definition of Done as a commitment of the increment; the purpose of the Sprint Retrospective.
2. Nygard, M., [Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions), 15 November 2011. Short numbered records: title, context, decision, status, consequences; superseded and not deleted.
3. GitHub Docs, [Creating a pull request template for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository). The `pull_request_template.md` file.
4. [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Changelogs for humans, the change types and the dated entry for each version.
