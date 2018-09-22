from random import randint
from os import listdir


class Twister:

    @staticmethod
    def start():
        # Text abfragen, der getwistet werden soll
        options = Twister.query_data()
        for i in range(len(options)):
            print("[" + str(i) + "] " + options[i])

        print("-----------------")
        user_choice = input("Ihre Auswahl: ")

        if user_choice == "0":
            user_input = input("Manuelle Eingabe: ")
            words = user_input.split()  # Woerter, die getwistet werden sollen in einer Liste speichern
            twisted_words = []  # Liste fuer codierte Woerter initialisieren

            for word in words:
                twisted_words.append(Twister.twist_word(word))

            output = "Getwisteter Text:"
            for twisted_word in twisted_words:
                output += " " + twisted_word

            print(output)

        else:
            pass

    @staticmethod
    def twist_word(to_twist):
        if len(to_twist) < 4:  # Falls das Wort drei oder weniger Buchstaben hat, muss es nicht mehr getwisted werden
            return to_twist

        first_letter_index = -1  # Falls kein Buchstabe gefunden wird, dient -1 als Platzhalter
        for i in range(len(to_twist)):
            if to_twist[i].isalpha():  # Wenn Zeichen an Position i ein Buchstabe ist...
                first_letter_index = i
                break

        if first_letter_index == -1:  # Nur Sonderzeichen sind vorhanden
            return to_twist

        prefix = to_twist[:(first_letter_index + 1)]
        boundary_left = (first_letter_index + 1)

        for j in range(boundary_left, len(to_twist)):
            if not to_twist[j].isalpha():  # Wenn zweiter Zaehler auf Sonderzeichen stoesst
                boundary_right = j-1
                next_word = Twister.twist_word(to_twist[j + 1:len(to_twist)])

                if (boundary_right - boundary_left) < 2:  # Es muss nicht getwistet werden, da höchstens drei Buchstaben
                    return to_twist[first_letter_index:j+1] + next_word

                suffix = to_twist[j-1:j+1]
                twisted_letters = Twister.twist_letters(to_twist[boundary_left:boundary_right])

                return prefix + twisted_letters + suffix + next_word

        boundary_right = len(to_twist) - 1
        twisted_letters = Twister.twist_letters(to_twist[boundary_left:boundary_right])
        suffix = to_twist[len(to_twist)-1]
        return prefix + twisted_letters + suffix

    @staticmethod
    def twist_letters(to_twist):
        ergebnis = ""
        used_positions = []

        for _ in range(len(to_twist)):
            random_position = randint(0, len(to_twist) - 1)
            while random_position in used_positions:
                random_position = randint(0, len(to_twist) - 1)

            ergebnis += to_twist[random_position]
            used_positions.append(random_position)

        return ergebnis

    @staticmethod
    def query_data():
        print("-----------------\nWelcher Text soll getwistet werden?\n-----------------")
        options_list = ["Manuelle Eingabe"]
        text_files_in_sample_folder = [x for x in listdir("beispieldaten/Twister/") if x.endswith(".txt")]
        options_list.extend(text_files_in_sample_folder)
        return options_list


Twister.start()

