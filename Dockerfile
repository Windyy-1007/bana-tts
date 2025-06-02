FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y libsndfile1

# Copy environment.yml
COPY environment.yml .

# Create the conda environment
RUN conda env create -f environment.yml

# Activate the environment and set it as default
SHELL ["conda", "run", "-n", "nmt", "/bin/bash", "-c"]

# Copy your code
COPY . .

# Set the default command (replace app.py with your entry point)
CMD ["conda", "run", "-n", "nmt", "python", "app.py"]