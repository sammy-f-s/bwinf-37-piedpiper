from os import listdir
import codecs  # Fuer deutsche Umlaute


class Enttwister:

    @staticmethod
    def start():
        # Text abfragen, der getwistet werden soll
        optionen = Enttwister.liste_aller_optionen()
        for i in range(len(optionen)):
            print("[" + str(i) + "] " + optionen[i])

        print("-----------------")
        benutzer_auswahl = input("Ihre Auswahl: ")

        # Manuelle Eingabe
        if benutzer_auswahl == "0":
            benutzer_eingabe = input("Manuelle Eingabe: ")
            print("\n-------------\nEnttwisteter Text:\n-------------\n")
            # Woerter, die enttwistet werden sollen in einer Liste speichern
            woerter = benutzer_eingabe.split()
            ausgabe = ""
            # Wörter werden entwistet und durch Leerzeichen getrennt
            for wort in woerter:
                ausgabe += " " + Enttwister.enttwiste_wort(wort)
            print(ausgabe)

        # Auslesen einer zuvor bestimmten Textdatei
        else:
            print("\n-------------\nEnttwisteter Text:\n-------------\n")
            # Ausgewählte Text-Datei wird geöffnet
            with codecs.open('beispieldaten/Enttwister/' + optionen[int(benutzer_auswahl)], 'r', 'utf-8') as datei:
                # Alle Zeilen werden in einem Array gespeichert
                zeilen = datei.read().splitlines()
                # Schleife durchläuft Zeile für Zeile
                for zeile in zeilen:
                    # Wörter einer Zeile werden in einem Array gespeichert
                    woerter = zeile.split()
                    # Ausgabe für die jeweilige Zeile wird initialisiert
                    ausgabe = ""
                    # Schleife durchläuft Wort für Wort
                    for wort in woerter:
                        # Wörter werden enttwistet und mit einem Leerzeichen getrennt
                        ausgabe += " " + Enttwister.enttwiste_wort(wort)
                    # Ausgabe einer enttwisteten Zeile
                    print(ausgabe)

    @staticmethod
    def enttwiste_wort(zu_enttwistendes_wort):
        # Falls das zu enttwistende Wort drei oder weniger Buchstaben hat, muss es nicht mehr enttwisted werden
        if len(zu_enttwistendes_wort) < 4:
            return zu_enttwistendes_wort

        # Falls kein Buchstabe gefunden wird, dient -1 als Platzhalter
        erster_buchstabe_pos = -1

        # Schleife geht solange durch jeden Buchstaben, bis an Position i ein Sonderzeichen vorhanden ist
        for i in range(len(zu_enttwistendes_wort)):
            if zu_enttwistendes_wort[i].isalpha():
                erster_buchstabe_pos = i
                break

        # Sofern beim vorherigen Schleifenvorgang kein Buchstabe gefunden worden ist...
        if erster_buchstabe_pos == -1:
            # ... werden die Sonderzeichen oder Zahlen zurückgegeben
            return zu_enttwistendes_wort

        # Wenn das Wort nach dem Sonderzeichen maximal 3 Buchstaben hat...
        if len(zu_enttwistendes_wort)-erster_buchstabe_pos < 4:
            # ... wird die Zeichenkette auch zurückgegeben
            return zu_enttwistendes_wort

        # Sonderzeichen oder Zahlen vor dem zu enttwistenden Wort, falls vorhanden
        praefix = zu_enttwistendes_wort[:erster_buchstabe_pos]

        # Zweite Schleife startet beim ersten Buchstaben und endet wenn an Position des Zählers j ein Sonderzeichen
        # vorhanden ist, oder wenn das letzte Zeichen erreicht worten ist
        for j in range(erster_buchstabe_pos, len(zu_enttwistendes_wort)):

            # Wenn zweiter Zaehler auf Sonderzeichen stoesst
            if not zu_enttwistendes_wort[j].isalpha():

                # Rekursiver Methodenaufruf, damit alles, was nach dem Sonderzeichen folgt, extra enttwistet wird
                folgendes_wort = Enttwister.enttwiste_wort(zu_enttwistendes_wort[j + 1:len(zu_enttwistendes_wort)])

                # Falls es sich nur um drei Buchstaben handelt, muss nicht enttwistet werden
                if (j - erster_buchstabe_pos) < 3:
                    return praefix + zu_enttwistendes_wort[erster_buchstabe_pos:j+1] + folgendes_wort

                # Sonderzeichen an Position j
                suffix = zu_enttwistendes_wort[j]
                # Das getwistete Wort ab dem ersten Buchstaben bis zum Buchstaben vor dem Sonderzeichen an Position j
                getwistetes_wort = zu_enttwistendes_wort[erster_buchstabe_pos:j]
                # Das getwistete Wort wird mithilfe der Methode passendes_wort_in_liste enttwistet
                enttwistetes_wort = Enttwister.passendes_wort_in_liste(getwistetes_wort)
                # Rückgabe des enttwisteten Wortes mit Sonderzeichen
                return praefix + enttwistetes_wort + suffix + folgendes_wort

        # An dieser Stelle folgen keine weiteren Sonderzeichen nach dem ersten Buchstaben, da die Schleife
        # ohne Rückgabe durchegelaufen ist

        # Das getwistete Wort
        getwistetes_wort = zu_enttwistendes_wort[erster_buchstabe_pos:len(zu_enttwistendes_wort)]
        # Das getwistete Wort wird mithilfe der Methode passendes_wort_in_liste enttwistet
        enttwistetes_wort = Enttwister.passendes_wort_in_liste(getwistetes_wort)
        # Rückgabe des enttwisteten Wortes mit möglichen Sonderzeichen
        return praefix + enttwistetes_wort

    @staticmethod
    def passendes_wort_in_liste(getwistetes_wort):
        # Text-Datei mit deutschen Wörtern, alphabetisch sortiert, wird geöffnet
        with codecs.open('beispieldaten/sortierte_woerterliste.txt', 'r', 'utf-8') as sortierte_worterliste:
            # Deutsche Wörterliste wird in einem Array gespeichert
            alle_deutschen_woerter = sortierte_worterliste.read().splitlines()
            # TODO: Binary Search for the beginning letter for better performance

            # Es wird Wort für Wort die Wörterliste durchgegangen
            for wort in alle_deutschen_woerter:
                # 1. Bedingung: Wort in der Liste muss denselben Anfangs- und Endbuchstaben
                # wie das zu enttwistende Wort haben
                if not wort.startswith(getwistetes_wort[0]) or not wort.endswith(getwistetes_wort[-1]):
                    continue

                # 2. Bedingung: Länge der beiden Wörter muss gleich sein
                if not len(getwistetes_wort) == len(wort):
                    continue

                # Alphabetisch sortierte Buchstaben in der Mitte des Wortes in der Liste
                sortierte_buchstaben_1 = ''.join(sorted(wort[1:-1]))
                # Alphabetisch sortierte Buchstaben in der Mitte des Wortes, das enttwistet werden soll
                sortierte_buchstaben_2 = ''.join(sorted(getwistetes_wort[1:-1]))
                # Wenn die selben Buchstaben in der selben Anzahl in beiden Wörtern vorkommen,
                # handelt es sich mit hoher Wahrscheinlichkeit um das enttwistete Wort
                if sortierte_buchstaben_1 == sortierte_buchstaben_2:
                    # Es kann sein, dass ein anderes Wort dieselben Bedingungen erfüllt
                    # An dieser Stelle wird also die erste Übereinstimmung zurückgegeben
                    return wort

        # Wenn kein passendes Wort gefunden wurde
        return getwistetes_wort

    @staticmethod
    def liste_aller_optionen():
        # Methode soll Liste aller Optionen zurückgeben
        # User-Interface
        print("-----------------\nWelcher Text soll enttwistet werden?\n-----------------")
        # Liste der Optionen
        optionen_liste = ["Manuelle Eingabe"]
        # Alle Text-Dateien in beispieldaten > Enttwister
        # Alle Text-Dateien in beispieldaten > Enttwister
        text_dateien = [x for x in listdir("beispieldaten/Enttwister/") if x.endswith(".txt")]
        # Liste der Optionen wird um vorhandene Text-Dateien im Ordner beispieldaten > Enttwister erweitert
        optionen_liste.extend(text_dateien)
        return optionen_liste


Enttwister.start()

