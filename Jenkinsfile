pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        PROJECT_NAME = 'ruoyi-fullstack-test'
        BUILD_NUMBER = env.BUILD_NUMBER
        TEST_REPORTS = 'reports/'
        IMAGE_TAG = "${BUILD_NUMBER}"
        TEST_EMAIL_TO = 'hejianping911@163.com'
        TEST_EMAIL_CC = ''
        SMTP_SERVER = 'smtp.163.com'
        SMTP_PORT = '587'
        SMTP_USERNAME = 'jenkins@163.com'
        SMTP_PASSWORD = credentials('jenkins-smtp-password')
    }
    
    triggers {
        pollSCM('H/15 * * * *')
        cron('0 0 * * *')
    }
    
    options {
        buildDiscarder(logRotator(
            daysToKeepStr: '30',
            numToKeepStr: '50',
            artifactDaysToKeepStr: '7',
            artifactNumToKeepStr: '10'
        ))
        timeout(time: 2, unit: 'HOURS')
        timestamps()
        ansiColor('xterm')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '========================================'
                echo 'Stage 1: 代码检出'
                echo '========================================'
                checkout scm
                bat 'git log --oneline -3'
            }
        }
        
        stage('Build Backend') {
            steps {
                echo '========================================'
                echo 'Stage 2: 构建后端应用'
                echo '========================================'
                dir('../RuoYi-Vue') {
                    bat 'mvn clean package -DskipTests -q'
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                echo '========================================'
                echo 'Stage 3: 构建前端应用'
                echo '========================================'
                dir('../RuoYi-Vue/ruoyi-ui') {
                    bat 'npm install --production'
                    bat 'npm run build:prod'
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                echo '========================================'
                echo 'Stage 4: 构建Docker镜像'
                echo '========================================'
                bat 'docker-compose build'
            }
        }
        
        stage('Start Services') {
            steps {
                echo '========================================'
                echo 'Stage 5: 启动测试环境服务'
                echo '========================================'
                bat 'docker-compose up -d'
                bat 'timeout /t 180 /nobreak'
            }
        }
        
        stage('Health Check') {
            steps {
                echo '========================================'
                echo 'Stage 6: 服务健康检查'
                echo '========================================'
                script {
                    def maxRetries = 10
                    def retryCount = 0
                    def adminHealthy = false
                    
                    while (retryCount < maxRetries && !adminHealthy) {
                        try {
                            bat 'curl -f http://localhost:8080/api/system/user/getInfo'
                            adminHealthy = true
                        } catch (Exception e) {
                            retryCount++
                            echo "服务健康检查失败，重试第 ${retryCount}/${maxRetries} 次"
                            bat 'timeout /t 30 /nobreak'
                        }
                    }
                    
                    if (!adminHealthy) {
                        error '服务启动超时'
                    }
                }
            }
        }
        
        stage('Smoke Test') {
            steps {
                echo '========================================'
                echo 'Stage 7: 冒烟测试'
                echo '========================================'
                bat 'docker exec ruoyi-test-runner pytest -m smoke -v --tb=short --html=reports/html/smoke_report.html --self-contained-html --junitxml=reports/junit/smoke.xml'
            }
            post {
                always {
                    junit 'reports/junit/smoke.xml'
                    archiveArtifacts artifacts: 'reports/html/smoke_report.html', fingerprint: true
                }
            }
        }
        
        stage('API Test') {
            steps {
                echo '========================================'
                echo 'Stage 8: API接口测试'
                echo '========================================'
                bat 'docker exec ruoyi-test-runner pytest -m api -v --tb=short --html=reports/html/api_report.html --self-contained-html --junitxml=reports/junit/api.xml -n auto'
            }
            post {
                always {
                    junit 'reports/junit/api.xml'
                    archiveArtifacts artifacts: 'reports/html/api_report.html', fingerprint: true
                }
            }
        }
        
        stage('UI Test') {
            steps {
                echo '========================================'
                echo 'Stage 9: UI自动化测试'
                echo '========================================'
                bat 'docker exec ruoyi-test-runner pytest -m ui -v --tb=short --html=reports/html/ui_report.html --self-contained-html --junitxml=reports/junit/ui.xml -n auto'
            }
            post {
                always {
                    junit 'reports/junit/ui.xml'
                    archiveArtifacts artifacts: 'reports/html/ui_report.html', fingerprint: true
                }
            }
        }
        
        stage('Integration Test') {
            steps {
                echo '========================================'
                echo 'Stage 10: 集成测试'
                echo '========================================'
                bat 'docker exec ruoyi-test-runner pytest -m integration -v --tb=short --html=reports/html/integration_report.html --self-contained-html --junitxml=reports/junit/integration.xml'
            }
            post {
                always {
                    junit 'reports/junit/integration.xml'
                    archiveArtifacts artifacts: 'reports/html/integration_report.html', fingerprint: true
                }
            }
        }
        
        stage('Performance Test') {
            steps {
                echo '========================================'
                echo 'Stage 11: 性能测试'
                echo '========================================'
                bat 'docker exec ruoyi-test-runner pytest -m performance -v --tb=short --html=reports/html/performance_report.html --self-contained-html --junitxml=reports/junit/performance.xml'
            }
            post {
                always {
                    junit 'reports/junit/performance.xml'
                    archiveArtifacts artifacts: 'reports/html/performance_report.html', fingerprint: true
                }
            }
        }
        
        stage('Security Test') {
            steps {
                echo '========================================'
                echo 'Stage 12: 安全测试'
                echo '========================================'
                bat 'docker exec ruoyi-test-runner pytest -m security -v --tb=short --html=reports/html/security_report.html --self-contained-html --junitxml=reports/junit/security.xml'
            }
            post {
                always {
                    junit 'reports/junit/security.xml'
                    archiveArtifacts artifacts: 'reports/html/security_report.html', fingerprint: true
                }
            }
        }
        
        stage('Stop Services') {
            steps {
                echo '========================================'
                echo 'Stage 13: 停止服务'
                echo '========================================'
                bat 'docker-compose down'
            }
        }
    }
    
    post {
        always {
            echo '========================================'
            echo 'Post Build: 归档测试报告'
            echo '========================================'
            archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
            junit 'reports/junit/**/*.xml'
        }
        
        success {
            echo '构建成功!'
            emailext attachLog: false,
                body: """
                <html>
                <head>
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f6f8fa; }
                    .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                    .header { padding-bottom: 16px; border-bottom: 1px solid #eaecef; margin-bottom: 20px; }
                    .header h2 { margin: 0; color: #2da44e; }
                    .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }
                    .info-item { padding: 10px; background-color: #f6f8fa; border-radius: 6px; }
                    .info-label { font-size: 12px; color: #6e7781; text-transform: uppercase; }
                    .info-value { font-size: 14px; font-weight: 600; color: #24292e; }
                    .report-section { margin-bottom: 20px; }
                    .report-section h3 { font-size: 16px; color: #24292e; margin-bottom: 12px; }
                    .report-list { list-style: none; padding: 0; }
                    .report-item { padding: 10px; border-bottom: 1px solid #eaecef; }
                    .report-item:last-child { border-bottom: none; }
                    .report-item a { color: #0969da; text-decoration: none; }
                    .report-item a:hover { text-decoration: underline; }
                    .footer { padding-top: 16px; border-top: 1px solid #eaecef; margin-top: 20px; color: #6e7781; font-size: 12px; }
                    .badge { display: inline-block; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: 600; }
                    .badge-success { background-color: #2da44e; color: white; }
                    .build-url { color: #0969da; font-size: 14px; }
                </style>
                </head>
                <body>
                <div class="container">
                    <div class="header">
                        <h2>✅ 构建成功 - RuoYi全栈测试</h2>
                        <span class="badge badge-success">SUCCESS</span>
                    </div>
                    
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">构建编号</div>
                            <div class="info-value">#${BUILD_NUMBER}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">构建状态</div>
                            <div class="info-value">${currentBuild.currentResult}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">构建时间</div>
                            <div class="info-value">${currentBuild.durationString}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">构建触发</div>
                            <div class="info-value">${currentBuild.causes[0].shortDescription}</div>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 20px; padding: 12px; background-color: #eff6ff; border-radius: 6px;">
                        <strong>构建URL:</strong> <a href="${BUILD_URL}" class="build-url">${BUILD_URL}</a>
                    </div>
                    
                    <div class="report-section">
                        <h3>📊 测试报告</h3>
                        <ul class="report-list">
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/smoke_report.html">🔹 冒烟测试报告</a></li>
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/api_report.html">🔹 API接口测试报告</a></li>
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/ui_report.html">🔹 UI自动化测试报告</a></li>
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/integration_report.html">🔹 集成测试报告</a></li>
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/performance_report.html">🔹 性能测试报告</a></li>
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/security_report.html">🔹 安全测试报告</a></li>
                        <li class="report-item"><a href="${BUILD_URL}testReport">🔹 JUnit汇总报告</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer">
                        <p>此邮件由Jenkins CI/CD流水线自动发送</p>
                        <p>项目: ${PROJECT_NAME} | 构建编号: #${BUILD_NUMBER}</p>
                    </div>
                </div>
                </body>
                </html>
                """,
                mimeType: 'text/html',
                subject: "[SUCCESS] RuoYi全栈测试构建 #${BUILD_NUMBER}",
                to: "${TEST_EMAIL_TO}",
                cc: "${TEST_EMAIL_CC}"
        }
        
        failure {
            echo '构建失败!'
            emailext attachLog: true,
                body: """
                <html>
                <head>
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f6f8fa; }
                    .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                    .header { padding-bottom: 16px; border-bottom: 1px solid #eaecef; margin-bottom: 20px; }
                    .header h2 { margin: 0; color: #cf222e; }
                    .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }
                    .info-item { padding: 10px; background-color: #fef2f2; border-radius: 6px; border: 1px solid #ffccc7; }
                    .info-label { font-size: 12px; color: #6e7781; text-transform: uppercase; }
                    .info-value { font-size: 14px; font-weight: 600; color: #24292e; }
                    .report-section { margin-bottom: 20px; }
                    .report-section h3 { font-size: 16px; color: #24292e; margin-bottom: 12px; }
                    .report-list { list-style: none; padding: 0; }
                    .report-item { padding: 10px; border-bottom: 1px solid #eaecef; }
                    .report-item:last-child { border-bottom: none; }
                    .report-item a { color: #0969da; text-decoration: none; }
                    .report-item a:hover { text-decoration: underline; }
                    .footer { padding-top: 16px; border-top: 1px solid #eaecef; margin-top: 20px; color: #6e7781; font-size: 12px; }
                    .badge { display: inline-block; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: 600; }
                    .badge-failure { background-color: #cf222e; color: white; }
                    .build-url { color: #0969da; font-size: 14px; }
                    .error-section { background-color: #fef2f2; padding: 16px; border-radius: 6px; border-left: 4px solid #cf222e; }
                    .error-section h4 { margin: 0 0 8px 0; color: #cf222e; }
                    .log-output { background-color: #1f2937; color: #f3f4f6; padding: 12px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 12px; max-height: 300px; overflow-y: auto; white-space: pre-wrap; }
                </style>
                </head>
                <body>
                <div class="container">
                    <div class="header">
                        <h2>❌ 构建失败 - RuoYi全栈测试</h2>
                        <span class="badge badge-failure">FAILURE</span>
                    </div>
                    
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">构建编号</div>
                            <div class="info-value">#${BUILD_NUMBER}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">构建状态</div>
                            <div class="info-value">${currentBuild.currentResult}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">构建时间</div>
                            <div class="info-value">${currentBuild.durationString}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">失败阶段</div>
                            <div class="info-value">${currentBuild.failedStage}</div>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 20px; padding: 12px; background-color: #eff6ff; border-radius: 6px;">
                        <strong>构建URL:</strong> <a href="${BUILD_URL}" class="build-url">${BUILD_URL}</a>
                    </div>
                    
                    <div class="error-section">
                        <h4>🚨 失败详情</h4>
                        <div class="log-output">${BUILD_LOG}</div>
                    </div>
                    
                    <div class="report-section">
                        <h3>📊 已生成的测试报告</h3>
                        <ul class="report-list">
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/smoke_report.html">🔹 冒烟测试报告</a></li>
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/api_report.html">🔹 API接口测试报告</a></li>
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/ui_report.html">🔹 UI自动化测试报告</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer">
                        <p>此邮件由Jenkins CI/CD流水线自动发送</p>
                        <p>项目: ${PROJECT_NAME} | 构建编号: #${BUILD_NUMBER}</p>
                        <p>请立即检查构建日志并修复问题</p>
                    </div>
                </div>
                </body>
                </html>
                """,
                mimeType: 'text/html',
                subject: "[FAILURE] RuoYi全栈测试构建 #${BUILD_NUMBER}",
                to: "${TEST_EMAIL_TO}",
                cc: "${TEST_EMAIL_CC}"
        }
        
        unstable {
            echo '构建不稳定!'
            emailext attachLog: false,
                body: """
                <html>
                <head>
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f6f8fa; }
                    .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                    .header { padding-bottom: 16px; border-bottom: 1px solid #eaecef; margin-bottom: 20px; }
                    .header h2 { margin: 0; color: #9e6a03; }
                    .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }
                    .info-item { padding: 10px; background-color: #fffbeb; border-radius: 6px; border: 1px solid #fed7aa; }
                    .info-label { font-size: 12px; color: #6e7781; text-transform: uppercase; }
                    .info-value { font-size: 14px; font-weight: 600; color: #24292e; }
                    .report-section { margin-bottom: 20px; }
                    .report-section h3 { font-size: 16px; color: #24292e; margin-bottom: 12px; }
                    .report-list { list-style: none; padding: 0; }
                    .report-item { padding: 10px; border-bottom: 1px solid #eaecef; }
                    .report-item:last-child { border-bottom: none; }
                    .report-item a { color: #0969da; text-decoration: none; }
                    .report-item a:hover { text-decoration: underline; }
                    .footer { padding-top: 16px; border-top: 1px solid #eaecef; margin-top: 20px; color: #6e7781; font-size: 12px; }
                    .badge { display: inline-block; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: 600; }
                    .badge-unstable { background-color: #9e6a03; color: white; }
                    .build-url { color: #0969da; font-size: 14px; }
                    .warning-section { background-color: #fffbeb; padding: 16px; border-radius: 6px; border-left: 4px solid #f59e0b; }
                    .warning-section h4 { margin: 0 0 8px 0; color: #9e6a03; }
                </style>
                </head>
                <body>
                <div class="container">
                    <div class="header">
                        <h2>⚠️ 构建不稳定 - RuoYi全栈测试</h2>
                        <span class="badge badge-unstable">UNSTABLE</span>
                    </div>
                    
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">构建编号</div>
                            <div class="info-value">#${BUILD_NUMBER}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">构建状态</div>
                            <div class="info-value">${currentBuild.currentResult}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">构建时间</div>
                            <div class="info-value">${currentBuild.durationString}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">构建触发</div>
                            <div class="info-value">${currentBuild.causes[0].shortDescription}</div>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 20px; padding: 12px; background-color: #eff6ff; border-radius: 6px;">
                        <strong>构建URL:</strong> <a href="${BUILD_URL}" class="build-url">${BUILD_URL}</a>
                    </div>
                    
                    <div class="warning-section">
                        <h4>⚠️ 警告</h4>
                        <p>构建已完成，但部分测试用例失败或不稳定。请检查测试报告以了解详细信息。</p>
                    </div>
                    
                    <div class="report-section">
                        <h3>📊 测试报告</h3>
                        <ul class="report-list">
                        <li class="report-item"><a href="${BUILD_URL}testReport">🔹 JUnit测试报告（查看失败详情）</a></li>
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/ui_report.html">🔹 UI自动化测试报告</a></li>
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/api_report.html">🔹 API接口测试报告</a></li>
                        <li class="report-item"><a href="${BUILD_URL}artifact/reports/html/smoke_report.html">🔹 冒烟测试报告</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer">
                        <p>此邮件由Jenkins CI/CD流水线自动发送</p>
                        <p>项目: ${PROJECT_NAME} | 构建编号: #${BUILD_NUMBER}</p>
                    </div>
                </div>
                </body>
                </html>
                """,
                mimeType: 'text/html',
                subject: "[UNSTABLE] RuoYi全栈测试构建 #${BUILD_NUMBER}",
                to: "${TEST_EMAIL_TO}",
                cc: "${TEST_EMAIL_CC}"
        }
    }
}
