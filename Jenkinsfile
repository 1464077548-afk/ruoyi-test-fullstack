pipeline {
    agent any

    environment {
        TEST_REPO = 'https://github.com/1464077548-afk/ruoyi-test-fullstack.git'
        TARGET_REPO = 'https://gitee.com/y_project/RuoYi-Vue.git'
        TEST_DIR = 'ruoyi-test-fullstack'
        TARGET_DIR = 'RuoYi-Vue'
        EMAIL_RECIPIENT = 'hejianping911@163.com'
    }

    triggers {
        // 每天晚上9点定时触发
        cron('H 21 * * *')
        // GitHub Webhook触发
        GenericTrigger(
            genericVariables: [
                [key: 'ref', value: '$.ref'],
                [key: 'repository', value: '$.repository.full_name']
            ],
            causeString: 'GitHub Webhook: $ref',
            printContributedVariables: true,
            printPostContent: true,
            regexpFilterText: '$ref',
            regexpFilterExpression: 'refs/heads/main'
        )
    }

    stages {
        stage('拉取测试代码') {
            steps {
                echo '========== 拉取测试代码 =========='
                git branch: 'main', url: "${TEST_REPO}"
                sh 'ls -la'
            }
        }

        stage('拉取被测代码') {
            steps {
                echo '========== 拉取被测代码 =========='
                dir("${TARGET_DIR}") {
                    git branch: 'master', url: "${TARGET_REPO}"
                    sh 'ls -la'
                }
            }
        }

        stage('部署Docker环境') {
            steps {
                echo '========== 部署Docker环境 =========='
                script {
                    // 检查并停止已存在的容器
                    sh '''
                        docker-compose down || true
                        docker-compose -f docker-compose.yml down || true
                    '''

                    // 启动Docker容器
                    sh '''
                        cd RuoYi-Vue
                        if [ -f "docker-compose.yml" ]; then
                            docker-compose up -d
                        else
                            echo "未找到docker-compose.yml，使用默认配置"
                            # 启动MySQL
                            docker run -d --name ruoyi-mysql \\n                                -e MYSQL_ROOT_PASSWORD=password \\n                                -e MYSQL_DATABASE=ry-vue \\n                                -p 3306:3306 \\n                                mysql:5.7

                            # 启动Redis
                            docker run -d --name ruoyi-redis \\n                                -p 6379:6379 \\n                                redis:latest

                            # 等待服务启动
                            sleep 30
                        fi
                    '''
                }
            }
        }

        stage('安装测试依赖') {
            steps {
                echo '========== 安装测试依赖 =========='
                sh '''
                    python -m venv venv || true
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-html allure-pytest pytest-xdist
                '''
            }
        }

        stage('执行自动化测试') {
            steps {
                echo '========== 执行自动化测试 =========='
                script {
                    try {
                        sh '''
                            . venv/bin/activate

                            # 创建报告目录
                            mkdir -p reports/junit
                            mkdir -p reports/allure-results
                            mkdir -p reports/html

                            # 执行API和UI测试
                            pytest tests/ --ignore=tests/performance \\n                                -v --tb=short \\n                                --html=reports/html/report_api_ui.html \\n                                --self-contained-html \\n                                --junitxml=reports/junit/junit_api_ui.xml \\n                                --alluredir=reports/allure-results \\n                                -n auto --dist loadscope \\n                                --reruns 3 --reruns-delay 2 || true

                            # 执行性能测试
                            pytest tests/performance/ \\n                                -v --tb=short \\n                                --html=reports/html/report_performance.html \\n                                --self-contained-html \\n                                --junitxml=reports/junit/junit_performance.xml \\n                                --alluredir=reports/allure-performance \\n                                -p no:xdist -m performance \\n                                --reruns 1 --reruns-delay 5 || true
                        '''
                    } catch (Exception e) {
                        currentBuild.result = 'UNSTABLE'
                        echo "测试执行出现异常: ${e.message}"
                    }
                }
            }
        }

        stage('生成测试报告') {
            steps {
                echo '========== 生成测试报告 =========='
                script {
                    try {
                        sh '''
                            . venv/bin/activate
                            allure generate reports/allure-results -o reports/allure-report --clean || true
                        '''
                    } catch (Exception e) {
                        echo "生成Allure报告失败: ${e.message}"
                    }
                }
            }
        }

        stage('清理Docker环境') {
            steps {
                echo '========== 清理Docker环境 =========='
                sh '''
                    docker-compose down || true
                    docker stop ruoyi-mysql ruoyi-redis || true
                    docker rm ruoyi-mysql ruoyi-redis || true
                '''
            }
        }
    }

    post {
        always {
            echo '========== 发布测试报告 =========='
            // 发布JUnit报告
            junit 'reports/junit/*.xml'

            // 发布HTML报告
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports/html',
                reportFiles: 'report_api_ui.html, report_performance.html',
                reportName: 'HTML Report'
            ])

            // 发布Allure报告
            allure(includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']])
        }

        success {
            echo '========== 构建成功，发送邮件通知 =========='
            emailext(
                subject: "【成功】RuoYi自动化测试报告 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>自动化测试执行成功</h2>
                    <p><strong>项目名称:</strong> ${env.JOB_NAME}</p>
                    <p><strong>构建编号:</strong> #${env.BUILD_NUMBER}</p>
                    <p><strong>构建时间:</strong> ${new Date()}</p>
                    <p><strong>构建URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><strong>测试报告:</strong> <a href="${env.BUILD_URL}HTML_20Report/">HTML报告</a></p>
                    <p><strong>Allure报告:</strong> <a href="${env.BUILD_URL}allure/">Allure报告</a></p>
                """,
                to: "${EMAIL_RECIPIENT}",
                mimeType: 'text/html'
            )
        }

        failure {
            echo '========== 构建失败，发送邮件通知 =========='
            emailext(
                subject: "【失败】RuoYi自动化测试报告 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>自动化测试执行失败</h2>
                    <p><strong>项目名称:</strong> ${env.JOB_NAME}</p>
                    <p><strong>构建编号:</strong> #${env.BUILD_NUMBER}</p>
                    <p><strong>构建时间:</strong> ${new Date()}</p>
                    <p><strong>构建URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><strong>控制台输出:</strong> <a href="${env.BUILD_URL}console">查看日志</a></p>
                """,
                to: "${EMAIL_RECIPIENT}",
                mimeType: 'text/html'
            )
        }

        unstable {
            echo '========== 构建不稳定，发送邮件通知 =========='
            emailext(
                subject: "【不稳定】RuoYi自动化测试报告 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>自动化测试执行不稳定（部分测试失败）</h2>
                    <p><strong>项目名称:</strong> ${env.JOB_NAME}</p>
                    <p><strong>构建编号:</strong> #${env.BUILD_NUMBER}</p>
                    <p><strong>构建时间:</strong> ${new Date()}</p>
                    <p><strong>构建URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><strong>测试报告:</strong> <a href="${env.BUILD_URL}HTML_20Report/">HTML报告</a></p>
                    <p><strong>Allure报告:</strong> <a href="${env.BUILD_URL}allure/">Allure报告</a></p>
                """,
                to: "${EMAIL_RECIPIENT}",
                mimeType: 'text/html'
            )
        }
    }
}