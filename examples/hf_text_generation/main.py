from transformers import pipeline

pipe = pipeline("text-generation", model = 'gpt2')
print(pipe("Hey, I am "))