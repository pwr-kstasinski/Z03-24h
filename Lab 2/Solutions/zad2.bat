@echo off           
rem xcopy /T - "Creates directory structure, but does not copy files. Does not
rem             include empty directories or subdirectories. /T /E includes
rem             empty directories and subdirectories."

xcopy %1 /E /T
