pipeline {
    agent any

    environment {
        // Variáveis de ambiente, como nome das imagens e repositório Docker
        DOCKER_REGISTRY = 'seu-registro-docker'
        BACKEND_IMAGE = "${DOCKER_REGISTRY}/django-backend:latest"
        FRONTEND_IMAGE = "${DOCKER_REGISTRY}/react-frontend:latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'docker build -t ${BACKEND_IMAGE} .'
                }
            }
        }
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'docker build -t ${FRONTEND_IMAGE} .'
                }
            }
        }
        stage('Push Images') {
            steps {
                // Certifique-se de que o Jenkins está autenticado no seu registro Docker
                sh 'docker push ${BACKEND_IMAGE}'
                sh 'docker push ${FRONTEND_IMAGE}'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                // Aqui você pode usar kubectl para aplicar os manifests do diretório k8s
                sh 'kubectl apply -f k8s/'
            }
        }
    }

    post {
        success {
            echo 'Deploy realizado com sucesso!'
        }
        failure {
            echo 'Falha no pipeline.'
        }
    }
}
