"""
URL configuration for student_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from student_management_app import views,HodView
from student_management_system import settings


urlpatterns = [
    path('demo', views.showDemoPage, name='home'),
    path('', views.showLoginPage),
    path('admin/', admin.site.urls),
    path('loginAction', views.loginAction),
    path('get_user_details', views.GetUserDetail),
    path('logout_user', views.logout_user),
    path('admin_home',HodView.admin_home),
    path('add_staff',HodView.add_staff),
    path('add_staff_save',HodView.add_staff_save),
    path('add_course', HodView.add_course,name="add_course"),
    path('add_course_save', HodView.add_course_save,name="add_course_save"),
    path('add_student', HodView.add_student,name="add_student"),
    path('add_student_save', HodView.add_student_save,name="add_student_save"),
    path('add_subject', HodView.add_subject,name="add_subject"),
    path('add_subject_save', HodView.add_subject_save,name="add_subject_save"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
