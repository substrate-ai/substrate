# GPU substrate

Modify dockerfile such that pytorch detect the GPU
**NEEDS TO BE DONE ON A CUDA LAPTOP (YOUR HP LAPTOP)**

```
docker build . -t gpu-substrate
```

```
docker run gpu-substrate  
```

You can evaluate task sucess when you get KJ you did it!!! in green in the terminal

## Details
Please don't add index to pip install. Indeed, we want the installation to be as general as possible
Thus we need the user to specify index (if any), however you could modify the `requirements.txt` to be more precise

Ideally don't use conda but if needed you can, we want the image to be as small as possible

## Ressources
https://saturncloud.io/blog/how-to-install-pytorch-on-the-gpu-with-docker/
https://dev.to/ordigital/nvidia-525-cuda-118-python-310-pytorch-gpu-docker-image-1l4a
https://saturncloud.io/blog/how-to-conda-install-cudaenabled-pytorch-in-a-docker-container/
https://www.reddit.com/r/docker/comments/unlqlr/use_cuda_within_a_docker_container/
https://blog.ceshine.net/post/replicate-conda-environment-in-docker/
https://blog.roboflow.com/use-the-gpu-in-docker/
https://jdhao.github.io/2022/02/09/dependency-hell-build-torch-GPU-docker-container/
https://towardsdatascience.com/a-complete-guide-to-building-a-docker-image-serving-a-machine-learning-system-in-production-d8b5b0533bde