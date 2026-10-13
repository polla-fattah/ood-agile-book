# SE506 Lecture Slides: Register of the Chapter Decks

*OO Development and Agile Practices*  
*Module Leader: Dr. Polla Abdulhamid Fattah*

One deck per chapter, `content/slides/chapter-NN.md` (NN = 01 to 15). Each deck was written from its chapter and its companion, section by section. The old weekly decks are retired: copies are in `internal_not_for_publishing/retired_week_decks/` (with the previous version of this register). Slide counts are the measured number of `.slide__inner` elements at 1280 x 720.

Checks run on every deck: no slide scrolls vertically or horizontally (`check.js`, measured in the browser), no text overlap or edge crossing in the hand-built SVG diagrams, and `slidefacts.py` against the chapter, companion and appendices (every code name and number traces to the sources).

| Deck | Chapter | Slides | Diagrams |
|---|---|---:|---:|
| chapter-01 | Developing Software That Can Change | 145 | 1 |
| chapter-02 | Object-Oriented Development Beyond Syntax | 183 | 9 |
| chapter-03 | Agile Development and the Nature of Change | 149 | 3 |
| chapter-04 | From Requirements to an Iteration | 159 | 4 |
| chapter-05 | Responsibilities, Extension, and Substitutability | 151 | 3 |
| chapter-06 | Interfaces, Dependencies, and Composition | 126 | 3 |
| chapter-07 | Testing as a Design Practice | 144 | 3 |
| chapter-08 | Creating and Connecting Objects | 118 | 6 |
| chapter-09 | Designing Changing Behaviour | 109 | 4 |
| chapter-10 | From Classes to Application Structure | 125 | 3 |
| chapter-11 | Refactoring and Legacy Code | 112 | 4 |
| chapter-12 | Measuring Progress, Flow and Technical Health | 101 | 2 |
| chapter-13 | Integration, Delivery and Feedback | 120 | 3 |
| chapter-14 | Responding to Change and Handing Over | 127 | 3 |
| chapter-15 | AI as a Software Engineering Assistant | 117 | 2 |

## Notes

- The decks keep the existing style: `assets/slides/deck.css`, `deck.js` and `layouts/slides/page.html` were not edited.
- Mermaid diagrams do not render on the deck pages, so every diagram is an inline SVG drawn by `internal_not_for_publishing/svgkit.py` and the `dg_chNN.py` files; `embed.py` fills the `<!--svg:NAME-->` markers.
- Open: no deck for Appendices A to F; the companion for Chapter 13 gives 203/26/3 test invocations in its expected output (Section 1.2) but its model answer to B1 says 202/25/3, which the decks do not repeat (they use 203/26/3).
