from random import randint


class Enttwister:

    @staticmethod
    def start():
        # Text abfragen, der getwistet werden soll
        user_input = input("Geben Sie den Text ein, der getwistet werden soll: ")
        words = user_input.split()  # Woerter, die getwistet werden sollen in einer Liste speichern
        twisted_words = []  # Liste fuer codierte Woerter initialisieren

        for word in words:
            if len(word) > 3:  # Wort muss getwisted werden
                twisted_words.append(Enttwister.twist_word(word))
            else:  # Bei drei oder weniger Buchstaben macht es keinen Sinn zu twisten
                twisted_words.append(word)

        output = "Getwisteter Text: "
        for twisted_word in twisted_words:
            output += " " + twisted_word

        print(output)

    @staticmethod
    def twist_word(to_twist):
        first_letter_index = -1  # Falls kein Buchstabe gefunden wird, dient -1 als Platzhalter
        for i in range(len(to_twist)):
            if to_twist[i].isalpha():  # Wenn Zeichen an Position i ein Buchstabe ist...
                first_letter_index = i
                break

        prefix = to_twist[:(first_letter_index + 1)]
        boundary_left = (first_letter_index + 1)

        for j in range(boundary_left, len(to_twist)):
            if not to_twist[j].isalpha():  # Wenn zweiter Zaehler auf Sonderzeichen stoesst
                boundary_right = j-1
                twisted_letters = Enttwister.twist_letters(to_twist[boundary_left:boundary_right])
                suffix = to_twist[j-1:j+1]
                next_word = Enttwister.twist_word(to_twist[j + 1:len(to_twist)])

                return prefix + twisted_letters + suffix + next_word

        boundary_right = len(to_twist)-1

        if first_letter_index == -1:  # Nur ein Sonderzeichen ist vorhanden
            return to_twist

        twisted_letters = Enttwister.twist_letters(to_twist[boundary_left:boundary_right])
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


Enttwister.start()
