# Flask application deployment with flask and kubernetes
This project demonstrates the creation and deployment of a web application using advanced Dockerization techniques, automated CI/CD pipelines with GitHub Actions, and Kubernetes for orchestration. The focus is on best practices in security, data persistence, and high availability.

## Version Control with GitHub
### Repository Initialization and Configuration
- **Branch Protection Rules:**
  - Implemented branch protection rules on the main branch.
  - These rules require pull request reviews and status checks before merging, ensuring code quality and preventing direct pushes to the main branch.
### Continuous Integration and Continuous Deployment (CI/CD)
The CI/CD pipeline for the application is defined in the **.github/workflows** directory. The workflow, named "Flask CI/CD Pipeline", is triggered on pull requests to the **main** branch. It consists of two primary jobs: **SemanticRelease** and **build**.

The SemanticRelease job automates versioning and changelog generation, while the build job handles Python environment setup, code linting, running tests, and building & pushing the Docker image to Docker Hub.

### Environment Variables and Tokens
**GitHub Secrets**
The pipeline utilizes GitHub Secrets to securely store and use sensitive information like tokens and usernames. These are used for authentication and authorization purposes within different steps of the workflow.

**GH_TOKEN:** A GitHub token used for creating releases and tagging in the GitHub repository. It's crucial for the SemanticRelease job.<br>
**DOCKERHUB_USERNAME:** The Docker Hub username, used for pushing the Docker image.<br>
**DOCKERHUB_TOKEN:** A token for Docker Hub, which is used to authenticate the Docker Hub account for pushing the built image<br>

## Application Setup
The core of the web application is the **app.py** file, which is a Python script using Flask, a lightweight WSGI web application framework and has following features<br>

- A home route (/) that returns a welcome message.
- An API endpoint (/api/data) supporting GET and POST methods for data interaction.
- Custom error handlers for 404 and 500 HTTP status codes.
- Configurable logging for debugging and monitoring.
- Dynamic port assignment for flexibility in various deployment environments.

### Dockerfile
The Dockerfile for this application is designed with a focus on security and efficiency. Here are its key characteristics:

**Base Image:** Utilizes python:3.9-slim, a lightweight version of the Python 3.9 image, to reduce the overall size and potential vulnerabilities of the container.<br>
**Dependencies Management:** Installs required Python packages from requirements.txt using pip without storing cache data, ensuring a smaller image size.<br>
**Application Files:** Incorporates the application source code, including the app.py file, into the container.<br>
**Non-root User:** Enhances security by creating and switching to a non-root user (aayushi) for running the application. This practice significantly reduces the risk of unauthorized system access.<br>
**Port Exposure:** Exposes port 5000, which is the designated port for the Flask application, allowing communication between the container and the outside world.<br>

### Accessing the Application
- On your local machine, pull the image from Docker Hub using the docker pull command.
  ```
   docker pull aayushipatel/flaskapp:v0.2.2
  ```
- After pulling the image, run it as a container. If your Flask app listens on port 5000, you can map it to a local port (e.g., 8000).
  ```
    docker run -p 8000:5000 aayushipatel/flaskapp:v0.2.2

  ```
- Open a web browser and navigate to ``` http://localhost:8000 ```. You should see your Flask application running.

###  To mount a specific filesystem directory from the host to the container's storage
- STEP-1:  Create a directory on the Host
  ```
    mkdir ~/host_data
  ```
- STEP-2: Modify the Docker Run Command
  ```
    docker run -p 8000:5000 -v ~/host_data:/data aayushipatel/flaskapp:v0.2.2
  ```
### Deploying with Kubernetes
- Configuring Persistent Storage: Apply the PersistentVolume and PersistentVolumeClaim manifests:
  ```
  kubectl apply -f pv.yaml
  kubectl apply -f pvc.yaml
  ```
- Create a Deployment: Apply the **deployment.yaml** file to create a Kubernetes Deployment.
  ```
  kubectl apply -f deployment.yaml
  ```
- Create a Service: Apply the **service.yaml** file to expose the application.
  ```
  kubectl apply -f service.yaml
  ```
- Setup Ingress: To use an ingress, apply the ingress.yaml file.
  ```
  kubectl apply -f ingress.yaml
  ```
- Accessing the Application: Find the external IP or domain to access your deployed application.
  ```
  kubectl get services
  ```
- Running the Application
  Since it's a local/development  environment, you can access the application through localhost.

### Filesystem Integration and Data Persistence
- Sending Data to the Application
  - Prepare Your Data: Create a JSON object with the data you want to send. 
  ```
  {
    "name": "aayushi"
  }
  ```
  - Send a POST Request: Use a tool like curl or Postman to send a POST request to the /save-data endpoint.
  ```
  curl -X POST http://localhost:8000/save-data -H "Content-Type: application/json" -d '{"name": "aayushi"}'
  ```
### Verifying Data Persistence
After sending the POST request, the data is written to a file in the persistent volume. Follow these steps to verify that the data has been stored persistently:
- Identify the Pod: First, identify the pod running your Flask application:
    ```
   kubectl get pods
    ```
- Access the Pod's Filesystem: Execute a command within the pod to view the contents of the file where data is stored. Assume the file is named datafile.txt and stored in a directory mapped to the persistent volume:
- Check if Data is Saved in Volume:
    ```
    kubectl exec [YOUR_POD_NAME] -- cat /data/datafile.txt
    ```
Verify the Data: The output should display the data you sent via the POST request, confirming that it has been written to the persistent volume.


