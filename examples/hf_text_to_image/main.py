import torch
from diffusers import DiffusionPipeline
generator = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2", use_safetensors=True)
image = generator("Image for a robot ad").images[0]

image.save("robot_ad.jpg")
# substrate env are short lived after you code is run the output is not kept
# so you need to upload your image to a file storage
