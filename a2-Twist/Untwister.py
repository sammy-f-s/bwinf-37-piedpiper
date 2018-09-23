from os import listdir
import codecs  # Fuer deutsche Umlaute


class Untwister:

    @staticmethod
    def start():
        # Text abfragen, der getwistet werden soll
        options = Untwister.query_data()
        for i in range(len(options)):
            print("[" + str(i) + "] " + options[i])

        print("-----------------")
        user_choice = input("Ihre Auswahl: ")

        # Manuelle Eingabe
        if user_choice == "0":
            user_input = input("Manuelle Eingabe: ")
            print("\n-------------\nEnttwisteter Text:\n-------------\n")
            words = user_input.split()  # Woerter, die getwistet werden sollen in einer Liste speichern
            output = ""
            for word in words:
                output += " " + Untwister.untwist_word(word)
            print(output)

        # Auslesen einer zuvor bestimmten Textdatei
        else:
            print("\n-------------\nEnttwisteter Text:\n-------------\n")
            with codecs.open('beispieldaten/Enttwister/' + options[int(user_choice)], 'r', 'utf-8') as file:
                lines = file.read().splitlines()
                for line in lines:
                    words = line.split()
                    output = ""
                    for word in words:
                        output += " " + Untwister.untwist_word(word)
                    print(output)

    @staticmethod
    def untwist_word(to_untwist):
        # Falls das Wort drei oder weniger Buchstaben hat, muss es nicht mehr enttwisted werden
        if len(to_untwist) < 4:
            return to_untwist

        # Falls kein Buchstabe gefunden wird, dient -1 als Platzhalter
        first_letter_index = -1

        # Schleife geht solange durch jeden Buchstaben, bis an Position i ein Sonderzeichen vorhanden ist
        for i in range(len(to_untwist)):
            if to_untwist[i].isalpha():
                first_letter_index = i
                break

        # Sofern beim vorherigen Schleifenvorgang kein Buchstabe gefunden worden ist...
        if first_letter_index == -1:
            # ... werden die Sonderzeichen oder Zahlen zurückgegeben
            return to_untwist

        if len(to_untwist)-first_letter_index < 4:  # Wenn das Wort nach dem Sonderzeichen maximal 3 Buchstaben hat...
            # ... wird die Zeichenkette auch zurückgegeben
            return to_untwist

        # Sonderzeichen oder Zahlen vor dem zu twistenden Wort, falls vorhanden
        prefix = to_untwist[:first_letter_index]

        # Zweite Schleife startet beim ersten Buchstaben und endet wenn an Position des Zählers j ein Sonderzeichen
        # vorhanden ist, oder wenn das letzte Zeichen erreicht worden ist
        for j in range(first_letter_index, len(to_untwist)):

            # Wenn zweiter Zaehler auf Sonderzeichen stoesst
            if not to_untwist[j].isalpha():

                # Rekursiver Methodenaufruf, damit alles, was nach dem Sonderzeichen folgt extra enttwistet wird
                next_word = Untwister.untwist_word(to_untwist[j + 1:len(to_untwist)])

                # Falls es sich nur um drei Buchstaben handelt, muss nicht enttwistet werden
                if (j - first_letter_index) < 3:
                    return prefix + to_untwist[first_letter_index:j+1] + next_word

                # Sonderzeichen an Position j
                suffix = to_untwist[j]
                # Das getwistete Wort ab dem ersten Buchstaben bis zum Buchstaben vor dem Sonderzeichen an Position j
                single_word_to_untwist = to_untwist[first_letter_index:j]
                # Das getwistete Wort wird mithilfe der Methode find_word_in_dictionary enttwistet
                untwisted_word = Untwister.find_word_in_dictionary(single_word_to_untwist)
                # Rückgabe des enttwisteten Wortes mit Sonderzeichen
                return prefix + untwisted_word + suffix + next_word

        # An dieser Stelle folgen keine weiteren Sonderzeichen nach dem ersten Buchstaben, da die Schleife
        # ohne Rückgabe durchegelaufen ist

        # Das getwistete Wort
        single_word_to_untwist = to_untwist[first_letter_index:len(to_untwist)]
        # Das getwistete Wort wird mithilfe der Methode find_word_in_dictionary enttwistet
        untwisted_word = Untwister.find_word_in_dictionary(single_word_to_untwist)
        # Rückgabe des enttwisteten Wortes mit möglichen Sonderzeichen
        return prefix + untwisted_word

    @staticmethod
    def find_word_in_dictionary(to_replace):
        # Text-Datei mit deutschen Wörtern, alphabetisch sortiert, wird geöffnet
        with codecs.open('beispieldaten/sortierte_woerterliste.txt', 'r', 'utf-8') as sorted_word_list:
            # Deutsche Wörterliste wird in einem Array gespeichert
            german_words = sorted_word_list.read().splitlines()
            # TODO: Binary Search for the beginning letter for better performance

            # Es wird Wort für Wort die Wörterliste durchgegangen
            for word in german_words:
                # 1. Bedingung: Wort in der Liste muss denselben Anfangs- und Endbuchstaben
                # wie das zu enttwistende Wort haben
                if not word.startswith(to_replace[0]) or not word.endswith(to_replace[-1]):
                    continue

                # 2. Bedingung: Länge der beiden Wörter muss gleich sein
                if not len(to_replace) == len(word):
                    continue

                # Alphabetisch sortierte Buchstaben in der Mitte der Woerter vergleichen
                sorted_mid_letters_1 = ''.join(sorted(word[1:-1]))
                sorted_mid_letters_2 = ''.join(sorted(to_replace[1:-1]))
                # Wenn die selben Buchstaben in der selben Anzahl in beiden Wörtern vorkommen
                if sorted_mid_letters_1 == sorted_mid_letters_2:
                    # Es kann sein, dass ein anderes Wort dieselben Bedingungen erfüllt
                    # An dieser Stelle wird also die erste Übereinstimmung zurückgegeben
                    return word

        # Wenn kein passendes Wort gefunden wurde
        return to_replace

    @staticmethod
    def query_data():
        # Methode soll Liste aller Optionen zurückgeben
        # User-Interface
        print("-----------------\nWelcher Text soll enttwistet werden?\n-----------------")
        # Liste der Optionen
        options_list = ["Manuelle Eingabe"]
        # Liste der Optionen wird um vorhandene Text-Dateien im Ordner beispieldaten > Enttwister erweitert
        text_files_in_sample_folder = [x for x in listdir("beispieldaten/Enttwister/") if x.endswith(".txt")]
        options_list.extend(text_files_in_sample_folder)
        return options_list


Untwister.start()

