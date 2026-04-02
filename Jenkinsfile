pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Run Backend Tests') {
            steps {
                sh 'docker-compose run --rm backend python manage.py test --verbosity=2'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully. Services are up.'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
            sh 'docker-compose down || true'
        }
        always {
            sh 'docker-compose logs --tail=50 || true'
        }
    }
}
