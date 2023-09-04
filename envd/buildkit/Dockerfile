FROM --platform=amd64 moby/buildkit

# add config file buildkitd.toml
COPY buildkitd.toml /etc/buildkit/buildkitd.toml

# how to loin into gcp 

ENTRYPOINT [ "/usr/bin/buildkitd", "--config", "/etc/buildkit/buildkitd.toml" ]
