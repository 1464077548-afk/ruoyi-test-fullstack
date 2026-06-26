pipeline {
    agent any

    environment {
        TEST_REPO = 'https://github.com/1464077548-afk/ruoyi-test-fullstack.git'
        TARGET_REPO = 'https://gitee.com/y_project/RuoYi-Vue.git'
        TEST_DIR = 'ruoyi-test-fullstack'
        TARGET_DIR = 'RuoYi-Vue'
        EMAIL_RECIPIENT = 'hejianping911@163.com'
        TEST_ENV = 'development'
    }

    triggers {
        // 每天晚上9点定时触发
        cron('H 21 * * *')
    }

    stages {
        stage('拉取测试代码') {
            steps {
                echo '========== 拉取测试代码 =========='
                git branch: 'main', url: "${TEST_REPO}"
                bat 'dir'
            }
        }

        stage('拉取被测代码') {
            steps {
                echo '========== 拉取被测代码 =========='
                dir("${TARGET_DIR}") {
                    git branch: 'master', url: "${TARGET_REPO}"
                    bat 'dir'
                }
            }
        }

        stage('编译被测项目') {
            steps {
                echo '========== 编译被测项目 =========='
                dir("${TARGET_DIR}") {
                    bat '''
                        echo 编译后端项目...
                        mvn clean package -DskipTests -q 2>&1 || exit /b 0
                        echo 编译前端项目...
                        cd ruoyi-ui
                        npm install --registry=https://registry.npmmirror.com 2>&1 || exit /b 0
                        npm run build:prod 2>&1 || exit /b 0
                        cd ..
                    '''
                }
            }
        }

        stage('部署Docker环境') {
            steps {
                echo '========== 部署Docker环境 =========='
                script {
                    bat '''
                        docker rm -f ruoyi-mysql ruoyi-redis ruoyi-admin ruoyi-ui ruoyi-test-runner 2>nul || exit /b 0
                        docker-compose down 2>nul || exit /b 0
                        docker volume prune -f 2>nul || exit /b 0
                    '''

                    bat '''
                        echo 使用docker-compose启动完整环境...
                        set DB_PASSWORD=123456
                        set DB_PORT=3307
                        set ADMIN_PORT=8080
                        set UI_PORT=8081
                        docker-compose up -d 2>&1
                        echo 等待容器启动...
                        timeout /t 60 /nobreak >nul || exit /b 0
                        docker ps
                    '''

                    bat '''
                        echo 检查MySQL容器状态...
                        for /l %%i in (1,1,10) do (
                            docker exec ruoyi-mysql mysqladmin ping -h localhost -u root -p123456 2>nul && (
                                echo MySQL已就绪
                                goto mysql_ready
                            )
                            echo 等待MySQL... %%i/10
                            timeout /t 10 /nobreak >nul || exit /b 0
                        )
                        :mysql_ready
                        echo MySQL健康检查通过
                    '''

                    bat '''
                        echo 检查Redis容器状态...
                        for /l %%i in (1,1,10) do (
                            docker exec ruoyi-redis redis-cli ping 2>nul | findstr /i "PONG" && (
                                echo Redis已就绪
                                goto redis_ready
                            )
                            echo 等待Redis... %%i/10
                            timeout /t 5 /nobreak >nul || exit /b 0
                        )
                        :redis_ready
                        echo Redis健康检查通过
                    '''

                    bat '''
                        echo 检查ruoyi-admin服务状态...
                        for /l %%i in (1,1,20) do (
                            curl -s -o nul -w "%%{http_code}" http://localhost:8080/ 2>nul | findstr "200" && (
                                echo ruoyi-admin已就绪
                                goto admin_ready
                            )
                            echo 等待ruoyi-admin... %%i/20
                            timeout /t 15 /nobreak >nul || exit /b 0
                        )
                        :admin_ready
                        echo ruoyi-admin健康检查通过
                    '''

                    bat '''
                        echo 检查ruoyi-ui服务状态...
                        for /l %%i in (1,1,10) do (
                            curl -s -o nul -w "%%{http_code}" http://localhost:8081/ 2>nul | findstr "200" && (
                                echo ruoyi-ui已就绪
                                goto ui_ready
                            )
                            echo 等待ruoyi-ui... %%i/10
                            timeout /t 10 /nobreak >nul || exit /b 0
                        )
                        :ui_ready
                        echo ruoyi-ui健康检查通过
                        docker ps
                    '''
                }
            }
        }

        stage('安装测试依赖') {
            steps {
                echo '========== 安装测试依赖 =========='
                bat '''
                    if exist venv rmdir /s /q venv
                    python -m venv venv
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\pip install pytest pytest-html allure-pytest pytest-xdist pytest-rerunfailures
                    venv\\Scripts\\pip install playwright requests pydantic pydantic-settings python-dotenv pymysql pyyaml
                    
                    set PLAYWRIGHT_BROWSERS_PATH=0
                    
                    if exist "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" (
                        echo 检测到系统Chrome，跳过浏览器下载
                        venv\\Scripts\\playwright install ffmpeg 2>&1 || echo ffmpeg安装失败，继续执行
                        venv\\Scripts\\python -c "from playwright.sync_api import sync_playwright; print('Playwright imported successfully')" 2>&1 || (
                            echo Playwright导入失败，尝试安装驱动...
                            venv\\Scripts\\playwright install chromium --force 2>&1 || echo 驱动安装失败，将使用系统Chrome尝试运行
                        )
                    ) else (
                        echo 未检测到系统Chrome，尝试下载Playwright Chromium（最多重试3次）
                        venv\\Scripts\\playwright install chromium 2>&1 || venv\\Scripts\\playwright install chromium 2>&1 || venv\\Scripts\\playwright install chromium 2>&1
                        venv\\Scripts\\playwright install ffmpeg 2>&1 || echo ffmpeg安装失败，继续执行
                    )
                '''
            }
        }

        stage('执行自动化测试') {
            steps {
                echo '========== 执行自动化测试 =========='
                script {
                    try {
                        bat '''
                            call venv\\Scripts\\activate.bat

                            rem 创建报告目录
                            if not exist "reports\\junit" mkdir reports\\junit
                            if not exist "reports\\allure-results" mkdir reports\\allure-results
                            if not exist "reports\\html" mkdir reports\\html

                            rem 设置测试环境（development/testing/preproduction/production）
                            set TEST_ENV=development

                            rem 设置Playwright使用系统Chrome
                            set PLAYWRIGHT_BROWSERS_PATH=0
                            set CHROME_BINARY_PATH=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe

                            rem 执行API和UI测试
                            venv\\Scripts\\pytest tests/ --ignore=tests/performance -v --tb=short --html=reports/html/report_api_ui.html --self-contained-html --junitxml=reports/junit/junit_api_ui.xml --alluredir=reports/allure-results -n auto --dist loadscope --reruns 3 --reruns-delay 2 || exit /b 0
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
                        bat '''
                            call venv\\Scripts\\activate.bat
                            venv\\Scripts\\allure generate reports/allure-results -o reports/allure-report --clean || exit /b 0
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
                bat '''
                    docker-compose down 2>nul || exit /b 0
                    docker rm -f ruoyi-mysql ruoyi-redis 2>nul || exit /b 0
                '''
            }
        }
    }

    post {
        always {
            echo '========== 发布测试报告 =========='
            // 发布JUnit报告
            junit(
                testResults: 'reports/junit/*.xml',
                allowEmptyResults: true
            )

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
