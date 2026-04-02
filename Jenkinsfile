pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Images') {
            steps {
                sh 'docker compose build --no-cache'
            }
        }

        stage('Run Backend Tests') {
            steps {
                sh '''
                    docker compose run --rm backend \
                        python manage.py test --verbosity=2
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker compose down --remove-orphans
                    docker compose up -d
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully. Services are up.'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
            sh 'docker compose down --remove-orphans || true'
        }
        always {
            sh 'docker compose logs --tail=50 || true'
        }
    }
}
