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
    eingabe = []
    kleinster_platzverlust = -1
    beste_anordnung = []

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
                        platzverlust = Schrebergaerten.getPlatzverlust(neue)
                        if Schrebergaerten.kleinster_platzverlust != -1:
                            if platzverlust - Schrebergaerten.getUebrigeFlaeche(
                                    benutzte_rechtecke) > Schrebergaerten.kleinster_platzverlust:
                                continue
                        if len(neue) == len(Schrebergaerten.eingabe):
                            if platzverlust == 0:
                                return neue
                            elif platzverlust < Schrebergaerten.kleinster_platzverlust or Schrebergaerten.kleinster_platzverlust == -1:
                                Schrebergaerten.beste_anordnung.clear()
                                Schrebergaerten.beste_anordnung.extend(neue)
                                Schrebergaerten.kleinster_platzverlust = platzverlust

                        else:
                            used = []
                            used.extend(benutzte_rechtecke)
                            used.append(rechteck_index)
                            x = Schrebergaerten.finde_anordnung(neue, used)
                            if not x == [-1]:
                                return x
                            used.clear()

                        neue.clear()
        return [-1]

    @staticmethod
    def get_eckpunkte(anordnung):
        # Zunächst werden alle Eckpunkt-Koordinaten in einer Liste gespeichert
        if len(anordnung) == 0:
            return [Koordinate(0, 0)]

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
            if rechteck.ox > breite:
                breite = rechteck.ox
            if rechteck.x + rechteck.ox > breite:
                breite = rechteck.x + rechteck.ox
            if rechteck.y + rechteck.oy > hoehe:
                hoehe = rechteck.y + rechteck.oy
            if rechteck.oy > hoehe:
                hoehe = rechteck.oy
        return [breite, hoehe]

    @staticmethod
    def alle_ausrichtungen(rechteck):
        return [Koordinate(rechteck.x, rechteck.y), Koordinate(-rechteck.x, rechteck.y),
                Koordinate(rechteck.x, -rechteck.y), Koordinate(-rechteck.x, -rechteck.y)]

    @staticmethod
    # Prüfen, ob Rechteck valide gesetzt werden kann, ohne Überschneidung
    def ueberschneidung_vorhanden(anordnung, rechteck):
        # Erstmal wird überprüft, ob das zu setzende Rechteck das Koordinatensystem nicht überschneidet
        if rechteck.x + rechteck.ox < 0 or rechteck.y + rechteck.oy < 0:
            return True

        koordinatensystem_anordnung = Schrebergaerten.anordnung_in_felder(anordnung)
        koordinatensystem_rechteck = Schrebergaerten.anordnung_in_felder([rechteck])

        if len(koordinatensystem_rechteck) >= len(koordinatensystem_anordnung):
            x_range = len(koordinatensystem_rechteck)
        else:
            x_range = len(koordinatensystem_anordnung)

        if len(koordinatensystem_rechteck[0]) >= len(koordinatensystem_anordnung[0]):
            y_range = len(koordinatensystem_rechteck[0])
        else:
            y_range = len(koordinatensystem_anordnung[0])

        koordinatensystem_kombi = []
        for x_koordinate in range(x_range):
            koordinatensystem_kombi.append([])
            for y_koordinate in range(y_range):
                koordinatensystem_kombi[x_koordinate].append(False)

        for x in range(len(koordinatensystem_rechteck)):
            for y in range(len(koordinatensystem_rechteck[0])):
                if koordinatensystem_rechteck[x][y]:
                    koordinatensystem_kombi[x][y] = True

        for x in range(len(koordinatensystem_anordnung)):
            for y in range(len(koordinatensystem_anordnung[0])):
                if koordinatensystem_anordnung[x][y] and koordinatensystem_kombi[x][y]:
                    return True

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
            if rechteck.x > 0:
                x_range = range(rechteck.ox, rechteck.ox + rechteck.x)
            else:
                x_range = range(rechteck.ox + rechteck.x, rechteck.ox)

            if rechteck.y > 0:
                y_range = range(rechteck.oy, rechteck.oy + rechteck.y)
            else:
                y_range = range(rechteck.oy + rechteck.y, rechteck.oy)

            for x in x_range:
                for y in y_range:
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

    @staticmethod
    def getUebrigeFlaeche(benutzte_rechtecke):
        flaeche = 0
        for rechteck_index in benutzte_rechtecke:
            flaeche += Schrebergaerten.eingabe[rechteck_index].x * Schrebergaerten.eingabe[rechteck_index].y

        return flaeche


import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QPaintEvent, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


class Interface(QMainWindow):

    anordnung = []

    def __init__(self):
        super().__init__()
        self.title = 'Schrebergärten'
        self.left = 900
        self.top = 200
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def paintEvent(self, a0: QPaintEvent):
        hoehe = 200
        ursprung_x = 100
        ursprung_y = 100
        painter = QPainter(self)
        painter.setPen(QPen(QColor(104, 73, 61), 4, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(39,174,96), Qt.SolidPattern))

        x_max = 0
        y_max = 0

        for rechteck in Interface.anordnung:
            if rechteck.ox + rechteck.x > x_max:
                x_max = rechteck.ox + rechteck.x
            if rechteck.oy + rechteck.y > y_max:
                y_max = rechteck.oy + rechteck.y

        if x_max > y_max:
            scale = 200/x_max
        else:
            scale = 200/y_max

        for rechteck in Interface.anordnung:
            painter.drawRect(ursprung_x + rechteck.ox * scale, ursprung_y + hoehe - rechteck.oy * scale,
                             rechteck.x * scale, -rechteck.y * scale)
            if rechteck.ox + rechteck.x > x_max:
                x_max = rechteck.ox + rechteck.x
            if rechteck.oy + rechteck.y > y_max:
                y_max = rechteck.oy + rechteck.y > y_max


anzahl = int(input("Anz. der Schrebergaerten: "))
for i in range(anzahl):
    x = int(input("Schrebergarten " + str(i + 1) + " - Breite: "))
    y = int(input("Schrebergarten " + str(i + 1) + " - Höhe: "))
    Schrebergaerten.eingabe.append(Koordinate(x, y))

print("\n Anordnung wird berechnet...")
loesung = Schrebergaerten.finde_anordnung([], [])
app = QApplication(sys.argv)
if loesung != [-1]:
    Interface.anordnung = loesung

else:
    Interface.anordnung = Schrebergaerten.beste_anordnung

print("\n Anordnung gefunden! Interdace womöglich im Hintergrund")
print("--> Platzverlust: " + str(Schrebergaerten.getPlatzverlust(Interface.anordnung)))
print("--> Breite: " + str(Schrebergaerten.get_grenze(Interface.anordnung)[0]))
print("--> Höhe: " + str(Schrebergaerten.get_grenze(Interface.anordnung)[1]))
ex = Interface()
sys.exit(app.exec_())


#Beispiel 1: 25 x 15, 15 x 30, 15 x 25, 25 x 20.
#Beispiel 2: 6 x 3, 2 x 2, 3 x 1, 4 x 4, 4 x 4.
#eispiel 3: 4 x 4, 2 x 3, 6 x 1, 5 x 2, 3 x 5.

