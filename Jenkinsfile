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

        JENKINS_IMAGE_NAME      = 'jokenpoke-jenkins'
        JENKINS_IMAGE_TAG       = "latest"
        DOCKER_HUB_USER         = credentials('docker-hub-username')

        PIPELINE_NOTIFY_EMAIL = credentials('pipeline-notify-emails')
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
                        artifacts: 'reports/test-results.xml, reports/coverage.xml, reports/coverage-html/**',
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
        // DOCKER BUILD & PUSH — IMAGEM JENKINS CUSTOMIZADA
        // =====================================================
 
        stage('Docker Build & Push Jenkins Image') {
            steps {
                echo 'Construindo imagem Docker customizada do Jenkins...'

                script {
                    def buildNumber   = env.BUILD_NUMBER
                    def branch        = env.BRANCH_NAME ?: 'local'
                    def commit        = env.GIT_COMMIT
                    def imageName     = env.JENKINS_IMAGE_NAME
                    def imageTag      = env.JENKINS_IMAGE_TAG
                    
                    // constroi imagem a partir do Dockerfile
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

            emailext(
                subject: "[Jenkins] ✅ Pipeline OK — ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h3>Pipeline concluída com sucesso</h3>
                    <ul>
                        <li><b>Job:</b> ${env.JOB_NAME}</li>
                        <li><b>Build:</b> #${env.BUILD_NUMBER}</li>
                        <li><b>Branch:</b> ${env.BRANCH_NAME ?: 'local'}</li>
                        <li><b>Commit:</b> ${env.GIT_COMMIT}</li>
                        <li><b>Duração:</b> ${currentBuild.durationString}</li>
                    </ul>
                    <p>
                        🔍 <a href="${env.BUILD_URL}">Ver build no Jenkins</a>

                        📊 <a href="${SONAR_HOST_URL}/dashboard?id=jokenpoke-backend">Ver análise no SonarQube</a>
                    </p>
                """,
                mimeType: 'text/html',
                to: "${PIPELINE_NOTIFY_EMAIL}"
            )
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

            emailext(
                subject: "[Jenkins] ❌ Pipeline FALHOU — ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h3>Pipeline falhou</h3>
                    <ul>
                        <li><b>Job:</b> ${env.JOB_NAME}</li>
                        <li><b>Build:</b> #${env.BUILD_NUMBER}</li>
                        <li><b>Branch:</b> ${env.BRANCH_NAME ?: 'local'}</li>
                        <li><b>Commit:</b> ${env.GIT_COMMIT}</li>
                        <li><b>Duração:</b> ${currentBuild.durationString}</li>
                    </ul>
                    <p>🔍 <a href="${env.BUILD_URL}console">Ver logs no Jenkins</a></p>
                """,
                mimeType: 'text/html',
                to: "${PIPELINE_NOTIFY_EMAIL}"
            )
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

            emailext(
                subject: "[Jenkins] ⚠️ Pipeline INSTÁVEL — ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h3>Pipeline instável — falhas não críticas detectadas</h3>
                    <ul>
                        <li><b>Job:</b> ${env.JOB_NAME}</li>
                        <li><b>Build:</b> #${env.BUILD_NUMBER}</li>
                        <li><b>Branch:</b> ${env.BRANCH_NAME ?: 'local'}</li>
                        <li><b>Commit:</b> ${env.GIT_COMMIT}</li>
                        <li><b>Duração:</b> ${currentBuild.durationString}</li>
                    </ul>
                    <p>🔍 <a href="${env.BUILD_URL}console">Ver logs no Jenkins</a></p>
                """,
                mimeType: 'text/html',
                to: "${PIPELINE_NOTIFY_EMAIL}"
            )
        }
    }
}