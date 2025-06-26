from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    """Category untuk mengelompokkan courses (misal: Matematika, Fisika, dll)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)  # Font awesome icon class
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Course(models.Model):
    """Model untuk course (misal: Kalkulus, Aljabar Linear, dll)"""
    DIFFICULTY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Deskripsi singkat untuk preview")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    
    # Course metadata
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='BEGINNER')
    duration_hours = models.IntegerField(help_text="Estimasi durasi course dalam jam")
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    
    # Status dan visibilitas
    is_published = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=True, help_text="Apakah course ini memerlukan subscription")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO dan metadata
    meta_keywords = models.CharField(max_length=300, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})
    
    @property
    def total_videos(self):
        return self.videos.count()
    
    @property
    def total_duration_minutes(self):
        """Total durasi semua video dalam course (dalam menit)"""
        return self.videos.aggregate(
            total=models.Sum('duration_minutes')
        )['total'] or 0

class Video(models.Model):
    """Model untuk video dalam course"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    
    # Video metadata
    order = models.PositiveIntegerField(help_text="Urutan video dalam course")
    duration_minutes = models.PositiveIntegerField(help_text="Durasi video dalam menit")
    
    # File video - bisa pakai beberapa opsi:
    video_file = models.FileField(upload_to='courses/videos/', blank=True, null=True, help_text="Upload file video")
    video_url = models.URLField(blank=True, null=True, help_text="URL video (YouTube, Vimeo, dll)")
    
    # Thumbnail video
    thumbnail = models.ImageField(upload_to='courses/video_thumbnails/', blank=True, null=True)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_preview = models.BooleanField(default=False, help_text="Video preview yang bisa dilihat tanpa subscription")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course', 'order']
        unique_together = ['course', 'slug']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'course_slug': self.course.slug, 'video_slug': self.slug})

class UserProgress(models.Model):
    """Track progress user untuk setiap video"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    # Progress tracking
    is_completed = models.BooleanField(default=False)
    watch_time_seconds = models.PositiveIntegerField(default=0, help_text="Waktu menonton dalam detik")
    completion_percentage = models.FloatField(default=0.0, help_text="Persentase video yang sudah ditonton")
    
    # Timestamps
    first_watched_at = models.DateTimeField(auto_now_add=True)
    last_watched_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'video']
        ordering = ['-last_watched_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.video.title}"
    
    def mark_completed(self):
        """Mark video as completed"""
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
            self.completion_percentage = 100.0
            self.save()

class CourseEnrollment(models.Model):
    """Track enrollment user ke course"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
    
    @property
    def progress_percentage(self):
        """Hitung persentase progress course"""
        total_videos = self.course.videos.filter(is_published=True).count()
        if total_videos == 0:
            return 0
        
        completed_videos = UserProgress.objects.filter(
            user=self.user,
            course=self.course,
            is_completed=True
        ).count()
        
        return (completed_videos / total_videos) * 100
