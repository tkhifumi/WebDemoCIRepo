pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh '''echo \'Building...\'
python -m py_compile demoapp/server.py'''
      }
    }
  }
}