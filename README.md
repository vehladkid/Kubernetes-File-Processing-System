<p align="center">
  <img src="https://img.shields.io/badge/Kubernetes-326ce5?style=for-the-badge&logo=kubernetes&logoColor=white">
  <img src="https://img.shields.io/badge/Minikube-f5dd42?style=for-the-badge&logo=kubernetes&logoColor=black">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-07405e?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge">
</p>


# 🚀 Kubernetes File Processing Pipeline (OS Class Project)

A complete container-based scheduling and file-processing system built using **Kubernetes Jobs**, **PVC**, **Pods**, **Flask**, and **SQLite**.

---

## 📌 Project Overview

This project implements a file-processing pipeline using:

- Kubernetes Jobs  
- Persistent Volume Claims (PVC)  
- Container-based Scheduling (OS Concept)  
- Flask Web Interface  
- Kubernetes Dashboard  
- SQLite-backed file indexing  

Users can **upload**, **view**, and **delete** files using a Flask UI.  
Files are stored in a PVC and processed by Kubernetes Jobs running inside pods.  
A dashboard displays statistics such as number of images, documents, etc.

---

## 🎯 Objectives

- Implement OS-style **job scheduling** using Kubernetes Jobs & Containers  
- Build a persistent file management system using **PVC**  
- Deploy a microservice architecture with **Flask + K8s**  
- Track file metadata automatically using **SQLite DB inside containers**  
- Provide a clean UI for file upload / view / delete  
- Expose a dashboard for resource statistics  

---

## 🧩 Architecture



                     ┌─────────────────────────────┐
                     │          Flask UI            │
                     │   Upload / View / Delete     │
                     └───────────────┬─────────────┘
                                     │
                                     ▼
                     ┌─────────────────────────────┐
                     │   Kubernetes Deployment      │
                     │        (flask-site)          │
                     └───────────────┬─────────────┘
                                     │
                                     ▼
                     ┌─────────────────────────────┐
                     │     Persistent Volume        │
                     │     (PVC: file storage)      │
                     └───────────────┬─────────────┘
                                     │
                                     ▼
                     ┌─────────────────────────────┐
                     │   Kubernetes Job (processor) │
                     │ Classifies files (img/docs)  │
                     │ Updates SQLite DB            │
                     └───────────────┬─────────────┘
                                     │
                                     ▼
                     ┌─────────────────────────────┐
                     │     Dashboard Deployment     │
                     │   Shows counts/statistics    │
                     └─────────────────────────────┘





## 📁 Repository Structure


Kubernetes-File-Processing-System/

│

├── k8s-file-container/ # Backend file processor

│ ├── app/

│ ├── k8s/

│ └── process-files-job.yaml

│

├── k8s-dashboard/ # Dashboard to show file stats

│ ├── app.py

│ ├── deployment.yaml

│ ├── dashboard-deploy.yaml

│ ├── Dockerfile

│ └── pvc.yaml

│

├── flask-site/ # Flask frontend

│ ├── app.py

│ ├── templates/

│ ├── static/

│ └── flask-site-deployment.yaml

│

├── file-pvc.yaml # Persistent Volume Claim

├── process-files-job.yaml # Top-level processor job

├── setup_k8s_project.sh # Auto-deployment script

└── README.md




---

## 🖥️ Flask Web UI

The UI allows:

- Uploading files  
- Viewing images/documents  
- Deleting files  
- Navigating to dashboard  
- All operations sync with SQLite automatically  

Screenshots can be added later.

---

## ⚙️ How to Run the Project

### 1️⃣ Start Minikube
```bash
minikube start
```
### 2️⃣ Create namespace
```bash
kubectl create namespace file-demo
```
### 3️⃣ Apply PVC + Jobs
```bash
kubectl apply -f file-pvc.yaml -n file-demo
kubectl apply -f process-files-job.yaml -n file-demo
```
### 4️⃣ Deploy Flask UI
```bash
cd flask-site
kubectl apply -f flask-site-deployment.yaml -n file-demo
kubectl expose deployment flask-site --type=NodePort --port=5000 -n file-demo
flask run
```
### 5️⃣ Access Flask UI
```bash
minikube service flask-site -n file-demo --url
```

## 🌐 Dashboard

Shows:

Total Images

Total Documents

Total Files

Live counters from SQLite


## 🛠️ Tech Stack

Component	Technology

Web UI	Flask

Container Runtime	Kubernetes, Minikube

Storage	PVC / PV

Scheduling	Kubernetes Jobs

Database	SQLite

Frontend	HTML, CSS

Deployment	K8s Deployments & Services

## 🚧 Future Improvements

Add worker autoscaling (HPA)

Add Redis for message queue

Build React frontend

Add logs viewer

Add user authentication

