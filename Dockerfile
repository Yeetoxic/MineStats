# Install the base requirements for the app.
# This stage is to support development.
FROM --platform=$BUILDPLATFORM python:alpine AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM --platform=$BUILDPLATFORM node:18-alpine AS app-base
WORKDIR /app
COPY * .

# Do the actual build of the mkdocs site
FROM --platform=$BUILDPLATFORM base AS build
COPY . .
#RUN set -e
#RUN docker buildx build --platform linux/amd64,linux/arm64 -t Yeetoxic/StatCrafter:latest $(1==0)

