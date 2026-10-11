from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from . import ai
from .forms import JobForm, ProfileForm, ApplyForm
from .models import Job, Profile, Application

def _profile(user): return Profile.objects.get_or_create(user=user)[0]

def job_list(request):
    qs = Job.objects.all()
    if t := request.GET.get("type"): qs = qs.filter(job_type=t)
    if request.GET.get("remote"): qs = qs.filter(remote=True)
    if loc := request.GET.get("location"): qs = qs.filter(location__icontains=loc)
    q = request.GET.get("q", "").strip()
    rows = [{"job": j, "relevance": round(s * 100)} for j, s in ai.rank(q, qs)] if q else [{"job": j} for j in qs]
    if request.user.is_authenticated:
        p = _profile(request.user)
        for r in rows: r["match"] = ai.match(p.resume_text, p.skill_list, r["job"])[0]
    return render(request, "jobs/job_list.html", {"rows": rows, "q": q, "types": Job.TYPES})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk); ctx = {"job": job}
    if request.user.is_authenticated:
        p = _profile(request.user)
        ctx["score"], ctx["matched"], ctx["missing"] = ai.match(p.resume_text, p.skill_list, job)
        ctx["applied"] = Application.objects.filter(user=request.user, job=job).exists()
        ctx["form"] = ApplyForm()
    similar = [j for j, _ in ai.rank(job.text, Job.objects.exclude(pk=pk))[:3]]
    ctx["similar"] = similar
    return render(request, "jobs/job_detail.html", ctx)

@login_required
def apply(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        p = _profile(request.user)
        score = ai.match(p.resume_text, p.skill_list, job)[0]
        _, created = Application.objects.get_or_create(user=request.user, job=job,
            defaults={"cover_note": request.POST.get("cover_note", ""), "match_score": score})
        messages.success(request, "Application submitted!" if created else "You already applied.")
    return redirect("job_detail", pk=pk)

@login_required
def recommendations(request):
    p = _profile(request.user)
    if not p.resume_text and not p.skills:
        messages.info(request, "Add your resume or skills to get recommendations."); return redirect("profile")
    return render(request, "jobs/recommendations.html", {"recs": ai.recommend(p, Job.objects.all())})

@login_required
def profile(request):
    p = _profile(request.user)
    form = ProfileForm(request.POST or None, instance=p)
    if form.is_valid(): form.save(); messages.success(request, "Profile updated; skills re-extracted."); return redirect("profile")
    return render(request, "jobs/profile.html", {"form": form})

@login_required
def my_applications(request):
    return render(request, "jobs/applications.html", {"apps": Application.objects.filter(user=request.user).select_related("job")})

@login_required
def post_job(request):
    form = JobForm(request.POST or None)
    if form.is_valid():
        job = form.save(commit=False); job.owner = request.user; job.save(); return redirect("job_detail", pk=job.pk)
    return render(request, "jobs/post_job.html", {"form": form})

@login_required
def employer_dashboard(request):
    jobs = Job.objects.filter(owner=request.user)
    apps = Application.objects.filter(job__in=jobs).select_related("user", "job").order_by("-match_score")
    if request.method == "POST":
        a = get_object_or_404(apps, pk=request.POST["app_id"]); a.status = request.POST["status"]; a.save()
        return redirect("employer")
    return render(request, "jobs/employer.html", {"apps": apps, "statuses": Application.STATUS})

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid(): login(request, form.save()); return redirect("profile")
    return render(request, "registration/register.html", {"form": form})
