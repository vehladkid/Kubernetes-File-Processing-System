#!/bin/bash
set -e

echo "📁 Setting up folder structure..."
mkdir -p ~/k8s-file-container/app ~/k8s-file-container/k8s
cd ~/k8s-file-container

# ------------------------------
# 1️⃣ Flask App (File Container)
# ------------------------------
cat << 'EOF' > app/app.py
from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__)

@app.route("/")
def index():
    files = []
    for f in sorted(os.listdir(DATA_DIR)):
        path = os.path.join(DATA_DIR, f)
        stat = os.stat(path)
        files.append({"name": f, "size": stat.st_size, "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat()})
    return jsonify({"files": files})

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "no file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "empty filename"}), 400
    safe_name = file.filename
    dest = os.path.join(DATA_DIR, safe_name)
    file.save(dest)
    return jsonify({"ok": True, "path": dest})

@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    return send_from_directory(DATA_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
EOF

cat << 'EOF' > app/requirements.txt
Flask==2.2.5
EOF

cat << 'EOF' > app/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
EOF

# ------------------------------
# 2️⃣ Kubernetes Manifests
# ------------------------------
cat << 'EOF' > k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: file-demo
EOF

cat << 'EOF' > k8s/pv-hostpath.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-file-data
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: /mnt/data/file-demo
    type: DirectoryOrCreate
  persistentVolumeReclaimPolicy: Retain
EOF

cat << 'EOF' > k8s/pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-file-data
  namespace: file-demo
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
EOF

cat << 'EOF' > k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: file-service
  namespace: file-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: file-service
  template:
    metadata:
      labels:
        app: file-service
    spec:
      containers:
        - name: file-service
          image: file-service:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          volumeMounts:
            - name: file-data
              mountPath: /data
      volumes:
        - name: file-data
          persistentVolumeClaim:
            claimName: pvc-file-data
EOF

cat << 'EOF' > k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: file-service
  namespace: file-demo
spec:
  type: NodePort
  selector:
    app: file-service
  ports:
    - name: http
      port: 80
      targetPort: 8080
      nodePort: 30080
EOF

cat << 'EOF' > k8s/cronjob-process-files.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: process-files
  namespace: file-demo
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: processor
              image: busybox
              command:
                - /bin/sh
                - -c
                - |
                  echo "Processing files at $(date)"
                  cd /data || exit 0
                  if [ -z "$(ls -A .)" ]; then
                    echo "No files to process"
                    exit 0
                  fi
                  mkdir -p /tmp/out
                  TIMESTAMP=$(date +%s)
                  tar czf /tmp/out/processed-${TIMESTAMP}.tar.gz *
                  echo "Created archive processed-${TIMESTAMP}.tar.gz"
              volumeMounts:
                - name: file-data
                  mountPath: /data
          volumes:
            - name: file-data
              persistentVolumeClaim:
                claimName: pvc-file-data
EOF

echo "✅ All files created in ~/k8s-file-container"

# ------------------------------
# 3️⃣ Start Minikube and Build
# ------------------------------
echo "🚀 Starting Minikube..."
minikube start --driver=docker

echo "🐳 Setting up Docker inside Minikube..."
eval $(minikube -p minikube docker-env)

echo "🏗️ Building Docker image..."
cd ~/k8s-file-container/app
docker build -t file-service:latest .

echo "📂 Creating PV directory in Minikube..."
minikube ssh -- "sudo mkdir -p /mnt/data/file-demo && sudo chmod -R 777 /mnt/data/file-demo"

# ------------------------------
# 4️⃣ Deploy to Kubernetes
# ------------------------------
echo "📦 Deploying resources..."
cd ~/k8s-file-container/k8s
kubectl apply -f namespace.yaml
kubectl apply -f pv-hostpath.yaml
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f cronjob-process-files.yaml

echo "✅ Deployment complete!"
echo "🌐 Access your app via:"
minikube service file-service -n file-demo --url
