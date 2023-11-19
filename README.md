<p align="center">
  <a href="https://datasaurus.app">
    <img height="150" src="https://github.com/substrate-ai/substrate/assets/32412211/a0c125ad-f6d8-48bd-86f7-7b80d880f3c3" alt="logo">
  </a>
</p>

<h1 align="center">
  Substrate AI
</h1>

<p align="center">
  <i>Get your ML code up and running in the cloud in less than 5 minutes</i>
</p>

<p align="center">
  <a href="/LICENSE"><img alt="License Apache-2.0" src="https://img.shields.io/github/license/substrate-ai/substrate?style=flat-square"></a>
</p>

<p align="center">
  <a href="https://substrateai.com">Hosted Platfrom</a> - <a href="#running-locally">Running Locally</a>
</p>

<br>
You want to run your ML training on cloud GPU, however, it takes forever to set up. No more, using our platform to get up and running in a couple of minutes. 
<br>
<be>

## Getting Started
Install the package

```
pip install substrate-ai
```

Configure your folder to use substrate

```
substrate-ai init
```

Run your code on the cloud

```
substrate-ai run
```

## Demo
<details>
  <summary>View Demo</summary>

  Initialize your folder to be able to run with Substrate
  ```
  substrate-ai init
  ```

  Create a file with some Python code 
  ```py
  print("Welcome to substrate!")
  ```

  modify your `substrate.yaml` if necessary
  ```yaml
  project_name: basic
  hardware:
  type: cpu
  main_file_location: ./main.py
  ```

  Then run your code
  ```
  substrate-ai run
  ```

  The result
  <div align="center">
    <video src="https://github.com/substrate-ai/substrate/assets/32412211/8b84b8d6-1126-46ff-a469-6dcaef0dc83d"/>
  </div>
</details>

## Features

- Fully open-source
   - You can even run our platform yourself
- Your ml code running in the cloud in a couple of minutes
- No vendor-specific lock-in, we adjust your code to fit our framework, not the other way around
- Selling compute with zero markup
    - we use AWS for our GPUs and sell this computes at the same price as AWS cost
- Run your model on powerful GPUs
And many more features coming soon

## Examples

Look at our example folder for a couple of example projects

## Documentation

Read our extensive documentation on our website https://docs.substrateai.com/

## Roadmap

- [x] v0 launched
- [ ] Filesystem
- [ ] Remote image building
- [ ] Analytics on cloud jobs
- [ ] Inference support (mainly focusing on the ml training pipeline for right now)

## Running Locally

Detailed instructions coming soon. 

## Interested?

If you are interested, please leave us a star and/or sign up for the hosted version on [substrateai.com](https://substrateai.com)
