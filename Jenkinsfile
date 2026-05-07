pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock -u root'
        }
    }

    environment {
        PYTHON_VERSION    = '3.12'
        IMAGE_NAME        = 'jokenpoke-backend'
        IMAGE_TAG         = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
        DOCKER_REGISTRY   = credentials('docker-registry-url')
        DOCKER_CREDENTIALS = 'docker-hub-credentials'
        COVERAGE_THRESHOLD = '80'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {

        // BUILD
        stage('Build') {
            steps {
                echo 'Instalando dependências com Poetry...'
                sh '''
                    pip install --upgrade pip
                    pip install poetry
                    poetry config virtualenvs.in-project true
                    poetry install --no-interaction --no-ansi
                '''
            }
        }

        // TESTES UNITÁRIOS + COBERTURA
        stage('Test') {
            environment {
                DATABASE_URL = 'sqlite:///./test.db'
                SECRET_KEY   = 'test-secret-key-for-ci'
                ALGORITHM    = 'HS256'
            }
            steps {
                echo 'Executando testes com pytest...'
                sh '''
                    poetry run pytest tests/ \
                        --tb=short \
                        --junitxml=reports/test-results.xml \
                        --cov=app \
                        --cov-report=xml:reports/coverage.xml \
                        --cov-report=html:reports/coverage-html \
                        --cov-report=term-missing \
                        --cov-fail-under=${COVERAGE_THRESHOLD}
                '''
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                    publishHTML(target: [
                        reportDir  : 'reports/coverage-html',
                        reportFiles: 'index.html',
                        reportName : 'Coverage Report'
                    ])
                    archiveArtifacts artifacts: 'reports/coverage.xml', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo 'Limpando artefatos temporários...'
            sh '''
                docker image prune -f || true
                rm -rf .venv test.db || true
            '''
            cleanWs()
        }
        success {
            echo "Pipeline concluído com sucesso! Branch: ${env.BRANCH_NAME} | Build: #${env.BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline falhou! Verifique os logs. Branch: ${env.BRANCH_NAME} | Build: #${env.BUILD_NUMBER}"
        }
        unstable {
            echo "Pipeline instável (testes com falhas não-críticas)."
        }
    }
}