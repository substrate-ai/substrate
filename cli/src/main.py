import torch
import os

print(2+2)

print(torch.__version__)
print("cuda", torch.cuda.is_available())

# run the nvidia-smi cmd in the terminal
# !nvidia-smi

os.system('nvidia-smi')

print(torch.version.cuda)
