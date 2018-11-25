class Koordinate:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class RechteckVektor:

    def __init__(self, breite, hoehe, ortsvektorX, ortsvektorY):
        self.x = breite
        self.y = hoehe
        self.ox = ortsvektorX
        self.oy = ortsvektorY


class Schrebergaerten:
    eingabe = [Koordinate(2, 2), Koordinate(2, 1), Koordinate(1, 3)]
    kleinster_platzverlust = -1
    beste_anordnung = []

    @staticmethod
    def start():
        print(Schrebergaerten.finde_anordnung([RechteckVektor(2, 2, 0, 0)], [0]))
        print(Schrebergaerten.beste_anordnung)

    @staticmethod
    def finde_anordnung(aktuelle_anordnung, benutzte_rechtecke):

        for rechteck_index in range(len(Schrebergaerten.eingabe)):
            if rechteck_index in benutzte_rechtecke:
                continue

            for eckpunkt in Schrebergaerten.get_eckpunkte(aktuelle_anordnung):
                for rechteck in Schrebergaerten.alle_ausrichtungen(Schrebergaerten.eingabe[rechteck_index]):

                    if not Schrebergaerten.ueberschneidung_vorhanden(aktuelle_anordnung,
                                                                     RechteckVektor(rechteck.x, rechteck.y,
                                                                                    eckpunkt.x,
                                                                                    eckpunkt.y)):
                        neue = []
                        neue.extend(aktuelle_anordnung)
                        neue.append(RechteckVektor(rechteck.x, rechteck.y,
                                                   eckpunkt.x,
                                                   eckpunkt.y))

                        neue.clear()

    @staticmethod
    def get_eckpunkte(anordnung):
        # Zunächst werden alle Eckpunkt-Koordinaten in einer Liste gespeichert
        eckpunkte_aller_rechtecke = []
        for rechteck in anordnung:
            eckpunkte_aller_rechtecke.append(Koordinate(rechteck.ox, rechteck.oy))
            eckpunkte_aller_rechtecke.append(Koordinate(rechteck.ox + rechteck.x, rechteck.oy + rechteck.y))
            eckpunkte_aller_rechtecke.append(Koordinate(rechteck.ox + rechteck.x, rechteck.oy))
            eckpunkte_aller_rechtecke.append(Koordinate(rechteck.ox, rechteck.oy + rechteck.y))

        koordinatensystem = Schrebergaerten.anordnung_in_felder(anordnung)
        eckpunkte_der_anordnung = []
        for eckpunkt in eckpunkte_aller_rechtecke:
            if eckpunkt.x == 0 and eckpunkt.y == 0:
                continue
            if eckpunkt.x == 0:
                if not koordinatensystem[0][eckpunkt.y] or not koordinatensystem[0][eckpunkt.y - 1]:
                    eckpunkte_der_anordnung.append(eckpunkt)
                continue

            if eckpunkt.y == 0:
                if not koordinatensystem[eckpunkt.x][0] or not koordinatensystem[eckpunkt.x - 1][0]:
                    eckpunkte_der_anordnung.append(eckpunkt)
                continue

            # Prüfen, ob im Umfeld von einem Kästchen ein Feld False ist. Falls ja --> Eckpunkt muss am Rand sein
            if not koordinatensystem[eckpunkt.x][eckpunkt.y] or not koordinatensystem[eckpunkt.x - 1][eckpunkt.y] or not \
                    koordinatensystem[eckpunkt.x][eckpunkt.y - 1] or not koordinatensystem[eckpunkt.x - 1][
                eckpunkt.y - 1]:
                eckpunkte_der_anordnung.append(eckpunkt)
                continue

        return eckpunkte_der_anordnung

    @staticmethod
    # Erhalte Breite und Höhe für das gesamte Vieleck der aktuellen Anordnung
    def get_grenze(anordnung):
        breite = 0
        hoehe = 0
        for rechteck in anordnung:
            if rechteck.x + rechteck.ox > breite:
                breite = rechteck.x + rechteck.ox
            if rechteck.y + rechteck.oy > hoehe:
                hoehe = rechteck.y + rechteck.oy
        return [breite, hoehe]

    @staticmethod
    def alle_ausrichtungen(rechteck):
        return [Koordinate(rechteck.x, rechteck.y), Koordinate(-rechteck.x, rechteck.y),
                Koordinate(rechteck.x, -rechteck.y), Koordinate(-rechteck.x, -rechteck.y)]

    @staticmethod
    # Prüfen, ob Rechteck valide gesetzt werden kann, ohne Überschneidung
    def ueberschneidung_vorhanden(anordnung, rechteck):
        koordinatensystem = Schrebergaerten.anordnung_in_felder(anordnung)
        print(koordinatensystem)
        if rechteck.x + rechteck.ox > rechteck.ox:
            for x in range(rechteck.ox, rechteck.x + rechteck.ox):
                if x >= len(koordinatensystem):
                    continue
                for y in range(rechteck.oy, rechteck.oy + rechteck.y):
                    if y >= len(koordinatensystem[x]):
                        continue
                    if koordinatensystem[x][y]:
                        print("-vorhanden-")
                        Schrebergaerten.displayAnordnung(anordnung)
                        return True


        print("-nicht vorhanden-")
        Schrebergaerten.displayAnordnung([rechteck])
        return False

    @staticmethod
    def anordnung_in_felder(anordnung):
        # Anschließend werden nur die Eckpunkte zurückgegeben, die Eckpunkte der gesamten Rechteck-Anordnung sind
        grenzen = Schrebergaerten.get_grenze(anordnung)
        breite = grenzen[0]
        hoehe = grenzen[1]
        koordinatensystem = []

        # Dazu wird zunächst ein Koordinatensystem erstellt, das ein Kästchen weiter in die Breite und Höhe geht
        for x_koordinate in range(breite + 1):
            koordinatensystem.append([])
            for y_koordinate in range(hoehe + 1):
                # Alle Felder des Koordinatensystems werden erstmal auf False gesetzt
                koordinatensystem[x_koordinate].append(False)

        # Die Felder in denen sich Rechtecke befinden, werden nun auf True gesetzt
        for rechteck in anordnung:
            for x in range(rechteck.ox, rechteck.ox + rechteck.x):
                for y in range(rechteck.oy, rechteck.oy + rechteck.y):
                    koordinatensystem[x][y] = True

        return koordinatensystem

    @staticmethod
    def getPlatzverlust(anordnung):
        belegte_flaeche = 0
        for rechteck in anordnung:
            belegte_flaeche += abs(rechteck.x * rechteck.y)
        dimensionen = Schrebergaerten.get_grenze(anordnung)
        return dimensionen[0] * dimensionen[1] - belegte_flaeche

    @staticmethod
    def displayAnordnung(anordnung):
        print("#ANORDNUNG -->")
        for rechteck in anordnung:
            print(str(rechteck.x) + " " + str(rechteck.y) + " " + str(rechteck.ox) + " " + str(rechteck.oy))
        print("-----------")


Schrebergaerten.start()
