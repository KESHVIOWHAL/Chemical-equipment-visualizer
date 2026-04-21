pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "chemical-visualizer"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Cleanup') {
            steps {
                sh 'docker-compose down -v --remove-orphans || true'
            }
        }

        stage('Build') {
            steps {
                sh 'docker-compose build --no-cache'
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Wait for Services') {
            steps {
                sh 'sleep 15'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker-compose exec -T backend python manage.py test --verbosity=2'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment successful'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed'
        }
        always {
            sh 'docker-compose logs --tail=30 || true'
            sh 'docker-compose down -v --remove-orphans || true'
        }
    }
}
