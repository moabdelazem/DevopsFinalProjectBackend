// pipeline {
//     agent any

//     environment {
//         // Docker and AWS credentials (Assume these are stored in Jenkins credentials store)
//         DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
//         AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
//         AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        
//         // GitHub repository details
//         GITHUB_REPO = 'https://github.com/moabdelazem/DevopsFinalProjectBackend'
//         // Docker Hub repository details
//         DOCKER_IMAGE_NAME = 'moabdelazem/devops_fp_bend'
//         DOCKER_IMAGE_TAG = 'latest'
//         REGION = 'us-east-1'  

//         // Terraform environment variables
//         TF_VAR_aws_access_key = AWS_ACCESS_KEY_ID
//         TF_VAR_aws_secret_key = AWS_SECRET_ACCESS_KEY
//         TF_VAR_region = 'us-east-1'
//     }

//     stages {
//         stage('Clone Repository') {
//             steps {
//                 git branch: 'main', url: "${env.GITHUB_REPO}"
//             }
//         }

//         stage('Terraform Init') {
//             steps {
//                 dir("${env.TERRAFORM_DIR}") {
//                     withAWS(credentials: "${env.AWS_CREDENTIALS_ID}", region: "${env.REGION}") {
//                         sh 'terraform init'
//                     }
//                 }
//             }
//         }


//         stage('Terraform Plan') {
//             steps {
//                 dir("${env.TERRAFORM_DIR}") {
//                     withAWS(credentials: "${env.AWS_CREDENTIALS_ID}", region: "${env.REGION}") {
//                         sh 'terraform plan -out=tfplan'
//                     }
//                 }
//             }
//         }

//         stage('Terraform Apply') {
//             steps {
//                 dir("${env.TERRAFORM_DIR}") {
//                     withAWS(credentials: "${env.AWS_CREDENTIALS_ID}", region: "${env.REGION}") {
//                         sh 'terraform apply tfplan'
//                     }
//                 }
//             }
//         }

//         stage('Deploy Application to EKS') {
//             steps {
//                 dir("${env.TERRAFORM_DIR}") {
//                     withAWS(credentials: "${env.AWS_CREDENTIALS_ID}", region: "${env.REGION}") {
//                         sh '''
//                         # You can add your kubectl commands here
//                         # For example:
//                         # kubectl apply -f k8s/deployment.yaml
//                         '''
//                     }
//                 }
//             }
//         }
//     }

//     post {
//         always {
//             cleanWs()
//         }
//     }
// }

pipeline {
    agent any

    environment {
        // Docker and AWS credentials (Assume these are stored in Jenkins credentials store)
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        
        // Docker Hub repository details
        DOCKER_IMAGE_NAME = 'moabdelazem/devops_fp_bend'
        DOCKER_IMAGE_TAG = 'latest'

        // Terraform environment variables
        TF_VAR_aws_access_key = AWS_ACCESS_KEY_ID
        TF_VAR_aws_secret_key = AWS_SECRET_ACCESS_KEY
        TF_VAR_region = 'us-east-1'
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull the latest code from GitHub
                git url: 'https://github.com/moabdelazem/DevopsFinalProjectBackend', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image using the Dockerfile in the repo
                script {
                    docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Log in to Docker Hub and push the image
                    docker.withRegistry('https://index.docker.io/v1/', 'DOCKER_HUB_CREDENTIALS') {
                        docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Terraform Init') {
            steps {
                // Initialize Terraform
                dir('terraform') {
                    sh 'terraform init'
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                // Apply the Terraform configuration to build/update the infrastructure
                dir('terraform') {
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Deploy to AWS EKS') {
            steps {
                script {
                    // Configure kubectl for EKS
                    withAWS(region: "${env.TF_VAR_region}", credentials: 'aws-creds') {
                        sh '''
                        aws eks update-kubeconfig --name demo --region us-east-1
                        kubectl apply -f kubernetes/deployment.yaml
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully!'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}
