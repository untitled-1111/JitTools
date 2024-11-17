@echo off
setlocal ENABLEDELAYEDEXPANSION ENABLEEXTENSIONS
set script_dir_path=%~dp0
set script_dir_path=%script_dir_path:~0,-1%

set cmake_scripts_dir=%script_dir_path%

call "%script_dir_path%"\""\qt-cmake.bat ^
     -DQT_BUILD_STANDALONE_TESTS=ON %*
