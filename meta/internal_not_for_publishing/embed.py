"""Fill the diagram markers in a deck with the SVG drawn by the dg_chNN.py modules.

  python embed.py content/slides/chapter-02.md

A marker pair in the deck looks like  <!--svg:NAME-->  <!--/svg-->  and whatever lies between is replaced,
so the command can be run again after a diagram changes. Internal, not for publishing.
"""
import importlib.util
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent


def registry():
    reg = {}
    for f in sorted(HERE.glob("dg_ch*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        reg.update(mod.DIAGRAMS)
    return reg


def embed(path):
    reg = registry()
    p = pathlib.Path(path)
    text = p.read_text(encoding="utf8")
    used = []

    def sub(m):
        name = m.group(1)
        if name not in reg:
            raise SystemExit(f"no diagram called {name!r}")
        used.append(name)
        svg = reg[name]().render()
        assert "\n\n" not in svg, name
        return f"<!--svg:{name}-->\n{svg}\n<!--/svg-->"

    new = re.sub(r"<!--svg:([\w-]+)-->.*?<!--/svg-->", sub, text, flags=re.S)
    markers = len(re.findall(r"<!--svg:", new))
    p.write_text(new, encoding="utf8", newline="\n")
    print(f"{path}: {len(used)} diagram(s) filled ({', '.join(used)}); markers in file: {markers}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf8")
    for arg in sys.argv[1:]:
        embed(arg)
