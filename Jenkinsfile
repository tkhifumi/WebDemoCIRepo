pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'python3 -m py_compile demoapp/server.py'
      }
    }
  }
}