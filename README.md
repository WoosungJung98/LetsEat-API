## FaceYelp

### Documents
- [FaceYelp API Design](https://docs.google.com/document/d/1cvx0RLAozOFaXrAdNLd8wsKsOPzj-ZBIeLHQnpzMB6Y/edit?usp=sharing)

### Dev Environment Setup
1. Make sure you are on an X86-64 machine (No ARM based machines like Apple M1 or M2)
2. Install pyenv, pyenv-virtualenv
```
https://github.com/pyenv/pyenv
https://github.com/pyenv/pyenv-virtualenv
```
3. Clone FaceYelp-API repository.
4. Install python (>= 3.10.7, < 3.11) using pyenv, create an pyenv-virtualenv environment, and activate the environment
5. Install packages within the activated environment
```
pip install -r requirements.txt
```
6. In main folder, make a copy of default.cfg and rename to faceyelp.cfg. (Ask William for details)
```
cp main/default.cfg main/faceyelp.cfg
```
7. Run Flask Server. (In production environment, execute ./bin/run_server.sh [port])
```
python run.py [port]
```
8. Checkout the API documentation.
```
http://[ip]:[port]/docs
```

#### Uploaders Execution

- Creates tables and uploads Yelp JSON Data in PostgreSQL database
```
python main/uploaders/run_faceyelp.py faceyelp
```
