# DatenbankenFluggesellschaft
Repo für Fluggesellschaft Teil 4 


Pull über GitHub Desktop
Open in VS Code - danach steht das Repo zur verfügung. Es wird empfohlen, alle Dependencies in ein venv zu laden; diese bitte nicht pushen
Alle dependencies sind im requirements.md hinterlegt und werden ins venv installiert

Erstellung venv: (zsh und bash(?))
    python venv venvname
    venvname\scripts\activate.bat

        #Danach Notification von VS-Code: Neuer Interpreter verfügbar: Diesen dann auswählen
        #In Terminal steht dann (venvname) Nutzer/Pfad/bei/dir/DatenbankenFluggesellschaft > 

    venvname/bin/activate
    pip install -r requirements.txt   #Installieren aller Dependencies

Erstellung venv: (Windows)

    python venv venvname
    venvname\scripts\activate.bat
    pip install -r requirements.txt

        #Update für die Requirements
        #normale CMD
    venvname\scripts\activate.bat
    pip freeze >requirements.txt  


Danach einfach app.py anklicken; oben rechts "Run python file", und im Browser http://127.0.0.1:5000/ öffnen.
22.02.2024 Einloggen mit test@admin.com (daweil keine Passwort Logik)   