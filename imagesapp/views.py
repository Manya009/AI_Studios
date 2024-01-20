from django.shortcuts import render
import openai
from storyapp.models import GeneratedStory
from .models import Lists
import time

openai.api_key = {"YOUR_API_KEY"}


def images_generator(pro):
    while True:
        try:

            image_generated = openai.Image.create(prompt=pro, n=1, size="1024x1024")
            url = image_generated['data'][0]['url']
            return url

        except openai.error.OpenAIError as e:
            error_message = str(e)
            if "Rate limit" in error_message:
                print("Rate limit exceeded. Waiting for 60 seconds...")
                time.sleep(60)
                # You might want to retry the API call after waiting
            else:
                # Handle other OpenAI API errors
                print(f"OpenAI API error: {error_message}")

# check if last character is a full stop
def jay_s(story_list):
    generated_urls = []
    im = 0
    for pro in story_list:
        im += 1
        print(im)
        if im == 3 or 5 or 7 or 9 or 11 or 13:
            time.sleep(10)
            url = images_generator(pro)
        else:
            url = images_generator(pro)
        generated_urls.append(url)
        # generated_url = Images(image_link=url)
        # generated_url.save()

    return generated_urls


def homie(request):
    if request.method == "POST":
        last_story = GeneratedStory.objects.latest('created_at')
        latest_story = last_story.generated_text
        story = str(latest_story)
        print(story)
        if story[-1] == '.':
            story_list = story.split(".")
        else:
            story_list = story[:-1].split(".")
        story_list = [s.strip() for s in story_list]  # remove whitespace from each string
        if ";" in story:
            story_list = [s for sl in story_list for s in sl.split(";")]

        story_list = list(filter(lambda x: x != "", story_list))
        url_list = jay_s(story_list)
        zipped_list = list(zip(story_list, url_list))

        # Convert the lists to strings with each element separated by a newline character
        url_list_str = '\n'.join(url_list)
        story_list_str = '\n'.join(story_list)

        # Create a new Story object and save it to the database
        new_story = Lists.objects.create(url_list=url_list_str, story_list=story_list_str)

        return render(request, "imagesapp/images.html", {'zipped_list': zipped_list})
    return render(request, "imagesapp/images.html")

