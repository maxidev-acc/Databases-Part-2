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


            Genereller Aufbau:
            
            app.py -Main Programm, __main__, enthält die Routen
            tools.py - Hilfsklassen und deren Funktionen (Authentifizierung, Registrierung, Buchung, ...) 
            DB_Access.py - gesonderte Hilfsklasse für gekappseltnen Datenbankzugriff (SQL)

            templates/
                    *alle HTML templates, index.html als Base template*
                    customers/ -> Frontoffice Seiten für Passagiere
                    backoffice/ -> Backoffice Seiten für Angestellte (Piloten,Techniker)


            instance/
                Datenbank

            documents/ 
                PDFs des Entwurfs, Texte zu AI-Buddy, genaue Technische Dokumentation der App
                Entwurf: REL und ERM


            setup/
                SetUp Datei zum befüllen der Datenbank, SQL File mit den Table- Anweisungen, rawdata.py mit Hilfs-Objekten zur Datengeneration


            .venv/ 
                lokale Laufzeitumgebung, bitte mit .gitignore (*) erstellen









APP Aufbau --

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

                                                    --Gebuchte Tickets aufgelistet -- Tickets ausdrucken und Stornieren 



Beispielbenutzer:


    PILOT: 
    Powers@gmail.com, password 

    TECHNIKER
    Farmer@gmail.com, password

    PASSAGIER

    Neff@gmail.com, password



    Für eine genaue Technische Dokumentation, siehe PDF: Dokumentation (/documents).
    Für Referenzen und Angaben zu AI-Tools, die in diesem Projekt verwendet wurden, siehe PDF: AI_Buddy (/documents)
