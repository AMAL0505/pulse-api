from django.contrib import admin
from .models import Course, Lesson, Enrollment


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1  

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor')
    search_fields = ('title', 'category', 'instructor__username')
    list_filter = ('category',)
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'content_type')
    list_filter = ('content_type', 'course')
    search_fields = ('title', 'course__title')

from django.utils.html import format_html

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress_display')
    list_filter = ('course', 'student')
    search_fields = ('student__username', 'student__email', 'course__title')

    def progress_display(self, obj):
        percent = int(obj.progress)
        color = "green" if percent >= 80 else "orange" if percent >= 50 else "red"
        return format_html(
            '<div style="width: 100px; background-color: lightgray;">'
            '<div style="width: {}%; background-color: {}; text-align: center; color: white;">{}%</div>'
            '</div>', percent, color, percent
        )

    progress_display.short_description = "Progress"
