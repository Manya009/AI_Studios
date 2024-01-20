from django.shortcuts import render

import os
import openai

openai.api_key = {"YOUR_API_KEY"}


def image_generator(request):
    if request.method == "POST":
        pro = request.POST['prompt']

        image_generated = openai.Image.create(
            prompt=pro,
            n=1,
            size="1024x1024"
        )

        url = image_generated['data'][0]['url']

        return render(request, "imageapp/image.html", {'reslut': str(url)})
    return render(request, "imageapp/image.html")
