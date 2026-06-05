pipeline {
    agent any

    environment {
        DEPLOY_SERVER = '18.171.244.171'
        DEPLOY_USER   = 'ubuntu'
        DEPLOY_PATH   = '/var/www/html'
    }

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'jenkins',
                    url: 'https://github.com/sorkerlimon/Microservices-Kubernetes.git'
            }
        }

        stage('Verify File') {
            steps {
                sh 'ls -la index.html'
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'deploy-server-ssh',
                        keyFileVariable: 'SSH_KEY'
                    )
                ]) {
                    sh '''
                        chmod 600 $SSH_KEY

                        ssh -i $SSH_KEY \
                            -o StrictHostKeyChecking=no \
                            $DEPLOY_USER@$DEPLOY_SERVER \
                            "echo SSH connection successful"

                        scp -i $SSH_KEY \
                            -o StrictHostKeyChecking=no \
                            index.html \
                            $DEPLOY_USER@$DEPLOY_SERVER:/tmp/index.html

                        ssh -i $SSH_KEY \
                            -o StrictHostKeyChecking=no \
                            $DEPLOY_USER@$DEPLOY_SERVER \
                            "sudo mv /tmp/index.html $DEPLOY_PATH/index.html && echo Deployed!"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Deployed successfully to $DEPLOY_SERVER"
        }
        failure {
            echo "Deployment failed!"
        }
        always {
            cleanWs()
        }
    }
}