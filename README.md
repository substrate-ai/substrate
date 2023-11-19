<p align="center">
  <a href="https://substrateai.com">
    <img height="150" src="https://github.com/substrate-ai/substrate/assets/32412211/a0c125ad-f6d8-48bd-86f7-7b80d880f3c3" alt="Substrate AI logo">
  </a>
</p>

<h1 align="center">Substrate AI</h1>

<p align="center">
  <i>Deploy your ML code in the cloud in under 5 minutes</i>
</p>

<p align="center">
  <a href="/LICENSE">
    <img alt="License Apache-2.0" src="https://img.shields.io/github/license/substrate-ai/substrate?style=flat-square">
  </a>
</p>

<p align="center">
  <a href="https://substrateai.com">Hosted Platform</a> • <a href="#running-locally">Running Locally</a>
</p>

---

Simplify your ML training on cloud GPUs with Substrate AI. Our platform allows you to set up and run your models quickly, bypassing the usual setup hassles.

## 🚀 Getting Started

### Installation

Install the package:

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

## 🎬 Demo
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
  project_name: Example Project
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
    <video src="https://github.com/substrate-ai/substrate/assets/32412211/7534a6f7-82f5-4ed5-ad55-f8c045df4300"/>
  </div>
</details>

## ✨ Features

- Fully open-source
    - Self-host our platform
- Quick deployment of ML code in the cloud
- No vendor lock-in
- AWS-powered GPUs without extra cost
More features on the horizon

## 💡 Examples

Explore example projects in our [example folder](https://github.com/substrate-ai/substrate/tree/main/examples)

## 📚 Documentation

Access our [documentation](https://docs.substrateai.com/)

## 🗺️ Roadmap

- [x] v0 launched
- [ ] Filesystem integration
- [ ] Remote image building
- [ ] Cloud job analytics
- [ ] Inference support
- [ ] Spot training
- [ ] Decreased compute cost (as we do not profit from computing, our focus is minimizing expenses)

## 🖥  Running Locally

Stay tuned for detailed instructions

## 🌟 Interested?

Please leave us a star and/or sign up for the [hosted version](https://substrateai.com)
