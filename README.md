# DatenbankenFluggesellschaft
Repo für Fluggesellschaft Teil 4 
# 1. Set-Up 
Pull über GitHub Desktop
Open in VS Code - danach steht das Repo zur verfügung. Es wird empfohlen, alle Dependencies in ein venv zu laden; diese bitte nicht pushen
Alle dependencies sind im requirements.txt hinterlegt und werden ins venv installiert

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


    #Wenn zusätliche Pakete installiert werden, bitte ins requirements mergen :
    #normale CMD
    venvname\scripts\activate.bat
    pip freeze >requirements.txt  


Danach einfach app.py anklicken; oben rechts "Run python file", und im Browser http://127.0.0.1:5000/ öffnen.
22.02.2024 Einloggen mit test@admin.com (daweil keine Passwort Logik) 

# 2. Projekt Aufbau





APP -- User ist Angestellter
                        --Backoffice        -- Flugschrieber ausborgen, Übersicht
                                            -- Profil bearbeiten
                                            -- Gebuchte Flüge sehen -- nur für Piloten

    -- User ist Customer
                        -- Customer-Seite   --Flüge suchen
                                            --Flüge in den Warenkorb legen
                                            --Warenkorb -Tansaktion mit virtueller Bank-API, die eine TranskationsID zurückgibt
                                                                                    -- https://retoolapi.dev/iibcMI/transactionAPI/1
                                            --Gebuchte Tickets aufgelistet -- Tickets ausdrucken 





#Änderung und Impport von Models in DB


(.venv) C:\Users\maxim\Documents\GitHub\DatenbankenFluggesellschaft>.venv\Scripts\activate.bat

(.venv) C:\Users\maxim\Documents\GitHub\DatenbankenFluggesellschaft>flask shell
Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\maxim\Documents\GitHub\DatenbankenFluggesellschaft\instance
>>> from app import db, Person
>>> db.drop_all()
>>> exit()

(.venv) C:\Users\maxim\Documents\GitHub\DatenbankenFluggesellschaft>flask shell
Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\maxim\Documents\GitHub\DatenbankenFluggesellschaft\instance
>>> from app import db, Person
>>> db.create_all()
>>>