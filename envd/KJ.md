# Envd, buildkit and GCP

This is main readme for the new solution for docker container building and pushing
This is mainly used for test and will be integrated into other folders potneitally (like cli)

# folder structure
- gcp-client-python
    This shows the google-cloud client sdk, the issue is that i cannot manage to login in the sdk with the credentials 
    What need to be done: Nothing not a prioirty
- envd-quick-start
    this is an example of an envd project, you use the cli to start building the container with envd
- buildkit:
    this is the worker that will be hosted in the cloud, that build and then push docker image to artificat registry


