# timestamp/api/views.py

from django.http import JsonResponse
from django.views import View
from main import generate_chapter_titles
from timestamp.models import Video


class GenerateTitlesView(View):
    def get(self, request, video_id):
        # Check if video_id already exists in the database
        video = Video.objects.filter(video_id=video_id).first()
        if video:
            # If it exists, return the stored chapter titles
            titles = video.chapter_titles
        else:
            # If it doesn't exist, generate the chapter titles and store them in the database
            titles = generate_chapter_titles(video_id)
            Video.objects.create(video_id=video_id, chapter_titles=titles)
        return JsonResponse(titles, safe=False)
