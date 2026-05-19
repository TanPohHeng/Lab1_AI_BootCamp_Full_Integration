RESUME_PROFILE_PROMPT = """
Instruction:
Extract only what is literally present in the résumé text. Never invent, paraphrase, or infer information. If a field is absent, return an empty array or empty string as appropriate.

Context:
This is for automated résumé analysis in the bootcamp. The résumé follows standard formatting with sections for skills, projects, and experience. The goal is to capture the candidate’s actual profile data exactly as written.

Constraints:
- Copy what is present — never invent
- Empty array if field absent
- Schema embedded verbatim in Output

Output:
{
  "name": "...",
  "skills": {
    "languages": ["..."],
    "frameworks": ["..."],
    "tools": ["..."]
  },
  "projects": ["..."],
  "experience": ["..."]
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""
JD_PROFILE_PROMPT = """
Instruction:
Extract only what is literally present in the job description (JD) text. Never invent, paraphrase, or infer information. If a field is absent, return an empty array or empty string as appropriate.

Context:
This is for automated résumé analysis in the bootcamp. The job description follows standard formatting with sections for required skills and experience and preferred skills. The goal is to capture the role requirements exactly as written.

Constraints:
- Copy what is present — never invent
- Empty array if field absent
- Schema embedded verbatim in Output

Output:
{
  "required_skills": ["..."], 
  "preferred_skills": ["..."]
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""
#to update and rewrite so the LLM will perform keyword matching on partial matches.
KEYWORD_MATCH_PROMPT = """
Instruction:
Given the resume profile JSON and JD profile JSON, evaluate skills in the resume JSON to the skill listed in the JD JSON by flagging skills that are present and missing in the resume JSON 
and return a JSON report of the present and missing keywords.
Use the skills given in the JD profile JSON as criterion, do not substitute your own. 

Context:
This is for automated résumé analysis in the bootcamp. You are an ATS keyword auditor evaluating resumes against Singapore
entry-level technical job requirements. The goal is to evaluate the resume profile JSON based on the criterions in the JD profile JSON.

Constraints:
- Return scores + flags only
- Never suggest rewrites
- score keyword_match_score between 0 to 100

Output:
{
  "keyword_match_score": "...", 
  "present": [{
        "keyword": "...",
        "score": "..."
      }], 
  "missing": [{
        "keyword": "...",
        "score": "..."
      }]
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""


BULLET_QUALITY_PROMPT = """
Instruction:
Given the resume profile JSON and JD profile JSON, evaluate the quality of each bullet point in the resume profile JSON . Use the following as criterion - do not use your own criterion 

EVALUATION CRITERIA (use these exactly — do not substitute your own):
  - Criterion 1: Action → Technology → Impact FORMULA
      [Strong Action Verb]
    + [Specific Tools & Tech Names]
    + [Measurable Result or Scope]
  - Criterion 2:Action Verb — start strong: Designed, Engineered, Implemented, Led, Reduced. Not "Worked on" or "Helped with." The first word signals your role and ownership.
  - Criterion 3: Technology — name the exact tools: "Vulkan," "C++," "Dear ImGui." Not "a graphics library." Recruiters and ATS scan for these specific names — vague descriptions match nothing.
  - Criterion 4: Impact — quantify what changed: "reduced iteration time by 40%," "handled 500+ objects at 60 fps," "deployed on Windows and Android." Numbers make achievements concrete and memorable.
        Level 1: OK (What most students write)
            Built the UI for a 3D game editor using ImGUI.
            This is vague. What kind of editor? What platforms? What was the result?

        Level 2: Better (Add context and real tech names)
            Built the entire UI for a 3D game editor (a digital workshop where creators build virtual worlds) using Dear ImGui and Vulkan, supporting both Windows and Android.
            Now we know the scope, the technologies, and the platforms.

        Level 3: Best (Tell a story with impact)
            Designed a Vulkan-based rendering tool using C++ and Dear ImGui that reduced iteration time for level designers by 40%, supporting cross-platform deployment on Windows and Android.
            This shows what you did, how you did it, and why it mattered. This is what gets you interviews.

Context:
This is for automated résumé analysis in the bootcamp. You are an ATS keyword auditor evaluating resumes against Singapore
entry-level technical job requirements. The goal is to evaluate the resume profile JSON based on the criterions in the JD profile JSON.

Constraints:
- Embed rubric tables verbatim
- Return scores + flags only
- Never suggest rewrites
- output bullet_quality_avg as a score out of 100

Output:
{
  "bullet_quality_avg": "...", 
  "bullets": ["..."]
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""

JARGON_AUDIT_PROMPT = """
Instruction:
Given the resume profile JSON and JD profile JSON, flag game-dev jargon with translations in the resume profile JSON.
Use the following content as jargon criterion, do not substitute your own. If a field is absent, return an empty array or empty string as appropriate.

EVALUATION CRITERIA (use these exactly — do not substitute your own):
- Criterion 1: jargon_score = max(0, 100 - 10*high - 5*medium - 2*low)
- Criterion 2: Use the following table to find Game dev jargon in the resume and only flag them if found explicity in the resume.
Do not flag terms not explicitly found in the resume text.
Game Dev Term -> Industry-Friendly Translation
Game loop -> Real-time application loop / event-driven architecture
Sprite rendering -> 2D graphics rendering
Level editor -> Developer tooling / content authoring tool
Level scripting -> Gameplay automation / scripting layer
Mob spawner / enemy AI -> Entity management system / behaviour system
HP bar / HUD -> Real-time UI rendering / overlay system
Collision detection (SAT, AABB) -> Computational geometry / spatial algorithms
Gameplay programmer -> Application developer / systems programmer
Shipped a game -> Delivered a software product to end users
Game jam (48 hours) -> Rapid prototyping under time constraints
Tiled map loading -> Data-driven level/content loading from structured files
Component-based engine -> Component architecture / ECS (Entity-Component-System)
Asset pipeline -> Content/data pipeline / build automation
Frame rate optimisation -> Performance profiling and optimisation
Multiplayer netcode -> Real-time network programming / client-server architecture
- Criterion 3:
Calculate the jargon score using the following formula,
but apply deductions only for jargon terms actually present explicitly in the résumé:
jargon_score = max(0, 100 - 10*high - 5*medium - 2*low)

Context:
This is for automated résumé analysis in the bootcamp. You are an ATS keyword auditor evaluating resumes against Singapore
entry-level technical job requirements. The goal is to evaluate the resume profile JSON based on the criterions in the JD profile JSON.

Constraints:
- Return scores + flags only
- Never suggest rewrites

Output:
{
  "jargon_score": "...", 
  "flags": [
    {
      "term": "string",
      "severity": "string",
      "suggested_translation": "string"
    }
  ]
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""

STRUCTURE_AUDIT_PROMPT = """
Instruction:
Given the resume profile JSON and JD profile JSON, check and evaluate Three-Thirds layout in the resume profile JSON.
Use the following content given as criterion, do not substitute your own. Return the overall score in the JSON format below.

EVALUATION CRITERIA (use these exactly — do not substitute your own):
- Criterion 1: 
The Three-Thirds Resume Structure
Think of your one-page resume as three horizontal zones. Each zone serves a different purpose. Click each tab to see what belongs there and why.

1. Top Third — Human Eyes
2. Middle Third — Depth
3. Bottom Third — ATS Keywords
Top Third — For Human Eyes (the 5-10 Second Scan)

This is prime real estate. A recruiter's eyes land here first. It must contain:

Your name — large, clear, at the very top (14-18pt bold)
Contact information — email, phone, LinkedIn, GitHub/portfolio (one line, 9pt)
Professional summary — 1-2 sentences tailored to the job (optional but recommended)
Your most impressive project or experience — the thing you're most proud of
The professional summary should mirror the job description's language. If they want "cross-platform C++ development," your summary should say: "CS student with experience in cross-platform C++ development."

Middle Third — Projects & Experience (Depth)

This section shows your track record. Include 2-3 of your strongest:

School projects
Personal projects
Internships or work experience
Leadership roles or extracurriculars
Each entry gets a bold title line with dates, followed by 1-3 bullet points following the Action → Technology → Impact formula. Aim for specificity — named tools, numbers, and outcomes.

Bottom Third — For the ATS (Keyword Density)

This section is primarily for the ATS scanner. It can use smaller text (8-9pt) and dense, structured lists. Include:

Education — degree, school, graduation date, relevant courses
Technical Skills — programming languages, frameworks, tools, platforms
Concepts — OOP, Agile, CI/CD, unit testing, etc.
Areas of Interest (optional)
This is where you include every relevant keyword from the job description. The ATS will find them here even if a human skims past this section.

- Criterion 2: 
Your resume needs to look professional and be machine-readable. Follow these rules strictly.

Do's
✅ single-column
Use a single-column layout — no side panels, no two-column designs
✅ standard fonts
Use Calibri or Arial (10-11pt for body text)
✅ clear headings
Use standard section headings in ALL CAPS or bold (e.g. EDUCATION, PROJECTS, SKILLS)
✅ bullet points
Use simple bullet points (•) for each achievement
✅ PDF format
Save as .pdf — this preserves formatting across all devices
✅ exactly one page
Keep it to exactly one page — no more, no less
Don'ts
❌ tables / columns
Don't use tables or multi-column layouts — ATS cannot parse them reliably
❌ headers / footers
Don't put important text in headers or footers — some ATS ignores these areas entirely
❌ text boxes
Don't use text boxes or shapes — their content is often skipped by parsers
❌ profile photo
Don't include a photo — not expected in Singapore tech roles and wastes space
❌ skill-level bars
Don't use icons or rating bars (e.g. "C++: ★★★★☆") — ATS cannot read images
❌ colour for information
Don't use colour for essential information — ATS reads plain text only

Context:
This is for automated résumé analysis in the bootcamp. You are an ATS keyword auditor evaluating resumes against Singapore
entry-level technical job requirements. The goal is to evaluate the resume profile JSON based on the criterions in the JD profile JSON.

Constraints:
- Embed rubric tables verbatim
- Return scores + flags only
- Never suggest rewrites
- score between 0 to 100

Output:
{
  "structure_score": "number"
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""

DEGREE_ALIGNMENT_PROMPT = """
Instruction:
Given the resume profile JSON and JD profile JSON, check if the JD fits the student's degree in the resume profile JSON.
Use the content given in the JD profile JSON as criterion, do not substitute your own.

Context:
This is for automated résumé analysis in the bootcamp. You are an ATS keyword auditor evaluating resumes against Singapore
entry-level technical job requirements. The goal is to evaluate the resume profile JSON based on the criterions in the JD profile JSON.

Constraints:
- Return scores + flags only
- Never suggest rewrites
- score between 0 to 100

Output:
{
  "degree_alignment_score": "..."
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""

OVERALL_SUMMARY_PROMPT = """
Instruction:
Use the JSON provided to synthesize 3-bullet executive summary about whether the resume is a good fit for the JD

Context:
This is for automated résumé analysis in the bootcamp. You are an ATS keyword auditor evaluating resumes against Singapore
entry-level technical job requirements. The goal is to evaluate the resume profile JSON based on the criterions in the JD profile JSON.

Constraints:
- Returns plain Markdown bullets
- No JSON schema required

Output:
- plain Markdown 3-bullet executive summary

"""