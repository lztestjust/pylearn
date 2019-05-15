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
node('docker') {
    checkout scm
    stage('Build') {
        docker.image('node:6.3').inside {
            sh 'npm --version'
        }
    }
}
