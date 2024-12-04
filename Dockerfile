FROM python:3.11-slim

# Install git and curl to clone the repository
RUN apt-get update && apt-get install -y git

# Set the working directory to the cloned repository
VOLUME ["/app"]
WORKDIR /app
RUN git clone https://github.com/Yeetoxic/StatCrafter.github

# Move the contents of /app/StatCrafter to /app
RUN mv ./StatCrafter/* . && rm -rf ./StatCrafter

# Install any dependencies from requirements.txt (if present)
#RUN pip install -r requirements.txt

# Set the command to run your Python application
#CMD ["python", "app.py"]
