pipeline {
    agent any

    environment {
        IMAGE_NAME              = 'jokenpoke-backend'
        IMAGE_TAG               = "${env.BRANCH_NAME ?: 'local'}-${env.BUILD_NUMBER}"

        COVERAGE_THRESHOLD      = '80'

        DOCKER_CREDENTIALS      = 'docker-hub-credentials'
        DOCKER_REGISTRY         = credentials('docker-registry-url')

        SUPABASE_DATABASE_URL   = credentials('supabase-database-url')

        DATABASE_URL            = 'sqlite:///./test.db'
        ALGORITHM               = 'HS256'

        SONAR_HOST_URL          = 'http://sonarqube:9000'
        SONAR_TOKEN             = credentials('sonarqube-token')

        GITHUB_TOKEN            = credentials('github-token')
        GITHUB_REPO             = 'C14-INATEL/jokenpoke-backend'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    triggers {
        // Execução diária às 18h
        cron('0 18 * * *')
        // Webhook para push
        githubPush()
    }

    stages {

        // =====================================================
        // SETUP
        // =====================================================

        stage('Build') {
            steps {
                echo 'Configurando ambiente Python...'

                sh '''
                    python3 -m venv .venv

                    .venv/bin/pip install --upgrade pip --quiet
                    .venv/bin/pip install poetry --quiet

                    .venv/bin/poetry config virtualenvs.in-project true

                    .venv/bin/poetry install \
                        --no-interaction \
                        --no-ansi
                '''
            }
        }

        // =====================================================
        // LINT
        // =====================================================

        stage('Lint') {
            steps {
                echo 'Executando verificações de lint com Ruff...'

                sh '''
                    .venv/bin/poetry run ruff check .
                    .venv/bin/poetry run ruff format --check .
                '''
            }
        }

        // =====================================================
        // TESTS
        // =====================================================

        stage('Test') {
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
                    junit(
                        allowEmptyResults: true,
                        testResults: 'reports/test-results.xml'
                    )

                    publishHTML(target: [
                        reportDir   : 'reports/coverage-html',
                        reportFiles : 'index.html',
                        reportName  : 'Relatório de Cobertura'
                    ])

                    archiveArtifacts(
                        artifacts: 'reports/coverage.xml',
                        allowEmptyArchive: true
                    )
                }
            }
        }

        // =====================================================
        // SONARQUBE
        // =====================================================

        stage('SonarQube Analysis') {
            steps {
                echo 'Executando análise estática com SonarQube...'

                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo 'Aguardando resultado do Quality Gate...'

                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
    // =========================================================
    // POST ACTIONS
    // =========================================================

    post {

        always {
            echo 'Limpando arquivos temporários...'

            sh '''
                rm -rf .venv
                rm -rf reports
                rm -f test.db
            '''

            cleanWs()
        }

        success {
            echo """
            Pipeline concluída com sucesso!

            Branch   : ${env.BRANCH_NAME ?: 'local'}
            Build    : #${env.BUILD_NUMBER}
            SonarQube: ${SONAR_HOST_URL}/dashboard?id=jokenpoke-backend
            """

            sh '''
                curl -s -X POST \
                    -H "Authorization: token ${GITHUB_TOKEN}" \
                    -H "Accept: application/vnd.github.v3+json" \
                    https://api.github.com/repos/${GITHUB_REPO}/statuses/${GIT_COMMIT} \
                    -d "{
                        \\"state\\": \\"success\\",
                        \\"description\\": \\"Pipeline passou — build, lint, testes e quality gate OK\\",
                        \\"context\\": \\"ci/jenkins\\"
                    }"
            '''
        }

        failure {
            echo """
            Pipeline falhou!

            Branch: ${env.BRANCH_NAME ?: 'local'}
            Build : #${env.BUILD_NUMBER}
            """

            sh '''
                curl -s -X POST \
                    -H "Authorization: token ${GITHUB_TOKEN}" \
                    -H "Accept: application/vnd.github.v3+json" \
                    https://api.github.com/repos/${GITHUB_REPO}/statuses/${GIT_COMMIT} \
                    -d "{
                        \\"state\\": \\"failure\\",
                        \\"description\\": \\"Pipeline falhou — verifique os logs no Jenkins\\",
                        \\"context\\": \\"ci/jenkins\\"
                    }"
            '''
        }

        unstable {
            echo 'Pipeline instável (falhas não críticas detectadas).'

            sh '''
                curl -s -X POST \
                    -H "Authorization: token ${GITHUB_TOKEN}" \
                    -H "Accept: application/vnd.github.v3+json" \
                    https://api.github.com/repos/${GITHUB_REPO}/statuses/${GIT_COMMIT} \
                    -d "{
                        \\"state\\": \\"failure\\",
                        \\"description\\": \\"Pipeline instável — falhas não críticas detectadas\\",
                        \\"context\\": \\"ci/jenkins\\"
                    }"
            '''
        }
    }
}