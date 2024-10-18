# rushydro-gym-client-pyqt
Приложение для проекта СМР "Гимнастика"

## Preliminary actions
Before building an application, you first need to run the following commands in Powershell (administrator)
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```
```
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```
Now we can go to your IDE's terminal


### Compile build
```
pyenv install 3.6.8
```
```
pyenv local 3.6.8
```
Don't forget to change the 'api_url' in the file 'api.py ' to the address of your server

```
python -m venv venv
```
```
.\venv\Scripts\activate
```
```
pip install pyinstaller
```
```
pip install -r .\requirements.txt
```
```
pyinstaller .\app.py
```
open the app 'health.exe 'via the 'dist' folder.
