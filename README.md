# SmartHire – AI-Enhanced Job Search Platform (Django)
```
pip install -r requirements.txt
python manage.py makemigrations jobs && python manage.py migrate
python manage.py seed_jobs
python manage.py createsuperuser   # optional
python manage.py runserver
```
Open http://127.0.0.1:8000. Sign up, paste your resume in Profile, then see match scores, "For you" recommendations and skill gaps.

## AI features (jobs/ai.py, no external dependencies)
- TF-IDF + cosine similarity natural-language job search
- Resume skill extraction (50+ skills; extend `SKILLS`)
- Resume↔job match score (65% skill overlap + 35% text similarity) with matched/missing skills
- Personalised recommendations, similar-job suggestions, applicants auto-ranked for employers
Upgrade path: swap `ai.rank`/`ai.match` for sentence-transformers or an LLM API.
"# job-search-platform" 
