# ☁️ASAH: Cloud Computing
## 📑About Our Project
  ASAH (Aplikasi Sortir Sampah) is an application aimed at encouraging the community to manage waste in an appropriate manner and provides rewards when users successfully manage their waste correctly. In our application, users are required to sort their waste first, and then they can dispose of or donate their waste to recycling agencies in their vicinity.
## 🖥️Related Project Repositories

Here are some of the related repositories which are part of the same project:

| Repository | Link |
| --- | --- |
| 📱 Mobile Development | [MD Repository](https://github.com/ASAH-Bangkit-2023/MD.git) |
| 🤖 Machine Learning | [ML Repository](https://github.com/ASAH-Bangkit-2023/ML) |

## 👷‍♂️CGP Architecture 
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/1591ad9a-a41a-484c-9844-5edc4a81f489" width="500px">
</p>

## 💼API Documentation
To access the API documentation, you can visit the following link [API Documentation](https://cloud-computing-asah-hhoivlttoa-uc.a.run.app/docs)

# 📋Deployment Steps

## 1. Cloud SQL 💾
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/6010b58c-e52f-4133-81fb-aca8c21fae08" width="500px">
</p>

- After filling in the instance ID and password, scroll down to create the instance

<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/4ab97880-be57-4c62-b293-04513834fb51" width="500px">
</p>

- Change the network to public in order to make it accessible to clients

<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/669ed3c4-939d-4504-9adc-e31f3f7ccdf1" width="500px">
</p>

- Once done, save the changes

## 2. Cloud Storage 🛒
- Click on "Create Bucket."
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/6cdf462d-6053-4243-9dfe-9759d6a45d7a" width="500px">
</p>

- After clicking "Create," fill in the "Bucket Name" field according to your needs
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/1fcdba61-5040-4d11-ab48-55ba0502e9b0" width="500px">
</p>

- In the "Choose how to control access to objects" section, uncheck the "Enforce public access prevention on this bucket" option
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/63a5e42f-3594-4aca-b818-8e4eef748e5e" width="500px">
</p>

- After that, click on "Continue" and then click on "Create"
- Once the bucket is created, click on "Permissions" as it is still set to "Not Public"
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/cbae7f2a-9619-4b6a-898b-71715845d1b9" width="500px">
</p>

- Next, scroll down to "+ Add access control entry" or "+ Grant access" button
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/51acfee8-6610-4b09-99d2-471de912f4cc" width="500px">
</p>
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/162a15fc-3d99-4d9c-8ab4-7f593450d5f8" width="500px">
</p>

- Add the following entries in the "New principals" section: "allUsers" and "allAuthenticatedUsers." Set the role as "Storage Viewer"

- Click on "Save" and you're done

## 3. Create Maps API Key 🔑
- Search “Google Maps ” pada bagian search di GCP
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/f8b83bf7-0f55-4fc6-a2f4-6fe229243fca" width="500px">
</p>

- Click on the "APIs" section and scroll down until you find the "Additional APIs" section 
- Choose the desired API from the available options
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/51e194fd-6ab3-4662-91b5-b90691b4f612" width="500px">
</p>

-  Once you have made your selection, click on it, and then click on "Enable"
-  Then, navigate to the "Credentials" section and choose the Google Maps Platform API for which you want to create a key
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/179df1de-eca4-470b-a090-6ec2113dd43b" width="500px">
</p>

-  Once done, click on the "+CREATE CREDENTIALS" button
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/f6ba0599-6f52-4316-a4bc-14250fc88110" width="500px">
</p>

-  After clicking "+CREATE CREDENTIALS"
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/2f6e1d3d-72a7-4f8d-82e5-e9d14a11d280" width="500px">
</p>

-  Select "API key" and start creating the API key
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/94b7c6f1-e631-4f52-92ff-9b0926fe6a46" width="300px">
</p>

-  After that, the API key will appear
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/71427553-5f45-47f5-b19c-4ab4ffd2a672" width="500px">
</p>

- The API key has been handed over to the MD team for their use
## 4. Prepare FastAPI (Using this exist repository) 🔥
- Clone the repository from the existing repo:
```bash
 git clone https://github.com/your-repo.git
```
## 5. Prepare Dockerfile 📄
- Setting up a Dockerfile for deployment

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENV PORT 1234
ENV MYSQL_URL "mysql+pymysql://root:PASSWORD@SERVER-IP:PORT/NAME DATABASE"
ENV JWT_SECRET_KEY "SECRET KEY"  
ENV JWT_REFRESH_SECRET_KEY "REFRESH SECRET KEY" 

RUN pip install --no-cache-dir -r requirements.txt

CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
```

## 6. Cloud Run 🏃‍♂️☁️
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/e5e4812a-2159-4ee9-8e36-6cbd2ba0e6f8" width="500px">
</p>

- Click on "Create Service"
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/87fe8769-e3b5-4b89-9cff-dfb9d79494ba" width="500px">
</p>

- Select "Continuously deploy new revisions from a source repository" to create CI/CD (Continuous Integration/Continuous Deployment)
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/aa23cea5-3923-4f88-b090-a70583d8c6a1" width="500px">
</p>

- Connect to GitHub and select the desired repository
- Next, choose "Build Configuration" with Dockerfile
- Then, leave everything else as default, and in the authentication section, select "Allow unauthenticated invocations" to make it accessible to the public
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/78dad855-09d1-4a82-b0cd-93b7ea2047d4" width="500px">
</p>

- Once you have selected "Allow unauthenticated invocations," click on "Create"
- After that, the website will be successfully deployed.
<p align="center">
  <img src="https://github.com/fikriiardiansyahh/fikri/assets/72667607/1c5c729a-7078-42c6-9c4a-700c2c46f9a7" width="500px">
</p>

## 7. Testing the Application 📱📟
- To test the deployed application, you can use tools like `curl` or API testing tools like Postman. Here is an example of how to test the API using `curl`:

```bash
curl -X GET https://your-app-url.com/api/endpoint
```

- Replace `your-app-url.com` with the actual URL of your deployed application and `/api/endpoint` with the desired endpoint to test.

- You can also use Postman to send requests to the API and verify the responses.
