FROM nginx:alpine

ARG BUILD_DATE=""
ARG BUILD_VERSION="dev"

LABEL maintainer="OpenTTD Dev Team <info@openttd.org>"
LABEL org.opencontainers.image.created=${BUILD_DATE}
LABEL org.opencontainers.image.authors="OpenTTD Dev Team <info@openttd.org>"
LABEL org.opencontainers.image.url="https://github.com/OpenTTD/gollum"
LABEL org.opencontainers.image.source="https://github.com/OpenTTD/gollum"
LABEL org.opencontainers.image.version=${BUILD_VERSION}
LABEL org.opencontainers.image.licenses="GPLv2"
LABEL org.opencontainers.image.title="Gollum nginx sidecar"
LABEL org.opencontainers.image.description="Nginx sidecar for Gollum"

# Configure nginx
RUN sed -i 's/access_log/# access_log/g' /etc/nginx/nginx.conf
COPY nginx.default.conf /etc/nginx/conf.d/default.conf
