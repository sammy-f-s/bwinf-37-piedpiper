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

        if user_choice == "0":
            user_input = input("Manuelle Eingabe: ")
            print("\n-------------\nEnttwisteter Text:\n-------------\n")
            words = user_input.split()  # Woerter, die getwistet werden sollen in einer Liste speichern
            output = ""
            for word in words:
                output += " " + Untwister.untwist_word(word)
            print(output)

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
        if len(to_untwist) < 4:  # Falls das Wort drei oder weniger Buchstaben hat, muss es nicht mehr enttwisted werden
            return to_untwist

        first_letter_index = -1  # Falls kein Buchstabe gefunden wird, dient -1 als Platzhalter
        for i in range(len(to_untwist)):
            if to_untwist[i].isalpha():  # Wenn Zeichen an Position i ein Buchstabe ist...
                first_letter_index = i
                break

        if first_letter_index == -1:  # Nur Sonderzeichen sind vorhanden
            return to_untwist

        if len(to_untwist)-first_letter_index < 4:  # Wenn das Wort nach dem Sonderzeichen maximal 3 Buchstaben hat
            return to_untwist

        prefix = to_untwist[:first_letter_index]

        for j in range(first_letter_index, len(to_untwist)):
            if not to_untwist[j].isalpha():  # Wenn zweiter Zaehler auf Sonderzeichen stoesst
                last_letter_index = j
                next_word = Untwister.untwist_word(to_untwist[j + 1:len(to_untwist)])

                if (last_letter_index - first_letter_index) < 3:  # Es muss nicht getwistet werden, da hoechstens drei Buchstaben
                    return prefix + to_untwist[first_letter_index:j+1] + next_word

                suffix = to_untwist[j]  # Sonderzeichen
                single_word_to_untwist = to_untwist[first_letter_index:last_letter_index]
                untwisted_word = Untwister.find_word_in_dictionary(single_word_to_untwist)
                return prefix + untwisted_word + suffix + next_word

        single_word_to_untwist = to_untwist[first_letter_index:len(to_untwist)]
        untwisted_word = Untwister.find_word_in_dictionary(single_word_to_untwist)
        return prefix + untwisted_word

    @staticmethod
    def find_word_in_dictionary(to_replace):
        with codecs.open('beispieldaten/sortierte_woerterliste.txt', 'r', 'utf-8') as sorted_word_list:
            german_words = sorted_word_list.read().splitlines()
            # TODO: Binary Search for the beginning letter for better performance
            for word in german_words:
                if not word.startswith(to_replace[0]) or not word.endswith(to_replace[-1]):
                    continue
                if not len(to_replace) == len(word):
                    continue

                # Buchstaben in der Mitte der Woerter vergleichen
                sorted_mid_letters_1 = ''.join(sorted(word[1:-1]))
                sorted_mid_letters_2 = ''.join(sorted(to_replace[1:-1]))
                if sorted_mid_letters_1 == sorted_mid_letters_2:
                    return word

        return to_replace  # Wenn kein passendes Wort gefunden wurde

    @staticmethod
    def query_data():
        print("-----------------\nWelcher Text soll enttwistet werden?\n-----------------")
        options_list = ["Manuelle Eingabe"]
        text_files_in_sample_folder = [x for x in listdir("beispieldaten/Enttwister/") if x.endswith(".txt")]
        options_list.extend(text_files_in_sample_folder)
        return options_list


Untwister.start()

