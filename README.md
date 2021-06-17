# sa-21-deep-lesion
UCU Software Architecture for Data Science in Python Course 2021

### FastAPI Server for Deep Lesion Detection/Segmentation

#### Team: Illia Ovcharenko, Marian Petruk, Anastasia Holovenko

The purpose of our project is to set up a server to perform lesion detection/segmentation on CT scans.
Lesion detection task is highly time-consuming and costly. Radilogists have to spend a lot of time
manually adding bookmarks. What is more, they usually add it only for one lesion's key slide per CT scan.
We, however, would like to optimize this process and provide anyone with an opportunity to upload their CT scan
and use our model to detect/segment a lesion on one's scan.

**Step 1**: Simply set up of a server

Option 1: Run server locally
```
 pyenv install 3.7.2 
 pyenv virtualenv 3.7.2 deep-lesion
 source <path-to-env>/deep-lesion/bin/activate
 pip install -r requirements.txt
 uvicorn setup:app --host 0.0.0.0 --port 8080
```

Option 2: Run in docker container
```
 docker build . -t deep-lesion:latest
 docker run -p 8080:8080 deep-lesion
```

Option 3: Deploy app
* Draft a new release using [workflow](https://github.com/aholovenko/sa-21-deep-lesion/releases/new)
* Wait for successful build and Google Cloud Registry upload
* Find your image in GCR with the tag used during the build
* Configure to run on the cloud
Current [url](https://deep-lesion-service-642qcpnmbq-ue.a.run.app)

**Step 2**: Upload your CT scan image as a `*.png`, `*.jpeg` or `*.jpg` file

![output](images/segmentation-example.png)

**Step 3**: Get detection/segmentation results

##### Warning: Please, don't jump to any conclusions and consult with your therapist! 
