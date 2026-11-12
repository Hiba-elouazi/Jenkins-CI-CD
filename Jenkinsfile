pipeline {
    agent any

    environment {
        REPO_URL   = 'https://github.com/Hiba-elouazi/Jenkins-CI-CD.git'   // URL de votre fork
        VENV_DIR   = '.venv'
        HOST       = '0.0.0.0'
        PORT       = '5000'
        APP_MODULE = 'app:app'
    }

    // Partie 5 : déclencheurs automatiques
    triggers {
        // 5.1 : build toutes les 5 minutes, même sans commit (à commenter après l'observation)
        cron('H/5 * * * *')
        // 5.2 : build à chaque push GitHub (webhook exposé avec ngrok)
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: "${REPO_URL}",
                    credentialsId: 'github-token'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            // Partie 7 : on saute les tests si le commit ne touche que README.md
            when {
                not { changeset 'README.md' }
            }
            // Partie 6 : les deux fichiers de tests tournent en parallèle
            parallel {
                stage('Tests test_app.py') {
                    steps {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            COVERAGE_FILE=.coverage.app1 python -m pytest test_app.py -v \
                                --cov=app --cov-report=term-missing --cov-report=xml:coverage-app1.xml \
                                --junitxml=results-app1.xml
                        '''
                    }
                    post { always { junit 'results-app1.xml' } }
                }
                stage('Tests test_app_2.py') {
                    steps {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            COVERAGE_FILE=.coverage.app2 python -m pytest test_app_2.py -v \
                                --cov=app --cov-report=term-missing --cov-report=xml:coverage-app2.xml \
                                --junitxml=results-app2.xml
                        '''
                    }
                    post { always { junit 'results-app2.xml' } }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate

                    # Arrête la version déployée par le build précédent, s'il y en a une
                    if [ -f gunicorn.pid ]; then
                        kill "$(cat gunicorn.pid)" 2>/dev/null || true
                        sleep 2
                    fi

                    # JENKINS_NODE_COOKIE empêche Jenkins de tuer gunicorn à la fin du build
                    JENKINS_NODE_COOKIE=dontKillMe nohup gunicorn --bind ${HOST}:${PORT} ${APP_MODULE} \
                        --pid gunicorn.pid > gunicorn.log 2>&1 &

                    sleep 3
                    python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:${PORT}/', timeout=5)"
                    echo "Application deployee : http://localhost:${PORT}"
                '''
            }
        }
    }

    post {
        success { echo "Pipeline reussi : build #${env.BUILD_NUMBER}" }
        failure { echo "Pipeline en echec : build #${env.BUILD_NUMBER}" }
    }
}
