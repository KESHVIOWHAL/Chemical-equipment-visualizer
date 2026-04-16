pipeline {
    agent any

    stages {

        stage('Checkout Multiple Repos') {
            steps {
                // Main repo
                checkout scm

                // Other repos
                dir('repo2') {
                    git branch: 'main', url: 'https://github.com/mrunaliKale31/devops-proj-A'
                }

                dir('repo3') {
                    git branch: 'main', url: 'https://github.com/olika-T/Jenkins-Project.git'
                }

                dir('repo4') {
                    git branch: 'main', url: 'https://github.com/KD231299/pharma-cloudops.git'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Run Backend Tests') {
            steps {
                sh 'docker-compose exec backend python manage.py test --verbosity=2'
            }
        }

        stage('Database Migration') {
            steps {
                sh 'docker-compose exec backend python manage.py migrate'
            }
        }

        stage('Deploy Confirmation') {
            steps {
                echo 'Deployment successful 🚀'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully ✅'
        }

        failure {
            echo 'Pipeline failed ❌'
            sh 'docker-compose down || true'
        }

        always {
            sh 'docker-compose logs --tail=50 || true'
        }
    }
}