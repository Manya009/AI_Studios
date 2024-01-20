from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from .models import GeneratedStory
import openai
path = './saved_models/Story_generation_text'

tokenizer = AutoTokenizer.from_pretrained(path)
model = AutoModelForCausalLM.from_pretrained(path)


# Create your views here.
def home(request):
    return render(request, "storyapp/home.html")


def story_predictor(request):
    if request.method == "POST":
        prompt = request.POST['prompt']

        input_ids = tokenizer.encode(prompt, return_tensors='pt')
        max_length = 200
        output = model.generate(input_ids, max_length=max_length, do_sample=True)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

        generated_story = GeneratedStory(generated_text=generated_text)
        generated_story.save()

        return render(request, "storyapp/page.html", {'reslut': str(generated_text)})
    return render(request, "storyapp/page.html")
