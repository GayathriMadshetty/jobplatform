from django.conf import settings
from django.db import models
from . import ai

class Job(models.Model):
    TYPES = [("FT","Full-time"),("PT","Part-time"),("CT","Contract"),("IN","Internship")]
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    job_type = models.CharField(max_length=2, choices=TYPES, default="FT")
    remote = models.BooleanField(default=False)
    salary = models.CharField(max_length=60, blank=True)
    skills = models.CharField(max_length=300, blank=True, help_text="Comma separated")
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    posted = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-posted"]
    def __str__(self): return f"{self.title} @ {self.company}"
    @property
    def skill_list(self): return [s.strip().lower() for s in self.skills.split(",") if s.strip()]
    @property
    def text(self): return f"{self.title} {self.title} {self.skills} {self.company} {self.location} {self.description}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=150, blank=True)
    resume_text = models.TextField(blank=True)
    skills = models.CharField(max_length=300, blank=True)
    @property
    def skill_list(self): return [s.strip().lower() for s in self.skills.split(",") if s.strip()]
    def save(self, *a, **k):  # auto-extract skills from resume
        found = set(self.skill_list) | set(ai.extract_skills(self.resume_text))
        self.skills = ", ".join(sorted(found)); super().save(*a, **k)

class Application(models.Model):
    STATUS = [("applied","Applied"),("review","In review"),("interview","Interview"),("offer","Offer"),("rejected","Rejected")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cover_note = models.TextField(blank=True)
    match_score = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS, default="applied")
    applied_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ("user","job"); ordering = ["-applied_at"]
