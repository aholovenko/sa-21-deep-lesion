# sa-21-deep-lesion
UCU Software Architecture for Data Science in Python Course 2021

### FastAPI Server for Deep Lesion Detection

#### Team: Illia Ovcharenko, Marian Petruk, Anastasia Holovenko

Run server locally
```
 pyenv install 3.9.2 
 pyenv virtualenv 3.9.2 deep-lesion
 source <path-to-env>/deep-lesion/bin/activate
 pip install -r requirements.txt
 uvicorn setup:app --host 0.0.0.0 --port 80
```

Run in docker container
```
 docker build . -t deep-lesion:latest
 docker run -p 80:80 deep-lesion
```
