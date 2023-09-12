FROM --platform=amd64 moby/buildkit

# add config file buildkitd.toml
COPY buildkitd.toml /etc/buildkit/buildkitd.toml

# install curl 
# RUN apk add --no-cache curl

# RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-444.0.0-linux-x86_64.tar.gz
# RUN ./google-cloud-sdk/install.sh
# RUN ../google-cloud-sdk/install.sh --quiet
# RUN rm -rf google-cloud-sdk

# # auth gcloud
# RUN gcloud auth activate-service-account --key-file=/etc/buildkit/gcloud.json

# # setup docker with gcp
# RUN gcloud auth configure-docker

# look at https://github.com/moby/buildkit/issues/1369


ENTRYPOINT [ "/usr/bin/buildkitd", "--config", "/etc/buildkit/buildkitd.toml" ]
