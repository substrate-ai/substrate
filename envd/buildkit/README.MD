# This is main readme you have to worry about

# setup
conda create -n envd
conda activate envd
pip install envd

envd context create --name local-buildkit-container \                                                                                  ✔  envd Py
  --builder tcp \
  --builder-address 127.0.0.1:8888 \
  --use 

envd context use --name local-buildkit-container




# get credential access account 
look at access accout and create a key (GCP IAM), you can call it gcp.json and put it in the buidkit folder
(you can also store it in base64, cf. How to push manually on docker)

# to Run

You need to terminal 
terminal 1: go to buildkit folder and do `docker compose up`

terminal 2: go to envd-quick-start and do `envd build --output type=image,name=us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai/substrate-ai,push=true`

`name=us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai`
This is just a repo in artificat registry (gcp)
You can modify it or create other repo if needed

# tips 
you can modify `build.envd` and remove all python package to speed up creation of docker container so you can debug authentification with gcp faster

# What I need help with 
THIS IS THE MAIN ISSUE
- making buildkit container able to push to a gcp registry (authentification problem)
    -> directions: look at service account in IAM gcp, look at artificat registry
  

(I told you in the meeting this was not working, i just manage to get it working in the end)



# How to push manually on docker
Could be useful for you to look at how to login with buildkit
`docker login -u USERNAME -p PASSWORD`
How to do that to login into gcp
`docker login -u _json_key -p "$(cat /Users/baptiste/Git/substrate/cli/gcp.json)" us-east1-docker.pkg.dev`
`base64 -i gcp.json -o gcp_base64.json`
`cat gcp_base64.json | docker login -u _json_key_base64 --password-stdin \ https://us-east1-docker.pkg.dev`
`docker push us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai/substrate-ai`

