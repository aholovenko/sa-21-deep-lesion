
# FastAPI Server for Deep Lesion Detection/Segmentation

### Team: Illia Ovcharenko, Marian Petruk, Anastasia Holovenko

### sa-21-deep-lesion
UCU Software Architecture for Data Science in Python Course 2021

## Description
Our project aims to set up a server to perform lesion detection/segmentation on CT scans.
The lesion detection task is highly time-consuming and costly.
Radiologists have to spend a lot of time manually adding bookmarks.
What is more, they usually add it only for one lesion's key slide per CT scan.
We, however, would like to optimize this process and provide anyone with an opportunity to upload their CT scan
and use our model to detect/segment a lesion on one's scan.

Here we develop a prototype that works with [DeepLesion Dataset](https://nihcc.app.box.com/v/DeepLesion/folder/50715173939),
and in the future project can be adapted to other datasets.

## Installation

**Step 1**: Simply set up of a server

Option 1: Run server locally
```bash
 pyenv install 3.9.2
 pyenv virtualenv 3.9.2 deep-lesion
 source <path-to-env>/deep-lesion/bin/activate
 python -m pip install --upgrade pip
 pip install wheel
 pip install -r requirements.txt
 uvicorn setup:app --host 0.0.0.0 --port 8080
```

Option 2: Run in docker container
```bash
 docker build . -t deep-lesion:latest
 docker run -p 8080:8080 deep-lesion
```

Option 3: Deploy the app
* Draft a new release using [workflow](https://github.com/aholovenko/sa-21-deep-lesion/releases/new)
* Wait for a successful build and Google Cloud Registry upload
* Find your image in GCR with the tag used during the build
* Configure to run on the cloud

Current [url](https://deep-lesion-service-642qcpnmbq-uc.a.run.app)

**Step 2**: Upload your CT scan image (from DeepLesion dataset) as a `*.png`, `*.jpeg` or `*.jpg` file

**Step 3**: Get detection/segmentation results

![output](images/segmentation-example.png)

##### Warning: Please, don't jump to any conclusions and consult with your therapist! 
