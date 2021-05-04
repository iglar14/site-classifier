IF NOT EXIST env (py -3 -m venv %~dp0\env)

%~dp0\env\Scripts\activate.bat && pip install -r %~dp0\requirements.txt
