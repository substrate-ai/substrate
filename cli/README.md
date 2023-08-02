docker build . -t substrate-test --platform linux/amd64

docker build . -t substrate-test --no-cache  --platform linux/x86_64        

docker run substrate-test --platform linux/x86_64