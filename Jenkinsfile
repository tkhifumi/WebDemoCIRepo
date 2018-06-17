pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Building...'
        sh 'python -m py_compile demoapp/server.py'
      }
    }
    stage('Functional Test') {
      failFast true
      parallel {
        stage('Server Setup') {
          steps {
            sh 'python demoapp/server.py'
          }
        }
        stage('Login Test') {
          steps {
            sleep 2
            sh 'robot login_tests'
            sh "kill -2 `ps -ef |grep python |grep server.py |awk '{print \$2}'`"
          }
        }
      }
    }
  }
}
