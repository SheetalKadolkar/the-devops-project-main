![Image](https://miro.medium.com/1%2AEVTio3p0OeFdda5MzEHCkw.jpeg)

![Image](https://docs.aws.amazon.com/images/architecture-diagrams/latest/modernize-applications-with-microservices-using-amazon-eks/images/modernize-applications-with-microservices-using-amazon-eks.png)

![Image](https://miro.medium.com/0%2AzdJ9qhUzq8CmtnLH.jpeg)

![Image](https://media2.dev.to/dynamic/image/width%3D1000%2Cheight%3D500%2Cfit%3Dcover%2Cgravity%3Dauto%2Cformat%3Dauto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fdyzwicbhbr3mq76prwwm.png)

# 🚀 AWS DevOps Project – EC2, Docker & EKS Deployment

## 📌 Project Overview

This project demonstrates an **end-to-end DevOps workflow on AWS**, covering:

* EC2 provisioning and secure SSH access
* Application containerization using Docker
* Image push to Docker Hub
* Kubernetes deployment using Amazon EKS
* Service exposure and cluster validation

---

## 🧱 Architecture

```
Developer Laptop
     |
     | SSH (key.pem)
     v
AWS EC2 (Amazon Linux)
     |
     | Docker Build & Push
     v
Docker Hub
     |
     | Kubernetes Deployment
     v
Amazon EKS Cluster
     |
     | LoadBalancer / NodePort
     v
Application Access (Port 5000)
```

---

## 🛠️ Technologies Used

| Component     | Tool       |
| ------------- | ---------- |
| Cloud         | AWS        |
| Compute       | Amazon EC2 |
| Containers    | Docker     |
| Orchestration | Kubernetes |
| Managed K8s   | Amazon EKS |
| SCM           | GitHub     |

---

## 1️⃣ EC2 Setup (Amazon Linux)

### 🔐 Security Group

* **Inbound Rule**: Allow TCP **5000**
* **SSH**: Port 22 (Your IP)

### 🔑 SSH into EC2

```bash
cd Downloads
chmod 400 key.pem
ssh -i "key.pem" ec2-user@ec2-3-85-61-152.compute-1.amazonaws.com
```

---

## 2️⃣ Install Required Packages

```bash
sudo yum update -y
sudo yum install python git docker tree pip -y
sudo systemctl start docker
sudo systemctl enable docker
```

---

## 3️⃣ Verify Installations

```bash
git --version
docker --version
python3 --version
pip --version
```

---

## 4️⃣ Clone Application Repository

```bash
git clone https://github.com/atulkamble/the-devops-project.git
cd the-devops-project
```

---

## 5️⃣ Install Application Dependencies

```bash
cd app/
pip install -r requirements.txt
```

---

## 6️⃣ Docker Build & Push

### 🔑 Login to Docker Hub

```bash
sudo docker login
```

### 🏗️ Build Image

```bash
sudo docker buildx build \
-t atuljkamble/the-devops-project:latest --load .
```

### 📤 Push Image

```bash
sudo docker push atuljkamble/the-devops-project:latest
```

### ▶️ Run Container Locally

```bash
sudo docker images
sudo docker run -d -p 5000:5000 atuljkamble/the-devops-project
sudo docker container ls
```

### ⏹️ Stop / Start Container

```bash
sudo docker container stop <container-id>
sudo docker container start <container-id>
```

---

## 7️⃣ AWS IAM & CLI Configuration

### 🔐 Create IAM User

* IAM → User → Group → Attach Policies
* Generate **Access Key & Secret Key**

### ⚙️ Configure AWS CLI

```bash
aws configure
```

**Input Values**

```
AWS Access Key ID     : ********
AWS Secret Access Key : ********
Default region name   : us-east-1
Default output format : json
```

---

## 8️⃣ Install eksctl

```bash
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH

curl -sLO https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz

curl -sL https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt \
| grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp
sudo install -m 0755 /tmp/eksctl /usr/local/bin
```

### ✅ Verify

```bash
eksctl info
```

---

## 9️⃣ Create EKS Cluster

```bash
eksctl create cluster \
--name mycluster \
--region us-east-1 \
--nodegroup-name mynodes \
--node-type t3.medium \
--nodes 2 \
--nodes-min 2 \
--nodes-max 2 \
--managed
```

---

## 🔟 Configure kubectl Access

```bash
aws eks update-kubeconfig \
--name mycluster \
--region us-east-1
```

---

## 1️⃣1️⃣ Install kubectl

```bash
curl -LO https://dl.k8s.io/release/${K8S_VERSION}/bin/linux/amd64/kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

---

## 1️⃣2️⃣ Deploy Application to Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

---

## 1️⃣3️⃣ Verify Kubernetes Resources

```bash
kubectl get nodes
kubectl get pods
kubectl get svc
kubectl get deployments
kubectl get ns
```

---

## ✅ Final Outcome

* Application containerized with Docker
* Image stored in Docker Hub
* Kubernetes workload running on Amazon EKS
* Application accessible via exposed service on **port 5000**

---

## 🧠 Key Learnings

* Secure EC2 access with key pairs
* Docker build → tag → push lifecycle
* IAM best practices for EKS
* eksctl-based Kubernetes cluster creation
* Kubernetes deployment & service management

---

### ✨ Built with ❤️ by **Atul Kamble**

Cloud & DevOps | AWS | Kubernetes | Terraform | CI/CD
