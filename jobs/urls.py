from django.urls import path
from . import views as v
urlpatterns = [
    path("", v.job_list, name="job_list"), path("job/<int:pk>/", v.job_detail, name="job_detail"),
    path("job/<int:pk>/apply/", v.apply, name="apply"), path("recommended/", v.recommendations, name="recommendations"),
    path("profile/", v.profile, name="profile"), path("applications/", v.my_applications, name="applications"),
    path("post/", v.post_job, name="post_job"), path("employer/", v.employer_dashboard, name="employer"),
    path("register/", v.register, name="register"),
]
