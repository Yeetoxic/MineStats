FROM python:3.11-slim


WORKDIR /app

# optional build arg to let the hardening process remove all package manager (apk, npm, yarn) too to not allow
# installation of packages anymore, default: do not remove "apk" to allow others to use this as a base image
# for own images
ARG REMOVE_APK=0

ENV HOME=/app
ENV NODE_ENV=production

# only single copy command for most parts as other files are ignored via .dockerignore
# to create less layers
COPY . .

#HEALTHCHECK --interval=1m --timeout=2s 

#ENTRYPOINT ["/app"]

EXPOSE 5000











# Install git and curl to clone the repository
#RUN apt-get update && apt-get install -y git

# Set the working directory to the cloned repository
#VOLUME ["/app"]
#WORKDIR /app
#RUN git clone https://github.com/Yeetoxic/StatCrafter.git

# Move the contents of /app/StatCrafter to /app
#RUN mv ./StatCrafter/* . && rm -rf ./StatCrafter

# Install any dependencies from requirements.txt (if present)
#RUN pip install -r requirements.txt

# Set the command to run your Python application
#CMD ["python", "app.py"]
