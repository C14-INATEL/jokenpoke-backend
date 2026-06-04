pipeline {
    agent {
        docker {
            image "${env.DOCKER_HUB_USER}/jokenpoke-jenkins:latest"
            args  '--network jokenpoke-backend_jokenpoke-net -v /var/run/docker.sock:/var/run/docker.sock --group-add 0'
            alwaysPull true
        }
    }

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

        JENKINS_IMAGE_NAME      = 'jokenpoke-jenkins'
        JENKINS_IMAGE_TAG       = 'latest'

        PIPELINE_NOTIFY_EMAIL   = credentials('pipeline-notify-emails')
        SMTP_HOST               = credentials('smtp-host')
        SMTP_USER               = credentials('smtp-user')
        SMTP_PASSWORD           = credentials('smtp-password')
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

        stage('Unit Tests') {
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
                        artifacts: 'reports/test-results.xml, reports/coverage.xml, reports/coverage-html/**',
                        allowEmptyArchive: true
                    )
                }
            }
        }

        stage('Integration Test') {
            steps {
                echo 'Executando testes de integração...'
                sh '''
                    mkdir -p reports
                    .venv/bin/poetry run pytest tests/integration/ \
                    --tb=short \
                    --junitxml=reports/integration-results.xml \
                    --cov=app \
                    --cov-append \
                    --cov-report=xml:reports/coverage.xml \
                    --cov-report=html:reports/coverage-html \
                    --cov-report=term-missing \
                    -v
                '''
            }
            post {
                always {
                    junit(
                        allowEmptyResults: true,
                        testResults: 'reports/integration-results.xml'
                    )
                    archiveArtifacts(
                        artifacts: 'reports/integration-results.xml',
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

        // =====================================================
        // PACKAGE
        // =====================================================

        stage('Package') {
            steps {
                sh '''
                    mkdir -p dist
                    tar -czf dist/jokenpoke-backend-${BUILD_NUMBER}.tar.gz \
                        --exclude='.venv' \
                        --exclude='dist' \
                        --exclude='reports' \
                        --exclude='.git' \
                        --exclude='__pycache__' \
                        --exclude='*.pyc' \
                        .
                '''
            }
            post {
                always {
                    archiveArtifacts(
                        artifacts: 'dist/*.tar.gz',
                        allowEmptyArchive: false
                    )
                }
            }
        }

        // =====================================================
        // DOCKER BUILD & PUSH — IMAGEM JENKINS CUSTOMIZADA
        // =====================================================

        stage('Docker Build & Push Jenkins Image') {
            steps {
                echo 'Construindo imagem Docker customizada do Jenkins...'

                script {
                    def buildNumber   = env.BUILD_NUMBER
                    def branch        = env.BRANCH_NAME ?: 'main'
                    def commit        = env.GIT_COMMIT
                    def imageName     = env.JENKINS_IMAGE_NAME
                    def imageTag      = env.JENKINS_IMAGE_TAG

                    sh '''
                        docker build \
                            --no-cache \
                            --label "build.number=''' + buildNumber + '''" \
                            --label "build.branch=''' + branch + '''" \
                            --label "build.commit=''' + commit + '''" \
                            -t $DOCKER_HUB_USER/$JENKINS_IMAGE_NAME:$JENKINS_IMAGE_TAG \
                            -t $DOCKER_HUB_USER/$JENKINS_IMAGE_NAME:''' + buildNumber + ''' \
                            -f docker/jenkins/Dockerfile.jenkins \
                            .
                    '''

                    echo 'Publicando imagem no Docker Hub...'

                    withCredentials([usernamePassword(
                        credentialsId: env.DOCKER_CREDENTIALS,
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                            docker push $DOCKER_HUB_USER/$JENKINS_IMAGE_NAME:$JENKINS_IMAGE_TAG
                            docker push $DOCKER_HUB_USER/$JENKINS_IMAGE_NAME:''' + buildNumber + '''

                            docker logout
                        '''
                    }

                    echo """
                    Imagem publicada com sucesso!

                    Tags publicadas:
                    - ${imageName}:${imageTag}
                    - ${imageName}:${buildNumber}
                    """
                }
            }

            post {
                always {
                    sh '''
                        docker rmi $DOCKER_HUB_USER/$JENKINS_IMAGE_NAME:$JENKINS_IMAGE_TAG || true
                        docker rmi $DOCKER_HUB_USER/$JENKINS_IMAGE_NAME:$BUILD_NUMBER      || true
                    '''
                }

                failure {
                    echo 'Falha ao construir ou publicar a imagem Jenkins.'
                }
            }
        }

        // =====================================================
        // SECURITY SCAN
        // =====================================================

        stage('Security Scan') {
            steps {
                echo 'Executando varreduras de segurança...'

                sh '''
                    mkdir -p reports/security

                    # Dependências Python (CVEs conhecidas)
                    .venv/bin/poetry run pip-audit \
                        --output reports/security/pip-audit.json \
                        --format json \
                        || true

                    # Secrets e credenciais expostas no código
                    .venv/bin/poetry run detect-secrets scan \
                        --baseline .secrets.baseline \
                        > reports/security/secrets-report.json \
                        || true

                    # Análise estática de segurança (SAST)
                    .venv/bin/poetry run bandit \
                        -r app/ \
                        -f json \
                        -o reports/security/bandit-report.json \
                        --severity-level medium \
                        --confidence-level medium
                '''

                // Varredura da imagem Docker construída
                sh '''
                    trivy image \
                        --format json \
                        --output reports/security/trivy-report.json \
                        --severity HIGH,CRITICAL \
                        $DOCKER_HUB_USER/$JENKINS_IMAGE_NAME:$BUILD_NUMBER
                '''
            }

            post {
                always {
                    archiveArtifacts(
                        artifacts: 'reports/security/**',
                        allowEmptyArchive: true
                    )
                }

                failure {
                    echo 'Vulnerabilidades críticas encontradas — verifique reports/security/'
                }
            }
        }

        // =====================================================
        // SMOKE TEST
        // =====================================================

        stage('Smoke Test') {
            environment {
                DEPLOY_URL = credentials('deploy-url')
                SMOKE_USER = credentials('smoke-test-user')
                SMOKE_PASS = credentials('smoke-test-password')
            }

            steps {
                echo 'Executando smoke tests contra ambiente Railway...'

                sh '''
                    set -e

                    check_status() {
                        LABEL=$1
                        EXPECTED=$2
                        ACTUAL=$3

                        if [ "$ACTUAL" != "$EXPECTED" ]; then
                            echo "  FALHOU: $LABEL — esperado HTTP $EXPECTED, recebido $ACTUAL"
                            exit 1
                        fi

                        echo "  OK: $LABEL — HTTP $ACTUAL"
                    }

                    echo "[1/3] Health check..."

                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
                        --max-time 5 "$DEPLOY_URL/health")

                    check_status "GET /health" "200" "$STATUS"

                    echo "[2/3] Auth — login..."

                    RESPONSE=$(curl -s --max-time 10 \
                        -X POST "$DEPLOY_URL/auth/login" \
                        -H "Content-Type: application/x-www-form-urlencoded" \
                        -d "username=$SMOKE_USER&password=$SMOKE_PASS")

                    TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

                    if [ -z "$TOKEN" ]; then
                        echo "  FALHOU: POST /auth/login — token não retornado"
                        exit 1
                    fi

                    echo "  OK: POST /auth/login — token obtido"

                    echo "[3/3] Pokemons — rota pública..."

                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
                        --max-time 10 "$DEPLOY_URL/pokemons/")

                    check_status "GET /pokemons/" "200" "$STATUS"

                    echo ""
                    echo "Todos os smoke tests passaram."
                '''
            }

            post {
                failure {
                    echo 'Smoke test falhou — aplicação indisponível ou fluxo crítico quebrado.'
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

            sh 'rm -f test_integration.db || true'

            node('built-in') {
                checkout scm
                sh "python3 scripts/notify.py ${currentBuild.currentResult}"
            }
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