@echo off
pip show pipreqs || pip install pipreqs
pipreqs . --force
pause