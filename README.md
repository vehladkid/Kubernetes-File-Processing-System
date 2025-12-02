KUBERNETES FILE PROCESSING PIPELINE (OS Class Project)
A complete container-based scheduling and file-processing system built using Kubernetes Jobs, PVC, Pods, Flask, and SQLite.



PROJECT OVERVIEW

This project implements a file-processing pipeline using:
Kubernetes Jobs
Persistent Volume Claims (PVC)
Container-based Scheduling (OS Concept)
Flask Web Interface
Kubernetes Dashboard
SQLite-backed file indexing

Users can upload, view, and delete files through a Flask UI.
Files are stored in a Kubernetes PVC and processed by Jobs running inside Pods.
A dashboard displays resource counts (images, documents, etc.), all synced with SQLite.



OBJECTIVES

Implement OS-style job scheduling using Kubernetes Jobs & Containers
Build a persistent file management system using PVC
Deploy a microservice architecture with Flask + K8s Jobs
Track file metadata automatically using SQLite DB inside containers
Provide a clean web UI for file upload/view/delete
Expose a dashboard for resource statistics



ARCHITECTURE
                    ┌─────────────────────────────────┐
                    │            Flask UI              │
                    │  - File Upload / View / Delete   │
                    │  - Triggers Job Creation         │
                    └─────────────────────────────────┘
                                   │
                                   ▼
                     ┌─────────────────────────────┐
                     │  Kubernetes Deployment       │
                     │  (flask-site)                │
                     └─────────────────────────────┘
                                   │
                                   ▼
                     ┌─────────────────────────────┐
                     │     Persistent Volume        │
                     │     (PVC: file storage)      │
                     └─────────────────────────────┘
                                   │
                                   ▼
                     ┌─────────────────────────────┐
                     │ Kubernetes Job (processor)   │
                     │ - Classifies files (img/docs)│
                     │ - Updates SQLite DB          │
                     └─────────────────────────────┘
                                   │
                                   ▼
                     ┌─────────────────────────────┐
                     │    Dashboard Deployment      │
                     │ - Shows counts/statistics    │
                     └─────────────────────────────┘




REPOSITORY STRUCTURE
k8s-os-project/
│
├── k8s-file-container/
│   ├── app/                   # Backend processing logic
│   ├── k8s/                   # YAML specs
│   └── process-files-job.yaml
│
├── k8s-dashboard/             # Dashboard UI + APIs
│   ├── app.py
│   ├── deployment.yaml
│   ├── dashboard-deploy.yaml
│   ├── Dockerfile
│   └── pvc.yaml
│
├── flask-site/                # Web UI (upload/view/delete)
│   ├── app.py
│   ├── templates/
│   ├── static/
│   └── flask-site-deployment.yaml
│
├── file-pvc.yaml              # Shared Persistent Volume
├── process-files-job.yaml     # Top-level job spec
├── setup_k8s_project.sh       # Script to auto-deploy system
└── README.md





🖥️ FLASK  WEB  UI (Screenshots)

Your UI supports:
Uploading files
Viewing images/documents
Deleting files (removes from PVC and SQLite)
Navigation to dashboard




HOW IT WORKS

1️⃣ Upload a file through the Flask UI
➡ Gets stored inside the PVC
➡ Entry added to SQLite DB

2️⃣ Kubernetes Job is triggered
Job container runs your OS scheduling logic
Classifies files → images/docs/text
Updates DB → status, type, etc.

3️⃣ Dashboard displays:
Total images
Total documents
Total files in PVC
Live synced from SQLite

4️⃣ Delete a file
Removed from PVC
Removed from SQLite
UI refreshes automatically




HOW TO RUN THE PROJECT

Run all commands inside your VM.

⭐ Start Kubernetes cluster
minikube start

⭐ Deploy namespace
kubectl create namespace file-demo

⭐ Deploy PVC + Jobs + Backend processing
kubectl apply -f file-pvc.yaml -n file-demo
kubectl apply -f process-files-job.yaml -n file-demo

⭐ Deploy Flask UI
cd flask-site
kubectl apply -f flask-site-deployment.yaml -n file-demo
kubectl expose deployment flask-site --type=NodePort --port=5000 -n file-demo
flask run

⭐ Open the UI

Get the NodePort:
minikube service flask-site -n file-demo --url

Open the link in a browser.
Dashboard

Visit the dashboard via:

http://<node-ip>:<dashboard-port>

Displays:
Total images
Total documents
Total text files
Total processed files
All in real-time from SQLite




🛠️ TECHNOLOGIES USED
Component       	Tech
Web UI	                Flask, HTML, CSS
Processing Backend	Python
Container Runtime	Kubernetes, Minikube
Storage          	PVC, PV
Scheduling Logic	Kubernetes Jobs
Database        	SQLite
Frontend Deployment	K8s Deployment + Service
Dashboard	        Flask API + K8s Deployment




🌟 FEATURES
✔ File Upload / View / Delete
✔ Automatic file classification
✔ Persistent storage using PVC
✔ SQLite-based indexing
✔ Dashboard showing resource statistics
✔ Container-based OS scheduling
✔ Complete microservice architecture




FUTURE IMPROVEMENTS
Add worker autoscaling using HPA
Convert Flask UI into a React frontend
Add Redis for queue management
Add user authentication
Store file type/model metadata
Add logs viewer in dashboard


