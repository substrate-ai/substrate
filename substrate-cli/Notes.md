docker build . -t substrate-test --platform linux/amd64

docker build . -t substrate-test --no-cache  --platform linux/x86_64        

docker run substrate-test --platform linux/x86_64

todo maybe check in dockerfile that GPu is availabel but this need to be done at runtime

todo terraform

# todo experiment with https://github.com/tensorchord/envd