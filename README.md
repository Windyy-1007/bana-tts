## ## Description

Bahnar Text-to-Speech is a project that turns written words—or text captured from images—into clear, natural-sounding Bahnar speech. Type a sentence or drop in a picture, and the project instantly reads the content aloud, saves each reading for later, and helps promote everyday use of the Bahnar language.
## Prerequisites

### 1 Install required tools

- **Git** – to clone the source code.
    
- **Docker Desktop / Docker Engine** – to build and run the container.
    
- **Windows Subsystem for Linux 2 (WSL2)** – the backend Docker Desktop uses on Windows (enable it via `wsl --install`).
    
- **Python ≥ 3.8** _(optional)_ – only needed if you want to run CLI commands or develop outside Docker.

### 2 Clone the repository

```bash
git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>
```

### 3 Download pretrained model checkpoints

1. Download **Grad‑TTS** and **HiFi‑GAN** checkpoints (trained on LJSpeech & Libri‑TTS, 22 kHz) from **[here](https://drive.google.com/drive/folders/1grsfccJbmEuSBGQExQKr3cVxNV0xEOZ7)**.
    
2. In the **existing** `checkpts/` directory (already present in the repo and containing `hifigan-config.json`), **move `hifigan.pt` into this folder**.
    
3. Inside `checkpts/`, create a sub‑folder `grad/`, move **grad‑tts.pt** there, and **rename it to `grad_1344.pt`** so the final layout looks like:
    
    ```
    checkpts/
    ├── hifigan-config.json
    ├── hifigan.pt
    └── grad/
        └── grad_1344.pt
    ```
    
### 4 Prepare Dockerfile 

If the repo does not already contain them, create a **Dockerfile** in the project root:

```Dockerfile
# --- Dockerfile ---
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
```

### 5 Build the Docker image

```bash
docker build -t your-image-name .
```

- `your-image-name`: any tag to identify the image.
    
- The dot (`.`) tells Docker to use the current directory as the build context.
    

### 6 Run the container

```
docker run --rm -p hostPort:containerPort your-image-name
```

- `-p hostPort:containerPort`: maps an available **hostPort** on your machine to the **containerPort** your app listens on (e.g. `5000:5000`).
    
- `--rm`: automatically removes the container when you stop it. 
    

### 7 Open your browser

Open **http://localhost****:** in your browser — replace `<hostPort>` with the value you used in `docker run -p hostPort:containerPort`.

- _Example:_ if you ran `docker run -p 5000:5000 ...`, navigate to http://localhost:5000.

## Usage Explanation:

To use the Bahnar Text-To-Speech web application, open the localhost site. The interface includes two main functionalities: text-to-speech and image-to-speech. 

In the Text-to-speech tab, users can enter text manually into the textbox or upload a .txt file using the “Upload Text File” button. After inputting the text, clicking the “Speak” button will generate and play the synthesized speech, while also saving the request to the history panel on the right.

In the Image-to-speech tab, users can drag and drop an image or use the “Upload Image” button to select an image from their device. The system will extract any text from the image and display it in the textbox. The user can then click “Speak” to convert the extracted text to speech. 

Additionally, a language selector is available in the top right corner, allowing users to switch the interface language between English and Vietnamese.
