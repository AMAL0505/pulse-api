from rest_framework import serializers
from .models import Course, Lesson, Enrollment
from accounts.models import User
from django.core.validators import FileExtensionValidator

class LessonSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)  
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content_type', 'content_url', 'course', 'created_by', 'created_at']
        extra_kwargs = {
            'content_url': {'required': True},
            'course' : {'required' : True}
        }

    def validate(self, data):
        content_type = data.get('content_type')
        content_url = data.get('content_url')

        if content_type == 'video' and not content_url.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Video content must be a valid URL")

        if content_type == 'pdf' and not content_url.endswith('.pdf'):
            raise serializers.ValidationError("PDF content must be a PDF file")

        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    total_students = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
            'image',
            'image_url',
            'description', 
            'category', 
            'instructor', 
            'instructor_name',
            'lessons',
            'total_students',
            'is_enrolled',
        ]
        read_only_fields = ['instructor']
        extra_kwargs = {
            'image': {
                'write_only': True,
                'validators': [
                    FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])
                ]
            }
        }
        
    def get_total_students(self, obj):
        return obj.enrollment_set.count()
    
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'student':
            return obj.enrollment_set.filter(student=request.user).exists()
        return False
    
    def validate_image(self, value):
        if value:
            # 2MB limit
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("Image size too large (max 2MB)")
        return value

class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_description = serializers.CharField(source='course.description', read_only=True)
    course_image = serializers.SerializerMethodField()
    student_name = serializers.CharField(source='student.username', read_only=True)
    instructor_name = serializers.CharField(source='course.instructor.username', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id',
            'student',
            'student_name',
            'course',
            'course_title',
            'course_description',
            'course_image',
            'instructor_name',
            'progress',
            'enrolled_at'
        ]
        read_only_fields = ['student', 'progress', 'enrolled_at']
    
    def get_course_image(self, obj):
        if obj.course.image and hasattr(obj.course.image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.course.image.url)
            return obj.course.image.url
        return None

class CourseProgressSerializer(serializers.ModelSerializer):
    completed_lessons = serializers.SerializerMethodField()
    total_lessons = serializers.SerializerMethodField()
    next_lesson = serializers.SerializerMethodField()
    
    class Meta:
        model = Enrollment
        fields = ['progress', 'completed_lessons', 'total_lessons', 'next_lesson']
        
    def get_completed_lessons(self, obj):
        return obj.completed_lessons.count() if hasattr(obj, 'completed_lessons') else 0
        
    def get_total_lessons(self, obj):
        return obj.course.lessons.count()
    
    def get_next_lesson(self, obj):
        # necxt lesson implement in the future
        return None

class UserCourseSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'progress', 'image_url']
        
    def get_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'student':
            enrollment = Enrollment.objects.filter(course=obj, student=request.user).first()
            return enrollment.progress if enrollment else 0
        return None
    
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None