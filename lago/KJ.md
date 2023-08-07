# Deploying lago on AWS

LOOK AT 
https://docs.getlago.com/guide/self-hosted/docker

SLACK
https://lago-community.slack.com/ssb/redirect

ASK baptiste for .env


Goal: 
Deploying the lago inside AWS. This means that lago code run on in an ec2 instance and is connected to RDS (databse), S3 (file bucket) and Redis (this is not stricly necessary...)

## Step 1
Just deploy locally and test sign up and create a customer
- docker-compose up

## Step 2
create RDS, S3, REDIS on AWS and connect local instance to it
use .env file 
useful to test connection to DB with local GUI (cf. tableplus mac app)

## Step 3 (OPTIONAL)
AWS install docker, docker compose with AWS Linux 2023
(or reuse my instance should be good enough)

## Step 4
Test setup on server and deploy to domain lago.substrateai.com

## Step 5
enable ssl, so https works 
(look at lago documentation)


### Tips:
- T2.medium ec2 instance works great, choose instance with at least 4gb
- on ec2 instance rename docker-compose.prod.yml to docker-compose.yml
and use docker-compose up otherwise you will have problems

(Could look at terraform for deployment?)


### list of cmds
docker system prune --all 
docker volume prune
docker-compose -f docker-compose.local.yml down   
docker-compose -f docker-compose.local.yml up
docker-compose
docker ps
docker logs CONTAINER
docker-compose logs

