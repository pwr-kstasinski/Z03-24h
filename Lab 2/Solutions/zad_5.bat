@echo off
ffmpeg -i %1 -vframes 1 -q:v 2 mini.jpg