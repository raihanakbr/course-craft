from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Course, Video, UserProgress, CourseEnrollment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'course_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = 'Total Courses'

class VideoInline(admin.TabularInline):
    model = Video
    extra = 0
    fields = ['title', 'slug', 'order', 'duration_minutes', 'is_published', 'is_preview']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'difficulty', 'is_published', 
        'is_premium', 'video_count', 'total_duration', 'created_at'
    ]
    list_filter = ['category', 'difficulty', 'is_published', 'is_premium', 'created_at']
    search_fields = ['title', 'description', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [VideoInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'difficulty')
        }),
        ('Content', {
            'fields': ('short_description', 'description', 'thumbnail')
        }),
        ('Settings', {
            'fields': ('duration_hours', 'is_published', 'is_premium')
        }),
        ('SEO', {
            'fields': ('meta_keywords',),
            'classes': ('collapse',)
        })
    )
    
    def video_count(self, obj):
        return obj.total_videos
    video_count.short_description = 'Videos'
    
    def total_duration(self, obj):
        duration = obj.total_duration_minutes
        hours = duration // 60
        minutes = duration % 60
        return f"{hours}h {minutes}m"
    total_duration.short_description = 'Duration'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'course', 'order', 'duration_minutes', 
        'is_published', 'is_preview', 'video_source', 'created_at'
    ]
    list_filter = ['course', 'is_published', 'is_preview', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['course', 'order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'title', 'slug', 'description')
        }),
        ('Video Content', {
            'fields': ('video_file', 'video_url', 'thumbnail')
        }),
        ('Settings', {
            'fields': ('order', 'duration_minutes', 'is_published', 'is_preview')
        })
    )
    
    def video_source(self, obj):
        if obj.video_file:
            return format_html('<span style="color: green;">File</span>')
        elif obj.video_url:
            return format_html('<span style="color: blue;">URL</span>')
        else:
            return format_html('<span style="color: red;">No Source</span>')
    video_source.short_description = 'Source'

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'video', 'course', 'completion_percentage', 
        'is_completed', 'last_watched_at'
    ]
    list_filter = ['is_completed', 'course', 'last_watched_at']
    search_fields = ['user__username', 'video__title', 'course__title']
    readonly_fields = ['first_watched_at', 'completed_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'video', 'course')

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'progress_percent', 'is_active', 'enrolled_at']
    list_filter = ['is_active', 'course', 'enrolled_at']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['enrolled_at']
    
    def progress_percent(self, obj):
        progress = obj.progress_percentage
        color = 'green' if progress == 100 else 'orange' if progress > 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, progress
        )
    progress_percent.short_description = 'Progress'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'course')
