import torch
import os

import sys
print(sys.path)

from substrateai import filesystem



print(torch.__version__)

if (torch.cuda.is_available()):
    print("CUDA is available")
else:
    print("CUDA is not available")

print(filesystem.ls("baptistecolle"))

# print(os.listdir("/"))
# print()

# # create a hello world file in /substrate
# with open("/substrate/hello_world.txt", "w") as f:
#     f.write("hello world")

# print(os.listdir("/substrate"))

# # read hello world file
# with open("/substrate/hello_world.txt", "r") as f:
#     print(f.read())


# write hello world
