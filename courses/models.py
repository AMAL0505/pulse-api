from django.db import models
from accounts.models import User
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    CONTENT_CHOICES = (
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('text', 'Text'),
    )
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=CONTENT_CHOICES)
    content_url = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lessons_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"