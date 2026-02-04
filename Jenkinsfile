pipeline {
    agent any

    environment {
        // AWS & Docker Registry
        AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_NAME = 'the-devops-project'
        IMAGE_TAG = "${BUILD_NUMBER}"
        
        // Kubernetes
        KUBE_NAMESPACE = 'default'
        EKS_CLUSTER_NAME = 'devops-cluster'
        
        // Git
        GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out code...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo '🔨 Building Docker image...'
                script {
                    sh '''
                        docker build -t ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} ${ECR_REGISTRY}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                echo '✅ Running tests...'
                script {
                    sh '''
                        docker run --rm ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} python -m pytest || true
                    '''
                }
            }
        }

        stage('Push to ECR') {
            steps {
                echo '📤 Pushing image to AWS ECR...'
                script {
                    sh '''
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        docker push ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${ECR_REGISTRY}/${IMAGE_NAME}:latest
                        echo "Image pushed: ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
                    '''
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                echo '🚀 Deploying to EKS...'
                script {
                    sh '''
                        # Update kubeconfig
                        aws eks update-kubeconfig --region ${AWS_REGION} --name ${EKS_CLUSTER_NAME}
                        
                        # Create namespace if it doesn't exist
                        kubectl create namespace ${KUBE_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
                        
                        # Update deployment with new image
                        kubectl set image deployment/flask-app \
                            flask-app=${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \
                            -n ${KUBE_NAMESPACE} || \
                        kubectl apply -f k8s/deployment.yaml -n ${KUBE_NAMESPACE}
                        
                        # Apply service configuration
                        kubectl apply -f k8s/service.yaml -n ${KUBE_NAMESPACE}
                        
                        # Check rollout status
                        kubectl rollout status deployment/flask-app -n ${KUBE_NAMESPACE}
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '🔍 Verifying deployment...'
                script {
                    sh '''
                        echo "Deployment Status:"
                        kubectl get deployment flask-app -n ${KUBE_NAMESPACE}
                        echo "\nPods Status:"
                        kubectl get pods -n ${KUBE_NAMESPACE} -l app=flask-app
                        echo "\nServices:"
                        kubectl get svc -n ${KUBE_NAMESPACE}
                    '''
                }
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up...'
            sh 'docker image prune -f || true'
        }
        success {
            echo '✨ Pipeline completed successfully!'
            echo "Deployed image: ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
    }
}
