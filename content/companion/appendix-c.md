---
title: "Appendix C Companion: Template Kit and Checker"
weight: 230
description: "Code explanations and solutions for Appendix C Companion: Template Kit and Checker."
---

*Engineering Templates*  
*OO Development and Agile Practices*

## 1. Scope and use

This file accompanies Appendix C. It supplies a small, complete **template kit**: thirteen blank templates, thirteen worked examples and a script that checks the structure of a filled-in document. Each template uses the headings of the record that the chapters themselves use, so a document made from the kit follows the chapter that introduced it:

| Template | First used in | Follows |
|---|---|---|
| `story-card` | Chapter 3 | The story-card fields of the Chapter 3 companion |
| `acceptance-example` | Chapter 3 | The given, when, then form of Section 3.7 |
| `definition-of-done` | Chapters 3 and 4 | The proposed Definition of Done and its Chapter 4 extension |
| `decision-record` | Chapters 4, 10, 13, 14 | The headings of ADR-010, ADR-013 and ADR-014 |
| `iteration-plan` | Chapter 4 | The capacity and forecast tables of Section 4.4 |
| `team-agreement` | Chapter 4 | The team agreement of Section 4.5 |
| `pull-request` | Chapters 2 and 4 | The problem, change and checks of a review description |
| `evidence-note` | Chapter 4 | The evidence-note fields of the Chapter 4 companion |
| `requirements-to-evidence` | Chapter 14 | `docs/REQUIREMENTS-TO-EVIDENCE.md` |
| `known-issues` | Chapter 14 | `docs/KNOWN-ISSUES.md` |
| `release-notes` | Chapter 14 | `docs/RELEASE-NOTES-0.14.0.md` |
| `retrospective` | Chapter 14 | The observation, evidence, action and owner table of Section 14.5 |
| `ai-assistance-record` | Chapter 15 | The eight headings of Section 15.8, checked by the lab's `check-record.sh` |

The examples are **constructed to illustrate**. They belong to an invented team, are labelled as such in their first line and are not evidence of anything. Do not copy their contents into your own records.

Save every listing in Section 2 and Section 3 at its path inside one new folder, for example `template-kit`. Use Git Bash or a Linux or macOS terminal. No Java, Maven or network access is needed. From that folder:

```bash
bash scripts/check-templates.sh
```

### Using a template well

1. **Start from the question, not from the form.** Decide what the document must let a stranger do, such as re-run a check, understand a choice or find the evidence, and write for that person.
2. **Replace every `{{placeholder}}`.** A placeholder left in a document is a promise you did not keep.
3. **Write “none yet” rather than invent.** An empty evidence field is honest. A made-up run address or review comment is not. Say what is missing and what the next action is.
4. **Keep the headings.** Other people and the script find things by heading. Add a heading if you need one; do not rename or delete one.
5. **Say what is constructed.** An example, a sample or a model answer is labelled as one.
6. **Keep it with the work.** Commit the document beside the code it describes, so that a change to one prompts a change to the other.

| The script can check | Only a reviewer can check |
|---|---|
| Every required heading is present | That the answer under it is correct |
| No heading is empty | That “reviewed and verified” describes a real review |
| No `{{placeholder}}` is left | That the evidence named is the right evidence |
| An example is labelled as constructed | That a hosted run, a reviewer or a date exists |

## 2. The templates

### 2.1 `templates/story-card.md`

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

### 2.2 `templates/acceptance-example.md`

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

### 2.3 `templates/definition-of-done.md`

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

### 2.4 `templates/decision-record.md`

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

### 2.5 `templates/iteration-plan.md`

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

### 2.6 `templates/team-agreement.md`

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

### 2.7 `templates/pull-request.md`

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

### 2.8 `templates/evidence-note.md`

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

### 2.9 `templates/requirements-to-evidence.md`

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

### 2.10 `templates/known-issues.md`

```markdown
# Known issues: {{project}}

## Issues
| ID | What is wrong or missing | Effect | Decision | Owner | Review trigger |
|---|---|---|---|---|---|
| {{KI-n}} | {{description}} | {{who is affected, how}} | {{fix, accept or defer, and why}} | {{name}} | {{what would reopen it}} |

## How this list is kept true
{{Who reads it, and when. Every row needs a decision, not only a description.}}
```

### 2.11 `templates/release-notes.md`

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

### 2.12 `templates/retrospective.md`

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

### 2.13 `templates/ai-assistance-record.md`

```markdown
# AI assistance record: {{task}}

## Task
{{What was asked, in one or two sentences, and who owns the requirement.}}

## Tool and model
{{The tool and model, or "none: constructed fixture", and the date. If no tool was available, how the exercise was done instead.}}

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

## 3. The worked examples

### 3.1 `examples/story-card.md`

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

### 3.2 `examples/acceptance-example.md`

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

### 3.3 `examples/definition-of-done.md`

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

### 3.4 `examples/decision-record.md`

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

### 3.5 `examples/iteration-plan.md`

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

### 3.6 `examples/team-agreement.md`

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

### 3.7 `examples/pull-request.md`

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

### 3.8 `examples/evidence-note.md`

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

### 3.9 `examples/requirements-to-evidence.md`

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

### 3.10 `examples/known-issues.md`

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

### 3.11 `examples/release-notes.md`

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

### 3.12 `examples/retrospective.md`

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

### 3.13 `examples/ai-assistance-record.md`

```markdown
<!-- Example: constructed to illustrate. Not real evidence. -->
# AI assistance record: explain the overlap rule

## Task
Ask for an explanation of `LoanPeriod.overlaps`, so that a teammate can review it. The developer owns the rule: a period includes its start and excludes its end.

## Tool and model
None: constructed fixture. The candidate below was written by the author of this example and stands in for an assistant's answer.

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

## 4. The checker

### 4.1 `scripts/check-templates.sh`

```bash
#!/usr/bin/env bash
# Checks the structure of the template kit, or of one document you filled in.
#   bash scripts/check-templates.sh                      check every template and every example
#   bash scripts/check-templates.sh --file NAME PATH     check your own document against template NAME
# A template must keep every required heading and still show a {{placeholder}}. An example, or your own
# document, must have every required heading, a non-empty body under each, and no {{placeholder}} left.
# The script cannot tell whether what is written is true or useful; a reviewer does that.
# It fails, and says so, when there is nothing to check, so an empty set can never be reported as checked.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

NAMES=(story-card acceptance-example definition-of-done decision-record iteration-plan team-agreement
       pull-request evidence-note requirements-to-evidence known-issues release-notes retrospective
       ai-assistance-record)

# The required items of one template. "## X" is a heading; "X:" is a line that starts with X:.
required() {
  case "$1" in
    story-card) printf '%s\n' "## Actor and value" "## Scope" "## Rules and assumptions" "## Acceptance examples" \
      "## Current support" "## Dependencies and questions" "## Estimate" "## Completion evidence" ;;
    acceptance-example) printf '%s\n' "## Given" "## When" "## Then" "## State afterwards" "## Evidence" ;;
    definition-of-done) printf '%s\n' "## Applies to" "## Conditions" "## Not covered" "## Ready policy" "## Agreement and review" ;;
    decision-record) printf '%s\n' "Date:" "Status:" "## Context" "## Decision" "## Alternatives considered" \
      "## Consequences" "## Validation and review" "## Revisit triggers" ;;
    iteration-plan) printf '%s\n' "## Iteration goal" "## Capacity" "## Forecast work" \
      "## Calendar and skill constraints" "## When to replan" ;;
    team-agreement) printf '%s\n' "## Where things live" "## How work moves" "## Branches and review" "## Checks" \
      "## Gaps and unavailable evidence" "## Review of this agreement" ;;
    pull-request) printf '%s\n' "## Problem" "## Change" "## Checks run" "## Review focus" "## Limits" ;;
    evidence-note) printf '%s\n' "## Repository and baseline revision" "## Implemented behaviour" \
      "## Local environment and command" "## Local check result" "## Hosted passing run" "## Deliberate failure" \
      "## Restored pass" "## Independent review" "## Unresolved questions" "## Known limitations" ;;
    requirements-to-evidence) printf '%s\n' "## Table" "## How this table is kept true" "## What this table cannot show" ;;
    known-issues) printf '%s\n' "## Issues" "## How this list is kept true" ;;
    release-notes) printf '%s\n' "Date:" "## Summary" "## Added" "## Changed" "## Fixed" \
      "## Behaviour you should know about" "## Not verified" ;;
    retrospective) printf '%s\n' "## Period and evidence brought" "## What the evidence shows" "## Process note" \
      "## Actions agreed" "## Last retrospective's actions" ;;
    ai-assistance-record) printf '%s\n' "## Task" "## Tool and model" "## Context given" "## Output received" \
      "## Decision" "## Changes made" "## Verification" "## Limits" ;;
    *) return 1 ;;
  esac
}

problems=0
checked=0
fail() {
  echo "FAIL $*"
  problems=$((problems + 1))
}

# check_file KIND FILE NAME   (KIND is template, example or mine)
check_file() {
  local kind="$1" file="$2" name="$3" item body
  if [ ! -f "$file" ]; then
    fail "$file: no such file"
    return
  fi
  checked=$((checked + 1))
  while IFS= read -r item; do
    case "$item" in
      "## "*)
        if ! grep -qxF "$item" "$file"; then
          fail "$file: missing heading '${item#\#\# }'"
        elif [ "$kind" != template ]; then
          body="$(awk -v h="$item" '$0 == h {on=1; next} /^## / {on=0} on' "$file" | tr -d '[:space:]')"
          [ -n "$body" ] || fail "$file: heading '${item#\#\# }' is empty"
        fi
        ;;
      *:)
        if ! grep -q "^${item}" "$file"; then
          fail "$file: missing line '${item}'"
        elif [ "$kind" != template ] && ! grep -q "^${item} *[^ ]" "$file"; then
          fail "$file: '${item}' has no value"
        fi
        ;;
    esac
  done < <(required "$name")
  if [ "$kind" = template ]; then
    grep -q '{{' "$file" || fail "$file: a template must still show its {{placeholders}}"
  else
    ! grep -q '{{' "$file" || fail "$file: an unfilled {{placeholder}} is left"
  fi
  if [ "$kind" = example ]; then
    head -1 "$file" | grep -q '^<!-- Example: constructed to illustrate' || fail "$file: the first line must label it as a constructed example"
  fi
}

if [ "${1:-}" = "--file" ]; then
  [ "$#" -eq 3 ] || { echo "usage: check-templates.sh --file NAME PATH" >&2; exit 2; }
  required "$2" >/dev/null || { echo "unknown template name: $2" >&2; exit 2; }
  check_file mine "$3" "$2"
else
  for name in "${NAMES[@]}"; do
    check_file template "templates/${name}.md" "$name"
    check_file example "examples/${name}.md" "$name"
  done
fi

if [ "$checked" -eq 0 ]; then
  echo "FAIL nothing was checked"
  echo "TEMPLATE CHECK FAILED"
  exit 1
fi
if [ "$problems" -gt 0 ]; then
  echo "TEMPLATE CHECK FAILED: ${problems} problem(s) in ${checked} file(s)"
  exit 1
fi
echo "TEMPLATE CHECK PASSED: ${checked} file(s)"
```

The script has two modes. Without arguments it checks the whole kit: every template must keep its required headings and still show a `{{placeholder}}`; every example must have every heading, a non-empty body under each, no placeholder left and a first line that labels it as constructed. With `--file NAME PATH` it checks one document you filled in, against the headings of template `NAME`, without the label requirement:

```bash
bash scripts/check-templates.sh --file decision-record docs/ADR-015-example.md
```

It fails, and says so, when there is nothing to check, so an empty set can never be reported as checked. It cannot tell whether what is written is true.

Three checks against the book's own records, run in Git Bash on the files as printed in the chapter companions: ADR-010, ADR-013 and ADR-014 each pass `--file decision-record`, and the Chapter 15 lab's filled record `AI-RECORD-earliest-start.md` passes `--file ai-assistance-record`. That is what “follows the headings of the chapters” means in practice.

### 4.2 Expected output

```text
TEMPLATE CHECK PASSED: 26 file(s)
```

### 4.3 A small fault experiment

In a separate copy of the kit, make one change at a time, run `bash scripts/check-templates.sh` and discard the copy.

| Change | What must happen |
|---|---|
| Delete the `## Limits` heading from `examples/ai-assistance-record.md` | `FAIL ... missing heading 'Limits'`, exit status 1 |
| Empty the text under `## Problem` in `examples/pull-request.md` | `FAIL ... heading 'Problem' is empty` |
| Replace a sentence in `examples/evidence-note.md` with `{{Hosted run}}` | `FAIL ... an unfilled {{placeholder}} is left` |
| Delete the first line of `examples/story-card.md` | `FAIL ... the first line must label it as a constructed example` |
| Remove every `{{` and `}}` from `templates/retrospective.md` | `FAIL ... a template must still show its {{placeholders}}` |
| Delete `examples/known-issues.md` | `FAIL ... no such file`, and 25 files checked |
| Empty the value after `Status:` in `examples/decision-record.md` | `FAIL ... 'Status:' has no value` |
| Delete `## Revisit triggers` from `templates/decision-record.md` | `FAIL ... missing heading 'Revisit triggers'` |
| Delete the `templates` and `examples` folders | `FAIL nothing was checked`, exit status 1 |
| `--file pull-request` with a path that does not exist | `FAIL nothing was checked`, exit status 1 |
| `--file nonsense ...` | `unknown template name: nonsense`, exit status 2 |

These experiments check that the script catches the chosen faults. They do not establish that it catches every possible fault, and they say nothing about whether a document is true.

## 5. Common mistakes, by template

| Template | Mistakes to look for |
|---|---|
| Story card | A feature name with no actor and no value; guesses listed as confirmed rules; “Completion evidence” filled in before anything exists |
| Acceptance example | A visible result without the state afterwards; vague values; two actions under “When”; “Evidence” that points at a check that does not run the example |
| Definition of Done | Conditions nobody can check; claiming a condition that does not exist yet, such as a passing pipeline before there is one; weakening it to move a card |
| Decision record | Recording a decision after the fact without saying so; editing an old record; listing only the chosen option; “reviewed” when nobody reviewed it |
| Iteration plan | Allocating every hour to features; converting story points into hours; hiding an overrun by skipping checks; treating unallocated hours as a promise |
| Team agreement | Copying another team's agreement; an empty gaps section; never rereading it |
| Pull request | A description that restates the diff; mixing a functional change with a workflow change; quoting a result that was not run on this revision; an invented review exchange |
| Evidence note | Planned behaviour written as implemented; the result of one revision cited for another; guidance text left in place of an answer |
| Requirements to evidence | A test that exists but checks something else; a table nobody rereads |
| Known issues | A row with a description and no decision; deleting a row to shorten the list |
| Release notes | “Various improvements”; saying production behaviour did not change without checking; an empty “Not verified” |
| Retrospective | An observation with no evidence; actions with no owner or date; naming a person as the cause |
| AI assistance record | Writing it after the details are forgotten; omitting what the assistant saw; secrets or personal data; “reviewed and verified” with nothing behind it |

## 6. Answers to the activity

1. **Check the kit.** `TEMPLATE CHECK PASSED: 26 file(s)`.
2. **Fill in one template for a real change** and run `--file`. Typical reports are a missing heading (renamed rather than kept), an empty section and a left-over placeholder.
3. **Break your file three ways.** Each break gives a different message (Section 4.3); restoring the file gives a pass.
4. **Choose a template your team does not use.** A good answer names the question the template forces, for example “what would make us reopen this decision?” for a decision record or “what was not verified?” for release notes.
5. **Fill in an evidence note**, writing “none yet” where something does not exist.

### The constructed AI candidate

The candidate in the activity is a complete evidence note that an assistant might produce when asked to “fill in the template”. It is constructed for teaching; it is not a captured model response. Save it as `fixtures/invented-evidence-note.md`:

```markdown
<!-- Constructed to illustrate: an evidence note that is complete in shape and invented in content. Not real evidence. -->
# Evidence note: example team, week 6

## Repository and baseline revision
example-team/lending, at revision a3f9c21.

## Implemented behaviour
US-01 and US-02 are fully implemented and verified.

## Local environment and command
JDK 17.0.11, Git Bash, `bash scripts/check.sh`.

## Local check result
All checks passed.

## Hosted passing run
Run 1432 passed on revision a3f9c21 on 12 October.

## Deliberate failure
Introduced and fixed; all checks green.

## Restored pass
Restored at revision b81e0d4; run 1433 passed.

## Independent review
Reviewed and approved by the team.

## Unresolved questions
None.

## Known limitations
None.
```

```bash
bash scripts/check-templates.sh --file evidence-note fixtures/invented-evidence-note.md
```

The script reports `TEMPLATE CHECK PASSED: 1 file(s)`. The note has every heading, every section is non-empty and no placeholder is left. It is also unverifiable and suspicious, and that is the point of the exercise.

| Entry | Could a reviewer verify it? How? | Why it looks invented |
|---|---|---|
| “Revision a3f9c21”, “run 1432”, “run 1433” | Yes. Open the repository and the run pages; compare the revision and the date | Nothing links the run to the revision. A run number and a short hash, with no address, are easy to make up |
| “US-01 and US-02 are fully implemented and verified” | Yes. Read the code and the checks for US-02 | “Fully” and “verified” are claims, and no check is named |
| “Introduced and fixed; all checks green” | Yes, if a failed run and a restored run both exist | A deliberate failure should name the failed assertion and the failed run |
| “Reviewed and approved by the team” | Only if a reviewer and the review text exist | No named reviewer, no finding, no correction; it is the ritual version |
| “None” under both questions and limitations | No | A real project always has an open question and a limit; “none” suggests the headings were filled to pass |

A script that checks shape passes this note, so a reviewer must check content. The honest evidence note in Section 3 shows the opposite habit: it says “none yet” and names the next action.

## 7. Teaching and revision notes

Ask learners to predict each fault-experiment result before they run it. The invented evidence note is worth ten minutes in class: have pairs mark every entry as verifiable, unverifiable or suspicious before they read the table in Section 6. A team without access to a hosted platform can still use every template; the evidence-note fields for a hosted run are filled with “none yet” and a next action, which is the honest outcome.

Keep the templates in the repository beside the work they describe. When a chapter changes the headings of its record, change the template and the list in `check-templates.sh` together, and run the script. Do not add the kit to the lending project's test totals: it is documents and a script, and it has no Java tests.

## References

Opened on 13 October 2026. The templates and examples are original; source text has not been reproduced.

1. Schwaber, K. and Sutherland, J., [The Scrum Guide](https://scrumguides.org/scrum-guide.html), November 2020. The Definition of Done as a commitment of the increment; the purpose of the Sprint Retrospective.
2. Nygard, M., [Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions), 15 November 2011. Short numbered records: title, context, decision, status, consequences; superseded and not deleted.
3. GitHub Docs, [Creating a pull request template for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository). A file named `pull_request_template.md` in the repository root, `docs` or `.github` supplies a pull-request template.
4. [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Changelogs for humans, the change types and the dated entry for each version.
