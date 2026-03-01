pipeline {
  agent any
  
  environment {
    IMAGE = 'iamridoydey/flask-api'
    VERSION = "${BUILD_ID}"
  }
  
  stages {
    stage('checkout') {
      steps {
        echo '-------------GIT CHECKOUT-----------------'
        git branch: 'main', url: 'https://github.com/iamridoydey/flask-api.git'
      }
    }

    stage('dockerhub-login') {
      steps {
        echo '------------DOCKERHUB LOGIN-------------'
        echo 'Logging into dockerhub...'
        withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'DOCKERHUB_PASS', usernameVariable: 'DOCKERHUB_USER')]) {
          sh '''
            echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
          '''
        }
      
        echo 'Successfully login to dockerhub'
        
      }
    }

    stage('generate-env') {
      steps {
        script {
          echo '----------------GENERATE ENV---------------'
          env.COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        }
      }
    }

    stage('build') {
      steps {
        script {
          echo '--------------BUILD-----------------'
          echo 'Building the image...'
          sh """
            docker build --network host \
              -t ${env.IMAGE}:${env.VERSION} \
              -t ${env.IMAGE}:${env.COMMIT_HASH} \
              -t ${env.IMAGE}:latest .
          """
        }
      }
    }

    stage('push') {
      steps {
        script {
          echo '-----------PUSH TO DOCKERHUB-----------'
          echo 'Pushing the image...'
          sh "docker push ${env.IMAGE}:${env.VERSION}"
          sh "docker push ${env.IMAGE}:${env.COMMIT_HASH}"
          sh "docker push ${env.IMAGE}:latest"
        }
      }
    }

    stage('clear-workspace') {
      steps {
        echo '----------CLEAR WORKSPACE---------'
        echo 'Cleaning up the workspace...'
        sh "rm -rf ${WORKSPACE}/*"
      }
    }

    stage('deploy') {
      steps {
        script {
          echo '------------DEPLOY-------------'
          echo 'Deploying...'
          sh """
            docker pull ${env.IMAGE}:latest
            docker rm -f flask-api || true
            docker run -d \
              --name flask-api \
              -p 5000:5000 \
              --restart unless-stopped \
              ${env.IMAGE}:latest
          """
        }
      }
    }

    stage('test') {
      steps {
        echo '---------------TEST----------------'
        script {
          // Wait for container to be ready
          sleep(5)
          sh '''
            curl --fail http://localhost:5000 || exit 1
            echo "Application is running successfully!"
          '''
        }
      }
    }
  }
  

}