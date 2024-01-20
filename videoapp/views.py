import requests
from django.shortcuts import render
import openai
from imagesapp.models import Lists
import os
from gtts import gTTS
import moviepy.editor as mp
from .models import Video
from django.core.files import File
import glob
import shutil
import dropbox

access_token = {"YOUR_DROPBOX_API_KEY"}
dbx = dropbox.Dropbox(access_token)

# Create your views here.

def audio_generator(story_list):
    n = 0
    audio_filenames = []
    # create the folder if it doesn't exist
    folder_path = "./audio"
    os.makedirs(folder_path, exist_ok=True)

    for text in story_list:
        n = n + 1
        # Language in which you want to convert
        language = 'en'
        # Create a `gTTS` object with the text and language
        myobj = gTTS(text=text, lang=language, slow=False)

        # create a unique filename for the audio file with folder path
        audio_filename = os.path.join(folder_path, f"output{n}.mp3")
        audio_filenames.append(audio_filename)

        # save the audio to a file
        myobj.save(audio_filename)

    return audio_filenames


def images_downloader(url_list):
    image_filenames = []
    # create the folder if it doesn't exist
    folder_path = "./imagez"
    os.makedirs(folder_path, exist_ok=True)

    for i, url in enumerate(url_list):
        response = requests.get(url)
        file_path = os.path.join(folder_path, f"{i + 1}.jpg")
        image_filenames.append(file_path)
        with open(file_path, "wb") as f:
            f.write(response.content)

    return image_filenames


def movie(request):
    # if request.method == "POST":
    # Retrieve the latest GeneratedStory object from the database
    latest_story = Lists.objects.latest('created_at')

    # Split the url_list and story_list strings into lists
    url_list = latest_story.url_list.split('\n')
    story_list = latest_story.story_list.split('\n')

    audio_files = audio_generator(story_list)
    images_file = images_downloader(url_list)
    folder_path = "./movie"
    os.makedirs(folder_path, exist_ok=True)

    clips = []
    i = 0
    for image_file in images_file:
        # image_path = os.path.join(IMAGE_DIR, image_file)
        # audio_path = os.path.join(AUDIO_DIR, audio_files[i])
        audio = mp.AudioFileClip(audio_files[i])
        i = i + 1
        duration = audio.duration
        clip = mp.ImageClip(image_file, duration=duration)
        clip = clip.set_audio(audio)
        clips.append(clip)

    final_clip = mp.concatenate_videoclips(clips)
    final_clip.write_videofile(os.path.join(folder_path, 'output.mp4'), fps=24)

    # Specify the local path and remote path for the video file
    local_path = os.path.join(folder_path, 'output.mp4')
    remote_path = '/video.mp4'

    # # Upload the video file
    # with open(local_path, 'rb') as f:
    #     dbx.files_upload(f.read(), remote_path, mode=dropbox.files.WriteMode.overwrite)
    #
    # # Create a shared link for the uploaded file
    # shared_link = dbx.sharing_create_shared_link(remote_path)
    #
    # # Extract the URL from the shared link
    # url = shared_link.url
    #
    # # Modify the URL to create a direct download link
    # direct_download_url = url.replace('www.dropbox.com', 'dl.dropboxusercontent.com')
    #
    # print("Video URL:", direct_download_url)

    # Generate video file
    latest_video_file_path = max(glob.glob(os.path.join(folder_path, "*.mp4")), key=os.path.getctime)

    # Create new Video instance
    video = Video(name="My Generated Video")

    # Set video file
    with open(latest_video_file_path, 'rb') as f:
        video.video_file.save(os.path.basename(latest_video_file_path), File(f))

    # Save Video instance in the database
    video.save()

    return render(request, "videoapp/video.html", {"movie": remote_path})

# return render(request, "videoapp/video.html")
