#!/bin/bash

# Update system
sudo dnf update -y

# Install Java (Jenkins requires Java 17)
sudo dnf install java-17-amazon-corretto -y

# Add Jenkins repo
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo

sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key

# Install Jenkins
sudo dnf install jenkins -y

# Start & enable Jenkins
sudo systemctl enable jenkins
sudo systemctl start jenkins

# Check status
sudo systemctl status jenkins

echo "----------------------------------------"
echo " Jenkins installed successfully! "
echo " Access Jenkins using: http://<EC2-Public-IP>:8080"
echo " Initial Admin Password:"
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
echo "----------------------------------------"
