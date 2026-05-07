pipeline {
    agent any

    environment {
        IMAGE_NAME         = 'jokenpoke-backend'
        IMAGE_TAG          = "${env.BRANCH_NAME ?: 'local'}-${env.BUILD_NUMBER}"
        COVERAGE_THRESHOLD = '80'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {

        // 1. BUILD
        stage('Build') {
            steps {
                echo 'Instalando dependências com Poetry...'
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip --quiet
                    .venv/bin/pip install poetry --quiet
                    .venv/bin/poetry config virtualenvs.in-project true
                    .venv/bin/poetry install --no-interaction --no-ansi
                '''
            }
        }

        // 2. TEST
        stage('Test') {
            environment {
                DATABASE_URL = 'sqlite:///./test.db'
                SECRET_KEY   = 'test-secret-key-for-ci'
                ALGORITHM    = 'HS256'
            }
            steps {
                echo 'Executando testes com pytest...'
                sh '''
                    mkdir -p reports
                    .venv/bin/poetry run pytest tests/ \
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
                    junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
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
            sh 'rm -rf .venv test.db || true'
            cleanWs()
        }
        success {
            echo "Pipeline concluído com sucesso! Branch: ${env.BRANCH_NAME ?: 'local'} | Build: #${env.BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline falhou! Branch: ${env.BRANCH_NAME ?: 'local'} | Build: #${env.BUILD_NUMBER}"
        }
        unstable {
            echo 'Pipeline instável (testes com falhas não-críticas).'
        }
    }
}