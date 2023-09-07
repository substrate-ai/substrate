# LAGO microservice 

## Requirements
- Docker (CLI) installed 

## Current Setup 
- Redis - local docker instance
- AWS S3 - enabled, invoice pdfs are stored there
- PostgresSQL Database - remote database on AWS RDS 
- AWS Region - us-east-1

## Setting up SSL certificates with LetsEncrypt
With reference to [getLago Docs - LetsEncrypt Certs](https://docs.getlago.com/guide/self-hosted/docker#lets-encrypt-certificate)  
1. Ensure `./lago/extra/init-letsencrypt.sh` and `./lago/extra/nginx-letsencrypt.conf` has been populated with the correct domain name 
2. Run the script  within the lago directory with the following commands in the terminal
    ``` sh
    cd ./lago
    ./extra/init-letsencrypt.sh

    # You will be asked to provide some information
    # After that you should be able to see the extra/certbot folder
    ```
3. Run `docker-compose down` once the process has completed.


## Launching the Lago microservice on a remote server
1. Ensure .env is populated with the correct values of each keys, you may refer to the `.env.example` file for the necessary key
2. Ensure SSL certificates have been initialized (with LetsEncrypt or any other means)
3. Run the following in the terminal within the lago directory
    ``` sh
    cd ./lago 
    source ./.env
    docker-compose up --build # add -d flag to detach from terminal 
    ```
4. The lago container should be online and is hosted via the remote server once the docker-compose process has been initiated 
    - Tip: 
        - Look into `/lago/extra/init-letsencrypt.sh` if there are DNS routing bugs