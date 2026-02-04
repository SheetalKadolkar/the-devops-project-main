pipeline {
    agent any

    environment {
        IMAGE_NAME = "sheetalkadolkar/the-devops-project:latest"
        DOCKER_CREDS = "docker-hub-creds"
        KUBE_NAMESPACE = "default"
    }

    stages {

        stage("Clone Code") {
            steps {
                git branch: 'main',
                    url: 'https://github.com/SheetalKadolkar/the-devops-project-main.git'
            }
        }

        stage("Docker Check") {
            steps {
                sh 'docker --version'
            }
        }

        stage("Build Docker Image") {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage("Login & Push Docker Image") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CREDS}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push sheetalkadolkar/the-devops-project:latest
                    '''
                }
            }
        }

        stage("Deploy to Kubernetes") {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                        kubectl get nodes
                        kubectl apply -f k8s/deployment.yaml -n ${KUBE_NAMESPACE}
                        kubectl apply -f k8s/service.yaml -n ${KUBE_NAMESPACE}
                        kubectl rollout status deployment/flask-app -n ${KUBE_NAMESPACE}
                    '''
                }
            }
        }

    }
}
