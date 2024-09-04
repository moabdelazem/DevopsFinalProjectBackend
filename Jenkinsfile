pipeline {
    agent any

    environment {
        AWS_CREDENTIALS_ID = 'aws-credentials'
        GITHUB_REPO = 'https://github.com/moabdelazem/DevopsFinalProjectBackend'
        TERRAFORM_DIR = 'terraform'
        REGION = 'us-east-1'  
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: "${env.GITHUB_REPO}"
            }
        }

        stage('Terraform Init') {
            steps {
                dir("${env.TERRAFORM_DIR}") {
                    withAWS(credentials: "${env.AWS_CREDENTIALS_ID}", region: "${env.REGION}") {
                        sh 'terraform init'
                    }
                }
            }
        }


        stage('Terraform Plan') {
            steps {
                dir("${env.TERRAFORM_DIR}") {
                    withAWS(credentials: "${env.AWS_CREDENTIALS_ID}", region: "${env.REGION}") {
                        sh 'terraform plan -out=tfplan'
                    }
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                dir("${env.TERRAFORM_DIR}") {
                    withAWS(credentials: "${env.AWS_CREDENTIALS_ID}", region: "${env.REGION}") {
                        sh 'terraform apply tfplan'
                    }
                }
            }
        }

        stage('Deploy Application to EKS') {
            steps {
                dir("${env.TERRAFORM_DIR}") {
                    withAWS(credentials: "${env.AWS_CREDENTIALS_ID}", region: "${env.REGION}") {
                        sh '''
                        # You can add your kubectl commands here
                        # For example:
                        # kubectl apply -f k8s/deployment.yaml
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}