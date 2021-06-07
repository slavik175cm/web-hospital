# wep app for hospital
### deployed on digital ocean, accessible on http://206.189.58.70:8000
### to run locally: 

#### first way using image from dockerhub(https://hub.docker.com/r/slavik175cm/web):

1. copy docker-compose-prod.yml
2. run
```
docker-compose -f docker-compose-prod.yml up --build
```
accessible on 127.0.0.1:8000

#### second way:

in HospitalDjango/config.py set credentials for email account from which verification letters will be send
```
$ git clone https://github.com/slavik175cm/web-hospital.git
$ docker-compose up --build
```

### Short description:

App is build for convenient hospital management.
User can review different information about hospital, doctors and relevant
COVID statistics in Belarus. Authorized user can order talons, see his previous and future 
doctors visits and change profile.
Doctors using their accounts can manage visits, like setting cost,
prescribing treatment, etc


