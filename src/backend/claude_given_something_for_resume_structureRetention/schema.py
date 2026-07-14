"""
schema.py — the structured contract between your agents and the renderer.

The whole point of Option B: your LLM agents NEVER emit LaTeX. They emit this
validated JSON. The renderer owns 100% of the layout. That separation is what
makes the pipeline robust to arbitrary input resumes.

Your four agents map onto this cleanly:
  - parser agent      -> fills Contact / Education / Experience from the raw PDF
  - scorer agent      -> produces match_score (not rendered, used for reporting)
  - keyword agent     -> produces missing_keywords + bold_keywords
  - rewriter agent    -> rewrites bullets / summary with keywords woven in
"""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class Contact(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    linkedin_label: Optional[str] = None   # visible text, e.g. "LinkedIn: Mrinmoy-H"
    linkedin_url: Optional[str] = None
    github_label: Optional[str] = None
    github_url: Optional[str] = None


class Education(BaseModel):
    institution: str
    location: str
    dates: str
    degree: str


class BulletGroup(BaseModel):
    # Optional sub-heading inside a role, e.g. "RAG & LLM Applications".
    heading: Optional[str] = None
    bullets: list[str] = Field(default_factory=list)


class Role(BaseModel):
    title: str
    org: str
    dates: str
    subtitle: Optional[str] = None         # e.g. "Generative AI, RAG, Agentic AI"
    groups: list[BulletGroup] = Field(default_factory=list)


class SkillCategory(BaseModel):
    name: str                              # e.g. "Generative AI & LLMs"
    items: list[str] = Field(default_factory=list)


class Resume(BaseModel):
    contact: Contact
    summary: Optional[str] = None
    education: list[Education] = Field(default_factory=list)
    experience: list[Role] = Field(default_factory=list)
    skills: list[SkillCategory] = Field(default_factory=list)

    # --- fields the renderer reads but does not "print" as a section ---
    # Whole-word, case-insensitive terms the keyword agent wants emphasised.
    # The renderer bolds them AFTER LaTeX-escaping (safe). Hooks straight onto
    # your missing-keywords output.
    bold_keywords: list[str] = Field(default_factory=list)
