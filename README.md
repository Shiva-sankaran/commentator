# COMMENTATOR

- A Code-mixed Multilingual Text Annotation Framework.
- Code-mixing on Hinglish Data.
- Easy extensibility to other code-mixed language pairs such as Gujarati-English, Marathi-English etc.

### 1. Relevant Links

Source Code: [`https://github.com/Shubh-Nisar/commentator`](https://github.com/Shubh-Nisar/commentator)
Youtube Demo: [`https://youtu.be/pFqcwyjAfB4`](https://youtu.be/pFqcwyjAfB4)
Live Demo Site: [`http://commentator-iitgn.s3-website.ap-south-1.amazonaws.com/`](http://commentator-iitgn.s3-website.ap-south-1.amazonaws.com/)

---

### 2. Folder Structure

```
backend
	app.py
	requirements.txt
	Dockerfile
fronend
	build
	node_module
	public
	src
		Admin
		Auth
		Components
		Edit
		Home
		User
		utils
		Router.js
	.env
	.ignore
	package-lock.json
	package.json
```

##### frontend/src/.env

    REACT_APP_BACKEND_URL=http://<YOUR_BACKEND_IP_ADDRESS>:5000
    OR
    REACT_APP_BACKEND_URL=http://localhost:5000

---

### 3. Database Schemas

|           |                                             |
| --------- | ------------------------------------------- |
| lid       | LID based Language Identification of Tokens |
| sentences | Sentences to be annotated                   |
| users     | Admin & Annotator Accounts                  |

### 4. Backend [ Local Server ]

##### Steps to Follow

a. Navigate inside backend folder

    cd backend

b. Installing Dependencies

    pip install -r requirements.txt

c. Updating Frontend URL

> Open `app.py` in a code/text editor (Visual Studio Code, Sublime Text, Notepad etc)

    frontend = YOUR_FRONTEND_HOST_URL
    OR
    frontend = http://localhost:3000

d. Updating MongoDB URL

> Open `app.py` in a code/text editor (Visual Studio Code, Sublime Text, Notepad etc)

    conn_str = YOUR_MONGODB_URL

e. Running the local server

    python app.py
    OR
    py app.py

---

### 5. Frontend [ Local Server ]

##### Steps to Follow

a. Navigate inside backend folder

    cd frontend

b. Install all frontend dependencies post 1st application download.
npm i

c. Start the frontend local server.

    npm start

> OR click on the frontend bash/shell file to run the frontend local server.

---

### 6. Administrative Configuration

##### Steps to Follow

1. Start Frontend and Backend Local Server. (Refer 2.e & 3.c)
2. Create an admin account.
3. Open MongoDB database and set `admin=True` to create superuser/admin account.
4. Login to Admin Dashboard.
5. Upload sentences to the database (csv).

### 7. Containerization of Backend using Docker

##### Steps to Follow

a. Creating a Docker Hub Account and a public repository

> Visit https://hub.docker.com/

b. Updating Dockerfile

    FROM python:3.9-slim-buster
    WORKDIR /commentator
    COPY requirements.txt requirements.txt
    RUN pip3 install -r requirements.txt
    COPY . .
    ENV FLASK_APP=app.py
    CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
    EXPOSE 5000/tcp

b. Push Image to Docker Hub

    docker build . -t python-docker
    docker tag python-docker <DOCKER_USERNAME>/<REPOSITORY_NAME>
    docker push <DOCKER_USERNAME>/<REPOSITORY_NAME>

c. Run Docker server on port 5000

    docker run -dp 5000:5000 <DOCKER_USERNAME>/<REPOSITORY_NAME>

d. List of active docker containers

    docker ps

e. Stop Docker Container by Container ID.

    docker stop <CONTAINER_ID>

---

### 8. Hosting

a. Backend

> AWS EC2 Instance is used to host the docker container
> Quick Guide: https://youtu.be/awFLzy0XwXo

In the SSH Terminal

    docker pull <DOCKER_USERNAME>/<REPOSITORY_NAME>
    docker run -dp 5000:5000 <DOCKER_USERNAME>/<REPOSITORY_NAME>

The updated backend URL `http://<public_IPv4_address>:5000`

b. Frontend

> AWS S3 Bucket is used to host the frontend website
> Quick Guide: https://blog.cloudthat.com/step-by-step-guide-to-deploy-reactjs-app-on-aws-s3/

##### Steps to create build

    cd frontend
    npm run build

The updated frontend URL is available at Properties > Static Web Hosting

### 9. Contributors

|                                                                                                                                           |                  |                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------ |
| <img  width="75"  alt="tn"  src="https://user-images.githubusercontent.com/65038837/126761822-ca949453-540f-40f1-a8cd-9a1ed3e4cae2.jpeg"> | Shubh Nisar      | [`https://shubh-nisar.github.io`](https://shubh-nisar.github.io)               |
| <img  width="75"  alt="vs"  src="">                                                                                                       | Vivek Srivastava | [`https://sites.google.com/view/vivek-srivastava/`](https://www.linkedin.com/) |
| <img  width="75"  alt="ms"  src="">                                                                                                       | Mayank Singh     | [`https://mayank4490.github.io/`](https://mayank4490.github.io/)               |
