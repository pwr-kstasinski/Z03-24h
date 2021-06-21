@echo off

SET /P source= source?
ROBOCOPY "%source% " "%~dp0 " /e /xf *
PAUSE