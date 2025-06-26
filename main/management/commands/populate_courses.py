from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import Category, Course, Video

class Command(BaseCommand):
    help = 'Populate sample course data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample courses and videos...')
        
        # Create Categories
        math_category, created = Category.objects.get_or_create(
            name='Matematika',
            defaults={
                'slug': 'matematika',
                'description': 'Kursus matematika dari dasar hingga mahir',
                'icon': 'fas fa-calculator'
            }
        )
        
        physics_category, created = Category.objects.get_or_create(
            name='Fisika',
            defaults={
                'slug': 'fisika',
                'description': 'Kursus fisika untuk pemahaman konsep dan aplikasi',
                'icon': 'fas fa-atom'
            }
        )
        
        # Create Kalkulus Course
        kalkulus_course, created = Course.objects.get_or_create(
            title='Kalkulus Dasar',
            defaults={
                'slug': 'kalkulus-dasar',
                'category': math_category,
                'short_description': 'Pelajari konsep dasar kalkulus dari limit hingga integral',
                'description': '''
                Kursus Kalkulus Dasar ini dirancang untuk memberikan pemahaman yang solid tentang konsep-konsep fundamental dalam kalkulus. 
                Anda akan mempelajari limit, turunan, dan integral beserta aplikasinya dalam kehidupan sehari-hari.
                
                Topik yang akan dibahas:
                - Sistem Bilangan Real
                - Konsep Limit dan Kontinuitas
                - Turunan dan Aplikasinya
                - Integral Tak Tentu dan Tertentu
                - Aplikasi Integral dalam Geometri
                ''',
                'difficulty': 'BEGINNER',
                'duration_hours': 20,
                'is_published': True,
                'is_premium': True,
                'meta_keywords': 'kalkulus, matematika, limit, turunan, integral'
            }
        )
        
        # Create Videos for Kalkulus
        kalkulus_videos = [
            {
                'title': 'Pengenalan Sistem Bilangan Real',
                'description': 'Memahami konsep bilangan real, sifat-sifatnya, dan operasi dasar',
                'duration_minutes': 45,
                'order': 1,
                'is_preview': True
            },
            {
                'title': 'Pertidaksamaan dan Nilai Mutlak',
                'description': 'Menyelesaikan pertidaksamaan linear dan kuadrat serta nilai mutlak',
                'duration_minutes': 50,
                'order': 2
            },
            {
                'title': 'Konsep Limit Fungsi',
                'description': 'Memahami definisi limit dan cara menghitung limit fungsi',
                'duration_minutes': 60,
                'order': 3
            },
            {
                'title': 'Teorema Limit dan Kontinuitas',
                'description': 'Memahami teorema-teorema limit dan konsep kontinuitas fungsi',
                'duration_minutes': 55,
                'order': 4
            },
            {
                'title': 'Pengenalan Turunan',
                'description': 'Definisi turunan dan interpretasi geometris',
                'duration_minutes': 50,
                'order': 5
            },
            {
                'title': 'Aturan-aturan Diferensiasi',
                'description': 'Aturan rantai, hasil kali, dan hasil bagi dalam diferensiasi',
                'duration_minutes': 65,
                'order': 6
            },
            {
                'title': 'Aplikasi Turunan dalam Optimasi',
                'description': 'Menggunakan turunan untuk mencari maksimum dan minimum fungsi',
                'duration_minutes': 70,
                'order': 7
            },
            {
                'title': 'Pengenalan Integral Tak Tentu',
                'description': 'Konsep anti-turunan dan integral tak tentu',
                'duration_minutes': 55,
                'order': 8
            },
            {
                'title': 'Teknik Integrasi Dasar',
                'description': 'Integrasi substitusi dan integrasi parsial',
                'duration_minutes': 75,
                'order': 9
            },
            {
                'title': 'Integral Tertentu dan Aplikasinya',
                'description': 'Teorema dasar kalkulus dan aplikasi integral dalam menghitung luas',
                'duration_minutes': 80,
                'order': 10
            }
        ]
        
        for video_data in kalkulus_videos:
            video, created = Video.objects.get_or_create(
                course=kalkulus_course,
                title=video_data['title'],
                defaults={
                    'slug': slugify(video_data['title']),
                    'description': video_data['description'],
                    'duration_minutes': video_data['duration_minutes'],
                    'order': video_data['order'],
                    'is_published': True,
                    'is_preview': video_data.get('is_preview', False)
                }
            )
            if created:
                self.stdout.write(f'  Created video: {video.title}')
        
        # Create Aljabar Linear Course
        aljabar_course, created = Course.objects.get_or_create(
            title='Aljabar Linear',
            defaults={
                'slug': 'aljabar-linear',
                'category': math_category,
                'short_description': 'Memahami konsep vektor, matriks, dan transformasi linear',
                'description': '''
                Kursus Aljabar Linear ini membahas konsep-konsep fundamental dalam aljabar linear
                yang sangat penting untuk matematika lanjut, fisika, dan teknik.
                
                Topik yang akan dibahas:
                - Vektor dan Operasinya
                - Sistem Persamaan Linear
                - Matriks dan Determinan
                - Ruang Vektor dan Basis
                - Transformasi Linear
                - Nilai Eigen dan Vektor Eigen
                ''',
                'difficulty': 'INTERMEDIATE',
                'duration_hours': 25,
                'is_published': True,
                'is_premium': True,
                'meta_keywords': 'aljabar linear, vektor, matriks, transformasi linear'
            }
        )
        
        # Create Fisika Dasar Course
        fisika_course, created = Course.objects.get_or_create(
            title='Fisika Dasar I - Mekanika',
            defaults={
                'slug': 'fisika-dasar-mekanika',
                'category': physics_category,
                'short_description': 'Pelajari konsep dasar mekanika klasik dan aplikasinya',
                'description': '''
                Kursus Fisika Dasar I ini fokus pada mekanika klasik, fondasi dari semua cabang fisika.
                Anda akan mempelajari gerak benda, gaya, energi, dan momentum.
                
                Topik yang akan dibahas:
                - Kinematika Gerak Lurus
                - Kinematika Gerak Melingkar
                - Dinamika - Hukum Newton
                - Kerja dan Energi
                - Momentum dan Impuls
                - Gerak Rotasi
                ''',
                'difficulty': 'BEGINNER',
                'duration_hours': 30,
                'is_published': True,
                'is_premium': True,
                'meta_keywords': 'fisika, mekanika, kinematika, dinamika, energi'
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- Categories: {Category.objects.count()}\n'
                f'- Courses: {Course.objects.count()}\n'
                f'- Videos: {Video.objects.count()}'
            )
        )
