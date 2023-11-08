<p align="center">
  <a href="https://datasaurus.app">
    <img height="150" src="https://github.com/substrate-ai/substrate/assets/32412211/4aad3e0f-670c-452f-a3bc-9e97151acaab" alt="logo">
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
You want to run your ML training on cloud GPU, however, it takes forever to setup. No more, use our platform to get up and running in a couple of minutes. 
<br>
<br>
<p align="center">
 <img width="720" src="https://github.com/datasaurus-ai/datasaurus/assets/32412211/7b9a36dd-9264-4442-ba25-e29a5a1516f3" alt="demo">
</p>

## Features

- Fully open-source
- Your ml code running in the cloud in a couple of minutes
- Selling compute with zero markup
    - we use AWS for our gpus and sell this compute at AWS cost
And many more features coming soon

## Examples

Look at our example folder for a couple of use-cases

## Documentation

https://docs.substrateai.com/

## Roadmap

- [x] v0 launched
- [x] Open-sourced the project (yes, we closed-source before 😣)
- [ ] Filesystem
- [ ] Remote image building
- [ ] Analytics on job
- [ ] Inference support (only training right now)

## Running Locally

Requirement: You need an AWS account

1. Install [NodeJS 20](https://nodejs.org/en/download/current) (earlier versions will very likely work but aren't tested)
2. Install [Supabase](https://supabase.com/docs/guides/cli/local-development) with `npm i supabase --save-dev`
3. Install [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
4. Clone this repository and open it: `git clone https://github.com/substrate-ai/substrate && cd substrate`
5. Install the frontend dependencies: `cd frontend && npm install && cd ..`
6. Install the backend dependencies: `cd backend && virtualenv substrate-backend && source substrate-backend/bin/activate && pip install -r requirements.txt && cd ..`
7. Start Supabase: `cd supabase && supabase start && cd ..`
9. Create the backend `.env` file (`cd backend && cp .env.example .env && cd ..`) and complete it
10. Create the frontend `.env` file (`cd frontend && cp .env.example .env && cd ..`) and complete it
11. Start the backend: `cd backend && source substrate-backend/bin/activate && uvicorn src.main:app --reload && cd ..`
12. Start the frontend: `cd frontend && npm run dev && cd ..`.
13. Navigate to [http://localhost:3000](http://localhost:3000)

## Interested?

If you are interested, please leave us a star and/or sign up for the hosted version on [substrateai.com](https://substrateai.com)
