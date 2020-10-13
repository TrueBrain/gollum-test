FROM ruby:2.7

ARG BUILD_DATE=""
ARG BUILD_VERSION="dev"

LABEL maintainer="OpenTTD Dev Team <info@openttd.org>"
LABEL org.opencontainers.image.created=${BUILD_DATE}
LABEL org.opencontainers.image.authors="OpenTTD Dev Team <info@openttd.org>"
LABEL org.opencontainers.image.url="https://github.com/OpenTTD/gollum"
LABEL org.opencontainers.image.source="https://github.com/OpenTTD/gollum"
LABEL org.opencontainers.image.version=${BUILD_VERSION}
LABEL org.opencontainers.image.licenses="GPLv2"
LABEL org.opencontainers.image.title="Gollum (Wiki)"
LABEL org.opencontainers.image.description="Gollum (Wiki) for OpenTTD."

# Gems need dependencies. We install and remove them in a single step, in an
# attempt to keep the image size as small as possible.
RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
        cmake \
        libicu-dev \
    && gem install \
        github-linguist \
        gollum \
        wikicloth \
    && apt-get remove -y \
        cmake \
        libicu-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Patch gollum and wikicloth, as they lack some features we like using.
COPY wikicloth.diff \
        gollum-lib.diff \
        /gollum/
RUN cd /usr/local/bundle/gems/wikicloth-* \
    && patch -p 1 -i /gollum/wikicloth.diff \
    && rm -f /gollum/wikicloth.diff \
    && cd /usr/local/bundle/gems/gollum-lib-* \
    && patch -p 1 -i /gollum/gollum-lib.diff \
    && rm -f /gollum/gollum-lib.diff

COPY config.rb /gollum/

ENV RACK_ENV=production

WORKDIR /wiki
EXPOSE 80

ENTRYPOINT ["gollum", "--port", "80", "--config", "/gollum/config.rb"]
CMD []
