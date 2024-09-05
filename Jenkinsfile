pipeline {
    agent any

    environment {
        // Docker Hub credentials - set these in Jenkins credentials store
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        DOCKER_IMAGE_NAME = 'moabdelazem/devops_fp_bend'
        DOCKER_IMAGE_TAG = 'latest'
        // Terraform credentials - set these in Jenkins credentials store
        TF_VAR_AWS_ACCESS_KEY_ID = credentials('moabdelazem')
        TF_VAR_AWS_SECRET_ACCESS_KEY = credentials('moabdelazem')
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from Git
                git url: 'https://github.com/moabdelazem/DevopsFinalProjectBackend', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                     docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}", "-f app/Dockerfile app")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Log in to Docker Hub
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        // Push Docker image to Docker Hub
                        docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}").push("${DOCKER_IMAGE_TAG}")
                    }
                }
            }
        }

          stage('Terraform Init') {
            steps {
                script {
                    // Initialize Terraform
                    dir('terraform') {
                        sh 'terraform init'
                    }
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                script {
                    // Generate Terraform execution plan
                    dir('terraform') {
                        sh 'terraform plan -out=tfplan'
                    }
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                script {
                    // Apply Terraform changes
                    dir('terraform') {
                        sh 'terraform apply -auto-approve tfplan'
                    }
                }
            }
        }

            stage('Deploy to EKS') {
            steps {
                script {
                    // Configure kubectl
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        // Apply Kubernetes configuration files
                        sh 'kubectl apply -f k8s/deployment.yaml'
                        sh 'kubectl apply -f k8s/service.yaml'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Docker image successfully built and pushed to Docker Hub.'
        }
        failure {
            echo 'Build or push failed.'
        }
    }
}
