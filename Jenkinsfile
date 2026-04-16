pipeline {
    agent any

    stages {

        stage('Checkout Multiple Repos') {
            steps {
                checkout scm

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