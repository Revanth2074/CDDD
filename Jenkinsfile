pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'chat-sentiment-analyzer'
        DOCKER_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Add your test commands here
                    bat "echo Running tests..."
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    bat "docker stop ${DOCKER_IMAGE} || true"
                    bat "docker rm ${DOCKER_IMAGE} || true"
                    bat "docker run -d -p 5000:5000 --name ${DOCKER_IMAGE} -v %CD%/uploads:/app/uploads ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
    }

    post {
        failure {
            // Cleanup on failure
            bat "docker stop ${DOCKER_IMAGE} || true"
            bat "docker rm ${DOCKER_IMAGE} || true"
        }
    }
}