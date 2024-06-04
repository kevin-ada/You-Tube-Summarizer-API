from django.urls import path
from .views import GenerateTitlesView

urlpatterns = [
    path('generate-scripts/<str:video_id>/', GenerateTitlesView.as_view(), name='generate-titles')
]
