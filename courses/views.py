from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Course, Lesson, Enrollment
from .serializers import (
    CourseSerializer, 
    LessonSerializer, 
    EnrollmentSerializer,
    CourseProgressSerializer,
    UserCourseSerializer
)
from .permissions import IsInstructor, IsStudent, IsInstructorOrReadOnly
from accounts.models import User

class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsInstructor]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Add basic filtering capability
        category = self.request.query_params.get('category')
        queryset = Course.objects.all()
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsInstructorOrReadOnly]  # Only instructor can update/delete

class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsInstructor]

class EnrollmentCreateView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class UserCoursesView(generics.ListAPIView):
    serializer_class = UserCourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Course.objects.filter(enrollment__student=user)
        else:  # instructor
            return Course.objects.filter(instructor=user)

def home(request):
    return render(request, 'courses/home.html')

class InstructorCourseListView(generics.ListAPIView):
    serializer_class = UserCourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)