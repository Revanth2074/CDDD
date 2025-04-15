pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat 'docker build -t chat-sentiment-analyzer:latest .'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    bat 'echo Running tests...'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Using PowerShell to handle the OR condition properly
                    powershell 'docker stop chat-sentiment-analyzer 2>$null; $true'
                    bat 'docker run -d --name chat-sentiment-analyzer -p 5000:5000 chat-sentiment-analyzer:latest'
                }
            }
        }
    }
    
    post {
        always {
            // Using PowerShell to handle the OR condition properly
            powershell 'docker stop chat-sentiment-analyzer 2>$null; $true'
        }
    }
}