chcp 65001

@echo off

set curPath = %cd%

cd docs

call gen_sidebar.bat

cd ../

call push.bat