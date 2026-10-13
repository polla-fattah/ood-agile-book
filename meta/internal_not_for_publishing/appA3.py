from cleanup_lib import *

M = "Appendix_A_Programming_Readiness_and_Notation.md"
C = "Appendix_A_Code_Explanations_and_Solutions.md"

# --- A.8 relationships table: add the 'drawn by hand' column
replace_once(M, "The renderer supplies the actual symbols.",
             "The renderer supplies the actual symbols; the last column says how to draw the same relationship by hand.")
NEW_TABLE = """| Relationship | Mermaid declaration | Meaning and review question | Drawn by hand |
|---|---|---|---|
| Association | `A --> B : holds` | A structural link, navigable from A to B. Does the design retain that link? | A solid line, with an open arrowhead at B to show navigation. |
| Association with navigation unspecified | `A -- B` | A link without a stated navigation direction; do not infer that both Java classes have fields. | A solid line with no arrowhead. |
| Dependency | `A ..> B : uses` | A uses B. A method-only use often needs no stronger relation. | A dashed line with an open arrowhead at B. |
| Shared aggregation | `Whole o-- Part` | A grouping claim, with a hollow diamond at the whole. Its precise meaning needs the model's explanation. | A solid line with a hollow diamond at the whole. |
| Composite aggregation | `Whole *-- Part` | Strong whole/part ownership, with a filled diamond at the whole. Is exclusive composite ownership and lifecycle intent actually specified? | A solid line with a filled diamond at the whole. |
| Generalisation / inheritance | `Base <\\|-- Derived` | The hollow triangle points to the general type. Does Derived meet Base's behavioural obligations? | A solid line with a hollow triangle at the general type. |
| Interface realisation | `Contract <\\|.. Implementation` | The hollow triangle points to the interface; the line is dashed. Does the class implement that contract? | A dashed line with a hollow triangle at the interface. |"""
cut(M, 0, "A.8 relationship table (replaced by a version with a hand-drawing column)",
    "| Relationship | Mermaid declaration | Meaning and review question |", "", NEW_TABLE, keep_evidence=False)

# --- A.8: sequence, state and flowchart reference
OLD = "Mermaid sequence syntax includes `participant`, messages such as `Caller->>Service: request`, return messages such as `Service-->>Caller: result`, and blocks closed with `end` [11]. Treat each diagram's caption as part of its meaning."
NEW = """The three kinds below are the ones, besides class diagrams, that the book draws. Each has a symbol table (the Mermaid source, and how the same symbol is drawn by hand) and one small example. The examples are notation exercises, not part of the lending project's design. Treat each diagram's caption as part of its meaning: it says what an arrow stands for in that figure.

### Sequence diagrams

A sequence diagram shows **one scenario in time order**, from top to bottom. It answers “who asks whom, and in what order?” and not “what classes exist?”. Chapter 8 introduces it; Chapters 9 and 10 use it again [11].

| Element | Mermaid source | Drawn by hand | Reading |
|---|---|---|---|
| Participant | `participant R as ReservationRules` | A box at the top of the page, with a name. | An object or role taking part. `as` gives it a short label for the lines below. |
| Lifeline | (the renderer draws it) | A dashed vertical line under the box. | That participant's time line. Time runs downwards. |
| Call | `U->>R: mayRequest(2, 7)` | A solid line with a filled arrowhead, labelled with the call. | The sender asks the receiver to do something. |
| Return | `R-->>U: true` | A dashed line with an open arrowhead. | The answer. In this book a return can also carry an exception. |
| Note | `Note over U,R: Nothing is stored` | A note box across the participants it concerns. | A comment on the scenario, not a message. |
| Alternatives | `alt` ... `else` ... `end` | A frame labelled `alt`, with a dashed line between the alternatives. | Exactly one alternative happens in a given run. |
| Optional, repeated | `opt` ... `end`, `loop` ... `end` | A frame labelled `opt` or `loop`. | A block that may happen once or not at all, and a block that repeats. The book's figures do not use them. |

```mermaid
sequenceDiagram
    participant U as Caller
    participant R as ReservationRules
    U->>R: mayRequest(count, days)
    alt Count below the limit
        R-->>U: true
    else Count at the limit
        R-->>U: false
    end
    Note over U,R: Nothing is stored
```

**Figure A.2.** A sequence-diagram notation example. The caller asks the rules object one question and receives one of two answers. The note says what does *not* happen.

Do not read a sequence diagram as a complete specification. It shows the scenario its author chose, and a path that is missing is not a claim that the path cannot happen (Figure 8.2 leaves out malformed provider data to stay readable). The vertical order is time order. It is not the order of the classes in the source code.

### State diagrams

A state diagram shows the **positions an object can be in and the events that move it between them**. It says nothing about how the states are implemented. Chapter 9 introduces it [12].

| Element | Mermaid source | Drawn by hand | Reading |
|---|---|---|---|
| State | `AVAILABLE` | A rounded rectangle with a name. | A situation the object can be in. |
| Start | `[*] --> AVAILABLE` | A filled circle with an arrow to the first state. | Where a new object begins. |
| Transition | `AVAILABLE --> RESERVED: reserve` | An arrow labelled with the event. | When the event happens in the first state, the object moves to the second. |
| Guard | `AVAILABLE --> RETIRED: retire [no open reservation]` | A label of the form `event [condition]`. | The transition fires only if the condition holds. The reservation lifecycle of Chapter 9 has no guards. |
| End | `RETIRED --> [*]` | A circle with a filled centre. | The object's life ends here. |

```mermaid
stateDiagram-v2
    [*] --> AVAILABLE
    AVAILABLE --> RESERVED: reserve
    RESERVED --> AVAILABLE: cancel
    RESERVED --> ON_LOAN: collect
    ON_LOAN --> AVAILABLE: return
    AVAILABLE --> RETIRED: retire [no open reservation]
    RETIRED --> [*]
```

**Figure A.3.** A state-diagram notation example for an equipment item. It is not the reservation lifecycle of Chapter 9 and not a design for the project.

To read one, take each state and each event in turn and ask whether an arrow exists. A missing arrow means the model does not allow that event in that state. The diagram does not say what the program does when the event arrives anyway: it might throw, ignore it or report an error. That is a separate decision. A state diagram also does not require one Java subclass per state.

### Flowcharts and dependency views

A flowchart is one Mermaid kind with several uses in this book. In a **process flow** the arrows mean “then” or “only if the previous step passed” (Figures 11.1 and 13.2). In a **dependency view** an arrow means that the code at its start may refer to the code at its end (Figure 10.1). In an **object-assembly view** a dotted arrow means “creates” (Figure 6.2). The caption always says which; never assume it.

| Element | Mermaid source | Drawn by hand | Reading |
|---|---|---|---|
| Step or part | `A["Check for overlap"]` | A rectangle with a label. | An action, or a part of the system. |
| Decision | `B{"Count below the limit?"}` | A diamond with a question. | A choice. Each exit carries a label. |
| Arrow | `A --> B` | A solid arrow. | What the caption says: “then”, “may refer to” or “passed to”. |
| Labelled arrow | `B -- "yes" --> C` | An arrow with a short label. | The condition or reason for that exit. |
| Dotted arrow | `A -. creates .-> C` | A dashed arrow with a label. | A different relationship from the solid arrows; the label says which. |
| Direction | `flowchart TD` or `flowchart LR` | (the page layout) | Top-down or left-to-right. It is layout only and carries no meaning. |

```mermaid
flowchart TD
    A["Request arrives"] --> B{"Count below the limit?"}
    B -- "no" --> D["Reject the request"]
    B -- "yes" --> C{"Overlaps another reservation?"}
    C -- "yes" --> D
    C -- "no" --> E["Store the reservation"]
```

**Figure A.4.** A process-flow notation example. Boxes are steps, diamonds are decisions and every exit of a diamond is labelled.

```mermaid
flowchart LR
    P["Presentation"] --> A["Application"]
    A --> D["Domain"]
    I["Storage adapter"] --> A
```

**Figure A.5.** A dependency-view notation example. An arrow means that code in the first box may refer to code in the second. A missing arrow means the reference is not permitted. The figure says nothing about the order of calls.

Formal UML has its own notation for the second use. A **package diagram** draws each package as a folder-shaped box, and a dependency is a dashed arrow with an open head from the package that uses to the package that is used. A **component diagram** draws each component as a box labelled `«component»` and shows its interfaces as a small ball (provided) and a socket (required). The book does not draw either; it draws the dependency view as a flowchart, because the only question is “who may refer to whom”. The reading rule is the same in both: the arrow starts at the code that refers and points to the code referred to. In a dependency view the arrow is **not** the direction of runtime calls. In Figure 10.1 the storage adapter refers to an application-owned contract, so the arrow points from the adapter to the application, although the coordinator calls the adapter at run time [9, 13]."""
replace_once(M, OLD, NEW)

# --- opening, A.9, sources
replace_once(M, "Use A.8 beside Chapter 2's longer class-diagram exercises.",
             "Use A.8 beside Chapter 2's longer class-diagram exercises, and return to it when Chapters 8 to 10 introduce sequence, state and dependency diagrams.")
replace_once(M, "After Chapter 2, attempt D10 and compare your diagram with the solution.",
             "After Chapter 2, attempt D10 and compare your diagram with the solution. After Chapters 8 to 10, read the sequence, state and flowchart fragments in the companion, Section 4.")
replace_once(M, "11. Mermaid, [Sequence diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html). Message and alternative-block syntax.",
             "11. Mermaid, [Sequence diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html). Message and alternative-block syntax.\n"
             "12. Mermaid, [State diagrams](https://mermaid.js.org/syntax/stateDiagram.html). States, transitions and the start and end markers.\n"
             "13. Mermaid, [Flowcharts](https://mermaid.js.org/syntax/flowchart.html). Nodes, decisions, labelled and dotted links.")

# --- companion practice
PRACTICE = """### Reading practice: sequence, state and flowchart fragments

Interpret these independent **Mermaid fragments**. They are notation exercises, not complete diagrams or project designs.

| Fragment | Interpretation |
|---|---|
| `U->>R: mayRequest(2, 7)` followed by `R-->>U: true` | `U` calls `R`, and `R` returns `true`. Nothing in the fragment says that a reservation was stored. |
| `alt Count below the limit` ... `else Count at the limit` ... `end` | Two alternatives. Exactly one happens in a given run. |
| `AVAILABLE --> RESERVED: reserve` | When the event `reserve` happens in the state `AVAILABLE`, the object moves to `RESERVED`. |
| `AVAILABLE --> RETIRED: retire [no open reservation]` | The same kind of transition, with a guard. It fires only if the condition holds. |
| `RETIRED --> [*]` | `RETIRED` is an end state. No further event moves the object out of it. |
| `B{"Count below the limit?"}` with one exit labelled `yes` and one labelled `no` | A decision with two labelled exits. Each path continues from the exit that matches the answer. |
| `I --> A` in a dependency view | Code in `I` may refer to code in `A`. It says nothing about which of them calls the other at run time. |

Two further questions. In Figure A.3, what does the absence of an arrow from `ON_LOAN` to `RETIRED` mean? The model does not allow `retire` in that state; the diagram does not say what the program does if the event arrives anyway. Why does the arrow in Figure A.5 point from the storage adapter to the application although the application calls the adapter at run time? Because the arrow shows which code refers to which code in the source, and the adapter's source refers to the contract that the application owns.
"""
replace_once(C, "## 5. Offline AI-activity solution", PRACTICE + "\n## 5. Offline AI-activity solution")

with LOG.open("a", encoding="utf8", newline="\n") as handle:
    handle.write("## Appendix A: UML reference drafted (A.8)\n\n")
    for entry in [
        "Manuscript A.8: the class-relationship table has a new last column, `Drawn by hand`, for each relationship.",
        "Manuscript A.8: the one-sentence note about Mermaid sequence syntax was replaced by three subsections: `Sequence diagrams` (Figure A.2), `State diagrams` (Figure A.3) and `Flowcharts and dependency views` (Figures A.4 and A.5). Each has a symbol table with the Mermaid source, how it is drawn by hand and how to read it, plus one small original example and a short `do not infer` paragraph. The text points to Figures 6.2, 8.2, 10.1, 11.1 and 13.2, which are the book's own flowchart, sequence and dependency figures.",
        "The book draws no UML component diagrams: Chapter 10's package view is a flowchart. The reference says so and describes the formal UML package and component notation in one paragraph.",
        "Manuscript opening paragraph, A.9 and Sources: pointers to the new material; two new sources (Mermaid state diagrams, Mermaid flowcharts). Companion Section 4: new `Reading practice` table for sequence, state and flowchart fragments with two questions.",
        "No blank hand-drawing worksheet was added. That depends on the open question of how the midterm diagram is produced.",
    ]:
        handle.write("- " + entry + "\n")
    handle.write("\n")
print("A.8 drafted")
