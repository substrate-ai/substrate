import torch
import os
from time import sleep


def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
 
 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

print(2+2)

print(torch.__version__)
print("cuda", torch.cuda.is_available())

# run the nvidia-smi cmd in the terminal
# !nvidia-smi

print(torch.version.cuda)

if (torch.cuda.is_available()):
    print(torch.cuda.get_device_name(0))

    prGreen("KJ you did it!!!")
else:
    prRed("Well try, but still did not work")


# os.system('nvidia-smi')

# while True:
#     sleep(1)
#     print("sleeping")
