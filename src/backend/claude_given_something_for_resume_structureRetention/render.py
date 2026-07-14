"""
render.py â€” turn validated JSON into a PDF, deterministically.

    python render.py sample.json out/

Pipeline stages (each is a clean seam you can unit-test):
    1. load + validate JSON      -> schema.Resume   (rejects malformed agent output)
    2. render template           -> .tex string
    3. compile with pdflatex     -> .pdf
    4. QA gate                   -> page count + overfull-box check

The LLM agents own stages upstream of (1) only. Layout lives entirely here.
"""
from __future__ import annotations
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from backend.claude_given_something_for_resume_structureRetention.schema import Resume

HERE = Path(__file__).parent

# --- GOTCHA #2: LaTeX special characters. Any of these in user content will
# break the compile (or silently mangle output) unless escaped. Order matters:
# backslash MUST be replaced first or you double-escape your own replacements.
_LATEX_SPECIAL = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
    ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
    ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
]


def latex_escape(value) -> str:
    if value is None:
        return ""
    s = str(value)
    for old, new in _LATEX_SPECIAL:
        s = s.replace(old, new)
    return s


def make_emph_filter(keywords: list[str]):
    """escape + bold the keyword-agent's terms. Escape FIRST, then wrap, so the
    \textbf we inject is the only un-escaped LaTeX in the string (safe)."""
    # longest-first so 'Azure OpenAI' wins over 'OpenAI'; word-boundaried.
    kws = sorted({k.strip() for k in keywords if k.strip()}, key=len, reverse=True)
    patterns = [(re.compile(rf"(?<!\w){re.escape(latex_escape(k))}(?!\w)", re.I), k)
                for k in kws]

    def emph(value) -> str:
        s = latex_escape(value)
        for pat, _ in patterns:
            s = pat.sub(lambda m: r"\textbf{" + m.group(0) + "}", s)
        return s
    return emph


def build_env(keywords: list[str]) -> Environment:
    # --- GOTCHA #1: remap delimiters away from { } so LaTeX braces survive. ---
    env = Environment(
        loader=FileSystemLoader(str(HERE)),
        block_start_string=r"\BLOCK{", block_end_string="}",
        variable_start_string=r"\VAR{", variable_end_string="}",
        comment_start_string="%#", comment_end_string="#%",
        trim_blocks=True, lstrip_blocks=True, autoescape=False,
    )
    env.filters["latex"] = latex_escape
    env.filters["emph"] = make_emph_filter(keywords)
    return env


def render_tex(resume: Resume) -> str:
    env = build_env(resume.bold_keywords)
    tmpl = env.get_template("template.tex.j2")
    # Pass model OBJECTS (not .model_dump() dicts): a field named "items"
    # would otherwise collide with dict.items() under Jinja attribute lookup.
    ctx = {name: getattr(resume, name) for name in type(resume).model_fields}
    return tmpl.render(**ctx)


def compile_pdf(tex: str, out_dir: Path, stem: str = "resume") -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    tex_path = out_dir / f"{stem}.tex"
    tex_path.write_text(tex, encoding="utf-8")
    # run twice for stable refs/page numbers; -halt-on-error fails loud.
    for _ in range(2):
        proc = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             f"-output-directory={out_dir}", str(tex_path)],
            capture_output=True, text=True,
        )
    if not (out_dir / f"{stem}.pdf").exists():
        tail = "\n".join(proc.stdout.splitlines()[-15:])
        raise RuntimeError(f"pdflatex failed:\n{tail}")
    return out_dir / f"{stem}.pdf"


def qa_gate(pdf_path: Path) -> dict:
    """Automatable quality check â€” the eyeball step, turned into a test."""
    report: dict = {"pdf": str(pdf_path)}

    # page count via poppler's pdfinfo
    if shutil.which("pdfinfo"):
        info = subprocess.run(["pdfinfo", str(pdf_path)],
                              capture_output=True, text=True).stdout
        m = re.search(r"Pages:\s+(\d+)", info)
        report["pages"] = int(m.group(1)) if m else None

    # overfull boxes = text bleeding past the margin (a layout smell)
    log = pdf_path.with_suffix(".log")
    if log.exists():
        text = log.read_text(errors="ignore")
        report["overfull_hboxes"] = len(re.findall(r"Overfull \\hbox", text))

    report["ok"] = report.get("pages") == 1 and report.get("overfull_hboxes", 0) == 0
    return report


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "sample.json"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "out"

    data = json.loads(src.read_text())
    resume = Resume.model_validate(data)          # stage 1: validate
    tex = render_tex(resume)                       # stage 2: render
    pdf = compile_pdf(tex, out)                    # stage 3: compile
    report = qa_gate(pdf)                          # stage 4: QA

    print(json.dumps(report, indent=2))
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
