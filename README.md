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



#Beispielbenutzer:

Email, Passwort
admin@gmail.com, admin
maxi@gmail.com, maxi
JeffreyHarris@gmail.com, pilot
EvaCollins@gmail.com, technican





