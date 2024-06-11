from django.http import JsonResponse
from django.views import View
from main import generate_chapter_titles
from timestamp.models import Video


class GenerateTitlesView(View):
    def get(self, request, video_id):
        # Always generate the chapter titles and store them in the database
        titles = generate_chapter_titles(video_id)
        Video.objects.create(video_id=video_id, chapter_titles=titles)
        return JsonResponse(titles, safe=False)
