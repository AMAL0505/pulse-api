from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/usercourses/', views.InstructorCourseListView.as_view(), name='user-courses'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('lessons/create/', views.LessonCreateView.as_view(), name='lesson-create'),
    path('enroll/', views.EnrollmentCreateView.as_view(), name='enroll'),
]