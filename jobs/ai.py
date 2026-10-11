"""Dependency-free AI layer: TF-IDF semantic ranking, skill extraction, resume-job matching."""
import math, re
from collections import Counter

STOP = set("a an the and or of to in for with on at by is are be as we you our will this that from it your have has can".split())
SKILLS = ["python","django","flask","fastapi","java","spring","javascript","typescript","react","vue","angular","node.js",
    "sql","postgresql","mysql","mongodb","redis","docker","kubernetes","aws","azure","gcp","git","ci/cd","rest","graphql",
    "machine learning","deep learning","nlp","pytorch","tensorflow","pandas","numpy","scikit-learn","data analysis",
    "tableau","power bi","excel","c++","go","rust","linux","agile","scrum","figma","ui/ux","seo","marketing","sales","communication"]

def tokens(text):
    return [w for w in re.findall(r"[a-z0-9+#./]+", text.lower()) if w not in STOP and len(w) > 1]

def extract_skills(text):
    low = text.lower()
    return sorted({s for s in SKILLS if re.search(r"(?<![a-z0-9])" + re.escape(s) + r"(?![a-z0-9])", low)})

def _idf(docs):
    df = Counter()
    for d in docs: df.update(set(d))
    n = len(docs)
    return {w: math.log((1 + n) / (1 + c)) + 1 for w, c in df.items()}

def _vec(toks, idf):
    return {w: c * idf.get(w, 1.0) for w, c in Counter(toks).items()}

def _cos(a, b):
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    na, nb = math.sqrt(sum(v*v for v in a.values())), math.sqrt(sum(v*v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0

def rank(query, jobs):
    """Semantic-ish search: TF-IDF cosine similarity between query and each job. Returns [(job, score)]."""
    jobs = list(jobs); q = tokens(query)
    docs = [tokens(j.text) for j in jobs]
    idf = _idf(docs + [q]); qv = _vec(q, idf)
    out = [(j, _cos(qv, _vec(d, idf))) for j, d in zip(jobs, docs)]
    return sorted([x for x in out if x[1] > 0], key=lambda x: -x[1])

def match(resume_text, profile_skills, job):
    """Returns (score 0-100, matched skills, missing skills)."""
    have = set(s.lower() for s in profile_skills) | set(extract_skills(resume_text))
    need = set(job.skill_list) | set(extract_skills(job.text))
    matched, missing = sorted(have & need), sorted(need - have)
    overlap = len(matched) / len(need) if need else 0.5
    q, d = tokens(resume_text), tokens(job.text)
    idf = _idf([q, d]); sim = _cos(_vec(q, idf), _vec(d, idf))
    return round(100 * (0.65 * overlap + 0.35 * min(1, sim * 2))), matched, missing

def recommend(user_profile, jobs, limit=10):
    res = []
    for j in jobs:
        s, m, x = match(user_profile.resume_text, user_profile.skill_list, j)
        res.append({"job": j, "score": s, "matched": m, "missing": x})
    return sorted(res, key=lambda r: -r["score"])[:limit]
