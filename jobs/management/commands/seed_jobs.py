from django.core.management.base import BaseCommand
from jobs.models import Job
DATA = [
 ("Backend Python Developer","Acme Cloud","Hyderabad","FT",False,"₹18-28 LPA","python, django, postgresql, docker, rest","Build scalable REST APIs with Django and PostgreSQL. Deploy with Docker on AWS."),
 ("Machine Learning Engineer","DataNova","Bengaluru","FT",True,"₹25-40 LPA","python, pytorch, machine learning, nlp, aws","Train and deploy NLP models. Strong PyTorch and MLOps experience needed."),
 ("Frontend React Developer","PixelWorks","Remote","CT",True,"$40-60/hr","javascript, react, typescript, figma","Craft responsive UIs in React and TypeScript, collaborating closely with designers."),
 ("Data Analyst","InsightIQ","Pune","FT",False,"₹8-14 LPA","sql, excel, tableau, pandas, data analysis","Analyse business data, build dashboards in Tableau, write SQL and pandas pipelines."),
 ("DevOps Engineer","InfraHive","Chennai","FT",False,"₹20-32 LPA","kubernetes, docker, aws, ci/cd, linux, git","Own CI/CD pipelines and Kubernetes clusters on AWS."),
 ("Full Stack Intern","StartupLab","Hyderabad","IN",True,"₹25k/mo","python, django, react, git","Learn by shipping features across Django backend and React frontend."),
 ("Digital Marketing Manager","BrightReach","Mumbai","FT",False,"₹12-18 LPA","seo, marketing, communication, excel","Lead SEO and campaign strategy, analyse funnel performance."),
 ("Data Scientist","QuantEdge","Remote","FT",True,"₹22-35 LPA","python, scikit-learn, pandas, sql, machine learning","Build predictive models, run experiments, communicate insights to stakeholders."),
]
class Command(BaseCommand):
    def handle(self, *a, **k):
        for t,c,l,jt,r,s,sk,d in DATA:
            Job.objects.get_or_create(title=t, company=c, defaults=dict(location=l,job_type=jt,remote=r,salary=s,skills=sk,description=d))
        self.stdout.write(self.style.SUCCESS(f"{Job.objects.count()} jobs available"))
