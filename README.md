# Annotation Flask

### 1. Backend [ Docker ]

a. Run Docker server on port 5000

    docker run -dp 5000:5000 iitgnshubh/backend

---

b. List of active docker containers

    docker ps

---

c. Stop Docker Container by Container ID.

    docker stop <CONTAINER_ID>

---

### 2. Frontend

> Inside the frontend folder

a. Install all frontend dependencies post 1st application download.
npm i

---

b. Start the frontend local server.

    npm start

> OR click on the frontend bash/shell file to run the frontend local server.

---

### 3. Database

a. Define Schemas in the mongoDB database.

    python3 schemas.py

---

b. Insert sentences in the defined database schema.

    python3 db.py

---

c. Create a csv file for the sentences present in the database.

> NOTE: "username" has to be updated to get the csv specific to your user account.

    python3 db_to_csv.py

d. Modify database storage location

> Update the <conn_str> present in backend/app.py to your mongoDB local or mongoDB atlas string.

---

### 4. Source Code

> https://github.com/Shubh-Nisar/annotation-flask

### 5. Contributors

|                                                                                                                                           |                  |                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ---------------------------------------------------------------- |
| <img  width="75"  alt="tn"  src="https://user-images.githubusercontent.com/65038837/126761822-ca949453-540f-40f1-a8cd-9a1ed3e4cae2.jpeg"> | Shubh Nisar      | [`https://shubh-nisar.github.io`](https://shubh-nisar.github.io) |
| <img  width="75"  alt="vs"  src="">                                                                                                       | Vivek Srivastava | [`Some Link`](https://www.linkedin.com/)                         |
| <img  width="75"  alt="ms"  src="">                                                                                                       | Mayank Singh     | [`Some Link`](https://www.linkedin.com/)                         |
