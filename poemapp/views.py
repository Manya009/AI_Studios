from django.shortcuts import render
from django.shortcuts import render
import torch
import openai
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from tqdm import tqdm, trange
import torch.nn.functional as F

path = './saved_models/poem_generator.pt'

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = torch.load(path, map_location=torch.device('cpu'))


def generate(model, tokenizer, poem_prompt, entry_count=1, entry_length=120, top_p=0.8, temperature=1., ):
    model.eval()
    generated_num = 0
    generated_list = []

    filter_value = -float("Inf")

    with torch.no_grad():

        for entry_idx in trange(entry_count):

            entry_finished = False
            generated = torch.tensor(tokenizer.encode(poem_prompt)).unsqueeze(0)

            for i in range(entry_length):
                outputs = model(generated, labels=generated)
                loss, logits = outputs[:2]
                logits = logits[:, -1, :] / (temperature if temperature > 0 else 1.0)

                sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

                sorted_indices_to_remove = cumulative_probs > top_p
                sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[
                                                    ..., :-1
                                                    ].clone()
                sorted_indices_to_remove[..., 0] = 0

                indices_to_remove = sorted_indices[sorted_indices_to_remove]
                logits[:, indices_to_remove] = filter_value

                next_token = torch.multinomial(F.softmax(logits, dim=-1), num_samples=1)
                generated = torch.cat((generated, next_token), dim=1)

                if next_token in tokenizer.encode("<|endoftext|>"):
                    entry_finished = True

                if entry_finished:
                    generated_num = generated_num + 1

                    output_list = list(generated.squeeze().numpy())
                    output_text = tokenizer.decode(output_list)
                    generated_list.append(output_text)
                    break

            if not entry_finished:
                output_list = list(generated.squeeze().numpy())
                output_text = f"{tokenizer.decode(output_list)}<|endoftext|>"
                generated_list.append(output_text)

    return generated_list


def clean_poem(text):
    # Find the last full stop in the text
    last_full_stop = text.rfind(".")

    # If there is a full stop, use it to split the text
    if last_full_stop != -1:
        text = text[:last_full_stop + 1]

    new_text = ""
    for char in text:
        if char in [",", ".", "?", "!"]:
            new_text += char + "\n"
        else:
            new_text += char
    return new_text


# Function to generate multiple sentences. Test data should be a dataframe
def text_generation(poem_prompt):
    # generated_lyrics = []
    generated_lyrics = generate(model.to('cpu'), tokenizer, poem_prompt, entry_count=1)
    generated_lyrics = clean_poem(generated_lyrics[0])
    return generated_lyrics


def poem_predictor(request):
    if request.method == "POST":
        poem_prompt = request.POST['poem_prompt']
        generated_lyrics = text_generation(poem_prompt)

        return render(request, "poemapp/page01.html", {'reslut': str(generated_lyrics)})
    return render(request, "poemapp/page01.html")
