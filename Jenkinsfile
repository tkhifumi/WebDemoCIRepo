pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Building...'
        sh 'python -m py_compile demoapp/server.py'
      }
    }
  }
}
