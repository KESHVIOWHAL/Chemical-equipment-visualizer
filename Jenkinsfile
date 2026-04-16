pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "devops_${BUILD_NUMBER}"
    }

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

        stage('Cleanup Old Containers') {
            steps {
                sh '''
                docker-compose down -v --remove-orphans || true
                docker system prune -f || true
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose -p $COMPOSE_PROJECT_NAME build --no-cache'
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker-compose -p $COMPOSE_PROJECT_NAME up -d'
            }
        }

        stage('Wait for Services') {
            steps {
                sh 'sleep 20'
            }
        }

        stage('Run Backend Tests') {
            steps {
                sh 'docker-compose -p $COMPOSE_PROJECT_NAME exec -T backend python manage.py test --verbosity=2'
            }
        }

        stage('Database Migration') {
            steps {
                sh 'docker-compose -p $COMPOSE_PROJECT_NAME exec -T backend python manage.py migrate'
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
        }

        always {
            sh '''
            docker-compose -p $COMPOSE_PROJECT_NAME logs --tail=50 || true
            docker-compose -p $COMPOSE_PROJECT_NAME down -v --remove-orphans || true
            '''
        }
    }
}