@echo off
chcp 65001 >nul
cd /d E:\ruoyi-ui\ruoyi_fullstack_test
venv\Scripts\python.exe -m pytest tests/ -v --tb=short --html=reports/html/report.html --self-contained-html --junitxml=reports/junit/junit.xml --reruns 3 --reruns-delay 2