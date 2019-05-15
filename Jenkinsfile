/*node {
    stage('build'){
     echo 'build';
    }
    
    stage('test'){
     echo 'test';
    }
    
    stage('deploy'){
     echo 'deploy';
    }
}*/
pipeline {
    agent { docker 'python:3.5.1' }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}
