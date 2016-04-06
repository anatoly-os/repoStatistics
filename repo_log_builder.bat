@echo off

IF "%~1" == "-h" (
@echo on
echo ----------------------------------------------------------------------------------
echo The script is used to get svn log of your working directory.
echo RSSTAT_REPO_PATH var should point to the root directory of your repo
echo 1st argument is optional - dates to build svn log: \"{y-m-d}:{y-m-d}\". {2017-01-01}:{2016-01-01} by default
echo 2nd argument is optional - file name for output log: "mylog.log". The logs/repoName_dates.log is used by default
echo ----------------------------------------------------------------------------------
EXIT
)

SET repo_path="%RSSTAT_REPO_PATH%"
IF "%repo_path%" == "" (echo "repo is undefined"
EXIT)

SET stat_path=%~dp0

if not exist "%stat_path%/logs" mkdir "%stat_path%/logs"

SET repoTemp=%repo_path%
cd /d %repoTemp:~1,3%
cd %repo_path%

SET dates=
IF "%~1" == "" (SET dates="{2017-01-01}:{2016-01-01}") ELSE (SET dates=%~1)

SET repoFolderSearcher=%repo_path%
for %%f in (%repoFolderSearcher%) do SET repoFolderName=%%~nxf

set datesToName=%dates%
set datesToName=%datesToName::=_%

if "%~2" == "" (set outputLog="%stat_path%/logs/%repoFolderName%_%datesToName%.log") else outputLog="%~2"
svn log -v --xml -r %dates% > %outputLog%

SET statPathVal=%stat_path%
cd /d %stat_path:~0,3%
cd "%stat_path%"
