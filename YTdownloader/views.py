from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import yt_dlp
import uuid

from .logger import MyLogger

# Create your views here.
class DownloadYouTubeVideo(APIView):
    def post(self, request):
        url = request.data.get('url')
        quality = request.data.get('quality', 'best') #default is best if not provided
        download_type = request.data.get('type', 'both')

        if not url:
            return Response({'error': 'No URL provided'}, status=400)
        
        logger = MyLogger()

        #UUID to append with the title
        unique_id = str(uuid.uuid4())

        #selecting the download type
        if download_type == 'video':
            ydl_opts = {
                'format': f'bestvideo[height<={quality}]',
                'outtmpl': f'downloads/%(title)s--{unique_id}.%(ext)s',
                'noplaylist': True,  # Avoid downloading playlists if the URL points to one
                'logger': logger,
            }
        elif download_type == 'audio':
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': f'downloads/%(title)s--{unique_id}.%(ext)s',
                'noplaylist': True,
                'logger': logger,
            }
        else:  # 'both'
            ydl_opts = {
                'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
                'outtmpl': f'downloads/%(title)s--{unique_id}.%(ext)s',
                'noplaylist': True,
                'logger': logger,
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # print(f'Downloading video to: downloads/{title}.{ext}')
                ydl.download([url])
            return Response({'success': 'Video downloaded successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        

class DownloadFacebookVideo(APIView):
    def post(self, request):
        url = request.data.get('url')
        download_type = request.data.get('type', 'video')  # Default is 'video'

        if not url:
            return Response({'error': 'No URL provided'}, status=400)

        logger = MyLogger()

        # UUID to append with the title
        unique_id = str(uuid.uuid4())

        # Set up the options based on the download type
        if download_type == 'video':
            ydl_opts = {
                'format': 'bestvideo',
                'outtmpl': f'downloads/facebook/%(title)s--{unique_id}.%(ext)s',
                'noplaylist': True,
                'logger': logger,
            }
        elif download_type == 'audio':
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': f'downloads/facebook/%(title)s--{unique_id}.%(ext)s',
                'noplaylist': True,
                'logger': logger,
            }
        else:  # Default to video
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'downloads/facebook/%(title)s--{unique_id}.%(ext)s',
                'noplaylist': True,
                'logger': logger,
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return Response({'success': 'Video downloaded successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class DownloadPrivateFacebookVideos(APIView):
    def scrape_url_from_page_source(self, html_source):
        import re

        # Use a regular expression to find all base_url entries
        matches = re.findall(r'"base_url"\s*:\s*"([^"]+)"', html_source)

        # Remove backslashes and create a list of cleaned URLs
        cleaned_urls = [url.replace('\\', '') for url in matches]

        # Output the list of base URLs
        print("Base URLs found:", cleaned_urls)
        return cleaned_urls