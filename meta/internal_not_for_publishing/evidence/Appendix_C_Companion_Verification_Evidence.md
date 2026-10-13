# Appendix C companion (template kit and checker): verification and working evidence (NOT FOR PUBLISHING)

Run on 13 October 2026. The published page is `content/companion/appendix-c.md`. It is a companion to the Appendix C written by someone else; no existing file was overwritten.

## Environment

Windows 11, Git Bash (the first `bash` on the path; the WSL `bash.exe` and a WindowsApps launcher are also on this machine's path and gave wrong results when a Python test launched `bash` by name), Git 2.54.0, Python 3.x with PyYAML, Hugo 0.166.0 extended. No Java or Maven is needed by the kit.

## What was built

13 templates, 13 worked examples, `scripts/check-templates.sh`, `fixtures/invented-evidence-note.md`: 28 files. The page was generated from the kit files, so the text and the files cannot drift.

## What was run

| Check | Result |
|---|---|
| Rebuild the kit from the published page (headings of the form `### N.N \`path\``, plus the fixture) | 28 files extracted; `diff -r` against the tested kit: identical |
| `bash scripts/check-templates.sh` on the rebuilt kit | `TEMPLATE CHECK PASSED: 26 file(s)`, exit 0 |
| `--file evidence-note fixtures/invented-evidence-note.md` | passes (as the page says it does) |
| Fault: heading removed from an example | `FAIL ... missing heading 'Limits'`, exit 1 |
| Fault: empty body | `FAIL ... heading 'Problem' is empty` |
| Fault: placeholder left in an example | `FAIL ... an unfilled {{placeholder}} is left` |
| Fault: label line deleted | `FAIL ... the first line must label it as a constructed example` |
| Fault: placeholders removed from a template | `FAIL ... a template must still show its {{placeholders}}` |
| Fault: example file deleted | `FAIL ... no such file`, 25 files checked |
| Fault: `Status:` without a value | `FAIL ... 'Status:' has no value` |
| Fault: template heading removed | `FAIL ... missing heading 'Revisit triggers'` |
| Fault: `templates/` and `examples/` deleted | 26 `no such file` lines, then `FAIL nothing was checked`, exit 1 |
| `--file pull-request /no/such.md` | `FAIL nothing was checked`, exit 1 |
| `--file nonsense x.md` | `unknown template name: nonsense`, exit 2 |
| The book's own records taken from `content/companion/chapter-10/13/14.md` and `chapter-15.md` | ADR-010, ADR-013, ADR-014 each pass `--file decision-record`; the Chapter 15 filled record passes `--file ai-assistance-record` |
| Hugo build of the page in a minimal scratch site | exit 0, no warnings; the `{{...}}` placeholders appear literally in the output |
| Code fences | 64 fence lines, balanced; front matter parses (`title`, `weight: 230`) |

## Findings during the work

- A first Python test launched `bash` by name and got the WSL launcher, so the ADR checks failed; with Git Bash's full path all passed. This is the same ambiguity described in Appendix B.
- An earlier manuscript draft for Appendix C (a full replacement of the existing page) was not published: the existing Appendix C is someone else's work and untracked in Git, so replacing it would have lost it. The review of that appendix is in `meta/Appendices_Review_and_Chapter_Reference_Contrast.md`.

## Sources opened

| Source | Check |
|---|---|
| Scrum Guide | HTTP 200; Definition of Done, commitment and Sprint Retrospective present |
| Nygard, Documenting Architecture Decisions | HTTP 200; superseded, consequences present |
| GitHub pull request template page | HTTP 200; `pull_request_template.md` in the root, `docs/` and `.github/` described |
| Keep a Changelog 1.1.0 | HTTP 200; Added and Security present |

## Not verified

- The checker was run on Windows (Git Bash) only, not on macOS or Linux; it avoids GNU-only options, but that was not run.
- No hosted platform was used: the pull-request template location was read from the documentation, not tried.
- The kit was not used by a real team; the examples are constructed.
