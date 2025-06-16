# CI/CD Pipeline with Jenkins, Ansible, Docker, and GitHub on AWS

## 🚀 Project Overview
This project demonstrates a full CI/CD pipeline using **Jenkins**, **Ansible**, **Docker**, and **GitHub Webhooks** on **AWS EC2 instances**. Jenkins automates the workflow triggered by GitHub pushes, Ansible manages the remote server configuration and deployment, and Docker is used for containerizing the application.

---

## 🔧 Infrastructure Setup

### 1. Provision EC2 Instances
Launch **2 Ubuntu 22.04** EC2 instances:
- `jenkins-ansible` — Jenkins, Ansible, Docker, Git, Python.
- `docker-target` — Docker host (target node).

---

## 🧩 Jenkins and Ansible Configuration (jenkins-ansible EC2)

### 2. Install Java & Jenkins
```bash
sudo apt update
sudo apt install openjdk-17-jre -y
```

#### Install Jenkins
```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee   /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]   https://pkg.jenkins.io/debian-stable binary/ |   sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install jenkins -y
sudo systemctl enable jenkins
sudo systemctl start jenkins
```

- Open Jenkins at `http://<public-ip>:8080`
- Retrieve admin password:
```bash
cat /var/lib/jenkins/secrets/initialAdminPassword
```

### 3. Install Ansible
```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible -y
```

### 4. Install Docker SDK for Ansible
```bash
sudo apt install python3-pip -y
pip install docker
```

### 5. Add Target to Ansible Inventory
Edit `/etc/ansible/hosts`:
```ini
[targets]
<target-node-private-ip>
```

---

## 🐳 Docker Setup (docker-target EC2)

### 6. Install Docker
```bash
sudo apt update
sudo apt install ca-certificates curl gnupg -y
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg |   sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg]   https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

sudo usermod -aG docker ubuntu
newgrp docker
```

---

## 🔐 SSH Key Setup for Ansible to Docker Host

### 7. Jenkins User Key Generation (jenkins-ansible EC2)
```bash
sudo -i
su - jenkins
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub
```

### 8. Authorize Jenkins Public Key on Target (docker-target EC2)
```bash
sudo -i
mkdir -p ~/.ssh
vim ~/.ssh/authorized_keys
# Paste the Jenkins public key here

systemctl restart sshd
```

Test SSH:
```bash
ssh root@<docker-target-public-ip>
```

---

## 📦 Ansible Playbook Setup

### 9. Create Ansible Playbook on Jenkins Instance
```bash
sudo -i
su - jenkins
mkdir ~/playbook
cd ~/playbook
vim ansible-playbook.yaml
```

#### ansible-playbook.yaml
```yaml
- name: Build & deploy docker container
  hosts: targets
  gather_facts: false
  remote_user: root
  tasks:

    - name: Stopping existing container
      docker_container:
        name: flaskapp
        image: harshj2003/jenkins-ansible-docker:latest
        state: stopping

    - name: Removing stopped container
      docker_container:
        name: flaskapp
        image: harshj2003/jenkins-ansible-docker:latest
        state: absent

    - name: Removing previous same docker image
      docker_image:
        name: harshj2003/jenkins-ansible-docker:latest
        state: absent

    - name: Building Docker image
      docker_image:
        name: harshj2003/jenkins-ansible-docker:latest
        source: build
        build:
          path: ~/project/
        state: present

    - name: Creating the container on target
      docker_container:
        name: flaskapp
        image: harshj2003/jenkins-ansible-docker:latest
        ports:
          - 5000:5000
        state: started
```

---

## 🔁 Jenkins Pipeline Configuration

### 10. Create Freestyle Jenkins Job
- Name: `ansible-jenkins-pipeline`
- Type: Freestyle Project

#### Source Code Management
- Git > GitHub repo URL
- Branch: `*/main` (or whatever branch you use)

#### Build Triggers
- Enable: **GitHub hook trigger for GITScm polling**

#### GitHub Webhook Setup
- URL: `http://<jenkins-ip>:8080/github-webhook/`
- GitHub > Repo > Settings > Webhooks > Add webhook
- Payload type: `application/json`
- Trigger: `Send me everything`

#### Build Steps > Execute Shell
```bash
scp -r /var/lib/jenkins/workspace/ansible-jenkins-pipeline/* root@<target-ip>:~/project/
ansible-playbook /var/lib/jenkins/playbook/ansible-playbook.yaml
```

---

## ✅ Verification and Testing

### 11. Confirm Pipeline Success
- Jenkins Console Output — success
- GitHub webhook — green check
- Target node: check `~/project` files
- Docker status:
```bash
docker ps
```
- Open web app:
```
http://<target-ip>:5000
```

---

## 💡 Insights & Best Practices

### 🔹 Jenkins
- Automates your integration pipeline.
- GitHub Webhook integration provides real-time triggering.

### 🔹 Ansible
- Agentless, secure configuration management.
- Easily scalable for multi-target deployments.

### 🔹 Docker
- Containerizes and standardizes app environments.
- Eliminates platform incompatibilities.

### 🔹 GitHub Webhooks
- Ensures GitHub and Jenkins stay in sync.
- Enables fully automated CI/CD pipelines.

### 🔹 AWS
- Reliable infrastructure to host your CI/CD stack.
- Scalable across development, staging, and production.

---

## 📂 Project Structure
```
project/
├── webapp/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── Jenkins/
    └── playbook/
        └── ansible-playbook.yaml
```

---

## 📘 Conclusion
With this pipeline, you’ve built an end-to-end automated deployment workflow integrating **GitHub**, **Jenkins**, **Ansible**, and **Docker** on **AWS EC2**. Any code pushed to GitHub triggers the pipeline, builds a new Docker image, and deploys it to a remote EC2 host using Ansible.

This is a production-ready, scalable CI/CD architecture ideal for modern DevOps workflows.

---

> **Author:** Harshwardhan Jadhav  
> **GitHub:** [harshj2003](https://github.com/harshj2003)  
> **Project:** CI/CD with Jenkins, Ansible, Docker, GitHub Webhooks, AWS Cloud.
