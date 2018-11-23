import random
from os import listdir
import codecs  # Für deutsche Umlaute


class Twister:

    @staticmethod
    def start():
        # Text abfragen, der getwistet werden soll
        optionen = Twister.liste_aller_optionen()
        for i in range(len(optionen)):
            print("[" + str(i) + "] " + optionen[i])

        print("-----------------")
        benutzer_auswahl = input("Ihre Auswahl: ")

        # Manuelle Eingabe
        if benutzer_auswahl == "0":
            benutzer_eingabe = input("Manuelle Eingabe: ")
            print("\n-------------\nGetwisteter Text:\n-------------\n")
            # Woerter, die getwistet werden sollen in einer Liste speichern
            woerter = benutzer_eingabe.split()
            ausgabe = ""
            for wort in woerter:
                ausgabe += " " + Twister.wort_twisten(wort)
            print(ausgabe)

        # Auslesen einer zuvor bestimmten Textdatei
        else:
            print("\n-------------\nGetwisteter Text:\n-------------\n")
            # Ausgewählte Text-Datei wird geöffnet
            with codecs.open('beispieldaten/Twister/' + optionen[int(benutzer_auswahl)], 'r', 'utf-8') as file:
                # Alle Zeilen werden in einem Array gespeichert
                lines = file.read().splitlines()
                # Schleife durchläuft Zeile für Zeile
                for line in lines:
                    # Wörter einer Zeile werden in einem Array gespeichert
                    woerter = line.split()
                    # Ausgabe für die jeweilige Zeile wird initialisiert
                    ausgabe = ""
                    # Schleife durchläuft Wort für Wort in der jeweiligen Zeile
                    for wort in woerter:
                        # Wörter werden getwistet und mit einem Leerzeichen getrennt
                        ausgabe += " " + Twister.wort_twisten(wort)
                    # Ausgabe einer gettwisteten Zeile
                    print(ausgabe)

    @staticmethod
    def wort_twisten(zu_twistendes_wort):
        # Falls das Wort drei oder weniger Buchstaben hat, muss es nicht mehr getwisted werden
        if len(zu_twistendes_wort) < 4:  
            return zu_twistendes_wort

        # Falls kein Buchstabe gefunden wird, dient -1 als Platzhalter
        erster_buchstabe_pos = -1

        # Schleife geht solange durch jeden Buchstaben, bis an Position i ein Sonderzeichen vorhanden ist
        for i in range(len(zu_twistendes_wort)):
            # Sofern an Position i ein Buchstabe vorhanden ist...
            if zu_twistendes_wort[i].isalpha():  
                erster_buchstabe_pos = i
                break

        # Sofern bei der vorherigen Schleife kein Buchstabe gefunden worden ist...
        if erster_buchstabe_pos == -1:  
            # ...werden die Sonderzeichen oder Zahlen zurückgegeben
            return zu_twistendes_wort

        # Sonderzeichen oder Zahlen vor dem zu twistenden Wort, falls vorhanden
        praefix = zu_twistendes_wort[:(erster_buchstabe_pos + 1)]
        linke_grenze = (erster_buchstabe_pos + 1)

        # Zweite Schleife startet beim ersten Buchstaben und endet wenn an Position des Zählers j ein Sonderzeichen
        # vorhanden ist, oder wenn das letzte Zeichen erreicht worten ist
        for j in range(linke_grenze, len(zu_twistendes_wort)):
            # Wenn die zweite Schleife auf ein Sonderzeichen stoesst
            if not zu_twistendes_wort[j].isalpha():  
                # Die Position des letzten Buchstaben wird gespeichert (eine Position vor dem Sonderzeichen)
                rechte_grenze = j-1
                # Rekursiver Methodenaufruf, damit alles, was nach dem Sonderzeichen folgt, extra getwistet wird
                next_wort = Twister.wort_twisten(zu_twistendes_wort[j + 1:len(zu_twistendes_wort)])

                # Wenn nur maximal drei Buchstaben vorhanden sind...
                if (rechte_grenze - linke_grenze) < 2:
                    # muss die aktuelle Buchstabenfolge nicht extra getwistet werden
                    return praefix + zu_twistendes_wort[erster_buchstabe_pos+1:j+1] + next_wort

                # Letzter Buchstabe und das darauffolgende Sonderzeichen 
                suffix = zu_twistendes_wort[j-1:j+1]
                # Buchstaben zwischen dem Anfangs-und Endbuchstaben werden zufällig angeordnet
                vertauschte_buchstaben = Twister.buchstaben_twisten(zu_twistendes_wort[linke_grenze:rechte_grenze])
                # Getwistetes Wort wird zurückgegeben
                return praefix + vertauschte_buchstaben + suffix + next_wort

        rechte_grenze = len(zu_twistendes_wort) - 1
        vertauschte_buchstaben = Twister.buchstaben_twisten(zu_twistendes_wort[linke_grenze:rechte_grenze])
        suffix = zu_twistendes_wort[len(zu_twistendes_wort)-1]
        return praefix + vertauschte_buchstaben + suffix

    @staticmethod
    def buchstaben_twisten(zu_twistende_buchstaben):
        # Die Buchstaben des zu twistendes Wortes in einer Liste
        buchstaben_liste = list(zu_twistende_buchstaben)
        # Zufälliges Sortieren der Items in der Buchstaben-Liste
        random.shuffle(buchstaben_liste)
        # Aus Buchstaben-Liste wieder einen String machen
        getwistete_buchstaben = ''.join(buchstaben_liste)
        return getwistete_buchstaben

    # Methode liest alle Textdateien und gibt die Liste aller Optionen zurück
    @staticmethod
    def liste_aller_optionen():
        print("-----------------\nWelcher Text soll getwistet werden?\n-----------------")
        optionen_list = ["Manuelle Eingabe"]
        text_files_in_sample_folder = [x for x in listdir("beispieldaten/Twister/") if x.endswith(".txt")]
        optionen_list.extend(text_files_in_sample_folder)
        return optionen_list


Twister.start()

