# DatenbankenFluggesellschaft
Repo für Fluggesellschaft Teil 4 
1.Set-Up 

*Pull über GitHub Desktop
Open in VS Code - danach steht das Repo zur verfügung. Es wird empfohlen, alle Dependencies in ein venv zu laden; diese bitte nicht pushen
Alle dependencies sind im requirements.txt hinterlegt und werden ins venv installiert*

Erstellung venv: (zsh und bash(?))

        python venv venvname
        venvname/bin/activate
        pip install -r requirements.txt   #Installieren aller Dependencies

        #Danach Notification von VS-Code: Neuer Interpreter verfügbar: Diesen dann auswählen
        #In Terminal steht dann (venvname) Nutzer/Pfad/bei/dir/DatenbankenFluggesellschaft > 

    

Erstellung venv: (Windows)

    python venv venvname
    venvname\scripts\activate.bat
    pip install -r requirements.txt


    #Wenn zusätliche Pakete installiert werden, bitte ins requirements mergen :
    #normale CMD
    venvname\scripts\activate.bat
    pip freeze >requirements.txt  


    Danach einfach app.py anklicken; oben rechts "Run python file", und im Browser http://127.0.0.1:5000/ öffnen.


2.Projekt Aufbau

APP --

    Login -> Beispielbenuter siehe unten
    Register  ->Nur Passenger Profile

            -- User ist Angestellter
                                --Backoffice        -- Flugschrieber ausborgen, Übersicht
                                                    -- Profil bearbeiten
                                                    -- Gebuchte Flüge sehen -- nur für Piloten

            -- User ist Passenger
                                -- Customer-Seite   --Flüge suchen
                                                    --Flüge in den Warenkorb legen
                                                    --Warenkorb -Tansaktion mit virtueller Bank-API, die eine TranskationsID zurückgibt
                                                                                            -- https://retoolapi.dev/iibcMI/transactionAPI/1
                                                    --Gebuchte Tickets aufgelistet -- Tickets ausdrucken und Storneiren 



Beispielbenutzer:


    PILOT: 
    Powers@gmail.com, password 

    TECHNIKER
    Farmer@gmail.com, password

    PASSAGIER

    Neff@gmail.com, password



    Für eine genaue Technische Dokumentation, siehe PDF: Dokumentation (/documents).
    Für Referenzen und Angaben zu AI-Tools, die in diesem Projekt verwendet wurden, siehe PDF: AI_Buddy (/documents)
