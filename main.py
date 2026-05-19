"""Day 4 — Résumé Analyzer"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from parse import read_resume_pdf, read_jd_text
from analyzer import (
    extract_resume_profile,
    extract_jd_profile,
    analyse_keyword_match,
    analyse_bullets,
    analyse_jargon,
    analyse_structure,
    analyse_degree_alignment,
    summarise_overall,
    compute_overall_score,
)
from report import render_markdown


VALID_DEGREES = {"RTIS", "IMGD", "UXGD", "BFA"}


def parse_args(argv: list[str]) -> tuple[str, str, str]:
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description=(
            "Analyse a PDF résumé against a job description and produce "
            "a scored report (0–100, 60 = ATS pass threshold)."
        ),
    )
    parser.add_argument("resume", metavar="resume.pdf", help="Path to the PDF résumé")
    parser.add_argument("job", metavar="job.txt", help="Path to the job description (plain text)")
    parser.add_argument(
        "degree",
        choices=sorted(VALID_DEGREES),
        metavar="degree",
        help="DigiPen degree code: RTIS | IMGD | UXGD | BFA",
    )
    args = parser.parse_args(argv[1:])
    return args.resume, args.job, args.degree

def analyze(rsp,jdp,dg) -> str:
    print("start analyse")
    logs = []  # buffer to collect messages

    def log(msg: str):
        logs.append(msg + "\n")

    resume_path, job_path, degree = [rsp, jdp, dg]
    load_dotenv()
    import os
    model = os.getenv("MODEL", "openai/gpt-4o-mini")
    log(f"Using model: {model}")

    log(f"[1/8] Parsing résumé: {resume_path}")
    try:
        resume_text = read_resume_pdf(resume_path)
    except ValueError as exc:
        log(f"ERROR: {exc}")
        return "\n".join(logs)

    log(f"[2/8] Reading JD: {job_path} (degree={degree})")
    
    jd_text = job_path

    try:
        log("[3/8] Extracting résumé profile (LLM)...")
        resume_profile = extract_resume_profile(resume_text)

        log("[4/8] Extracting JD profile (LLM)...")
        jd_profile = extract_jd_profile(jd_text)

        log("[5/8] Keyword match (LLM)...")
        keyword_match = analyse_keyword_match(resume_profile, jd_profile)

        log("[6/8] Bullet audit (LLM)...")
        bullets = analyse_bullets(resume_profile)

        log("[7/8] Jargon, structure, degree alignment (LLM x3)...")
        jargon    = analyse_jargon(resume_profile, degree, jd_profile)
        structure = analyse_structure(resume_text)
        degree_alignment = analyse_degree_alignment(jd_profile, degree)

    except RuntimeError as exc:
        log(f"ERROR: {exc}")
        return "\n".join(logs)

    report = {
        "meta": {
            "resume_path": resume_path,
            "job_path": job_path,
            "degree": degree,
            "model": model,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        },
        "resume_profile":  resume_profile,
        "jd_profile":      jd_profile,
        "keyword_match":   keyword_match,
        "bullets":         bullets,
        "jargon":          jargon,
        "structure":       structure,
        "degree_alignment": degree_alignment,
    }
    report["overall_score"]        = compute_overall_score(report)
    report["passes_ats_threshold"] = report["overall_score"] >= 60

    try:
        log("[8/8] Final summary (LLM)...")
        report["summary"] = summarise_overall(report)
    except RuntimeError as exc:
        log(f"ERROR: {exc}")
        return "\n".join(logs)

    # ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Path("outputs").mkdir(exist_ok=True)
    # json_path = f"outputs/match_report_{ts}.json"
    # md_path   = f"outputs/match_report_{ts}.md"

    # Path(json_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    # render_markdown(report, out_path=md_path)

    verdict = "PASS" if report["passes_ats_threshold"] else "FAIL"
    logs.append("")
    logs.append(
        f"Score: {report['overall_score']}/100  "
        f"({verdict} 60% ATS threshold)"
    )
    # logs.append(f"JSON:  {json_path}")
    # logs.append(f"MD:    {md_path}")
    logs.append("")
    logs.append(report["summary"])

    return "\n".join(logs)
