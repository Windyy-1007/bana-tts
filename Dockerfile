FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy environment.yml
COPY environment.yml .

# Create the conda environment
RUN conda env create -f environment.yml

# Activate the environment and set it as default
SHELL ["conda", "run", "-n", "nmt", "/bin/bash", "-c"]

# Copy your code
COPY . .

# Expose the port that Flask runs on
EXPOSE 5000

# Add health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Set the default command
CMD ["conda", "run", "-n", "nmt", "python", "app.py"]