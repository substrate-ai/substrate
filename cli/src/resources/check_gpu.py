import torch

assert torch.cuda.is_available(), "Please install CUDA drivers"

print("GPU is available", torch.cuda.get_device_name(0))
