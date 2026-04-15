pipeline {
    agent any

    stages {

        stage('Checkout Multiple Repos') {
            steps {
                // Main repo (this Jenkinsfile repo)
                dir('main') {
                    checkout scm
                }

                // Repo 2
                dir('repo2') {
                    git branch: 'main', url: 'https://github.com/mrunaliKale31/devops-proj-A'
                }

                // Repo 3
                dir('repo3') {
                    git branch: 'main', url: 'https://github.com/olika-T/Jenkins-Project.git'
                }
                dir('repo4') {
                    git branch: 'main', url: 'https://github.com/KD231299/pharma-cloudops.gitc'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                dir('main') {
                    sh 'docker compose build'
                }
            }
        }

        stage('Start Services') {
            steps {
                dir('main') {
                    sh 'docker compose up -d'
                }
            }
        }

        stage('Run Backend Tests') {
            steps {
                dir('main') {
                    sh 'docker compose exec backend python manage.py test --verbosity=2'
                }
            }
        }

        stage('Database Migration') {
            steps {
                dir('main') {
                    sh 'docker compose exec backend python manage.py migrate'
                }
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
            dir('main') {
                sh 'docker compose down || true'
            }
        }

        always {
            dir('main') {
                sh 'docker compose logs --tail=50 || true'
            }
        }
    }
}