import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QPaintEvent, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


class Koordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Mit einem RechteckVektor-Objekt lässt sich ein Rechteck im Koordinatensystem darstellen
class RechteckVektor:
    def __init__(self, richtung_x, richtung_y, ortsvektor_x, ortsvektor_y):
        self.x = richtung_x
        self.y = richtung_y
        self.ox = ortsvektor_x
        self.oy = ortsvektor_y


class Schrebergaerten:
    eingabe = []
    kleinster_platzverlust = -1  # -1 dient als Platzhalter, falls noch kein Platzverlust berechnet wurde
    beste_anordnung = []

    @staticmethod
    def finde_anordnung(aktuelle_anordnung, benutzte_rechtecke):
        # Es wird jedes Rechteck durchgegangen...
        for rechteck_index in range(len(Schrebergaerten.eingabe)):
            # ... mit Ausnahme von Rechtecken, die in der aktuellen Anordnung bereits vorhanden sind
            if rechteck_index in benutzte_rechtecke:
                continue
            # Jeder Eckpunkt der aktuellen Anordnung wird durchgegangen
            for eckpunkt in Schrebergaerten.get_eckpunkte(aktuelle_anordnung):
                # Jede mögliche Ausrichtung wird in Betracht gezogen
                for rechteck in Schrebergaerten.alle_ausrichtungen(Schrebergaerten.eingabe[rechteck_index]):
                    # Es wird überprüft, ob ausgerichtetes Rechteck an diesem Eckpunkt valide gesetzt werden kann
                    if not Schrebergaerten.ueberschneidung_vorhanden(aktuelle_anordnung,
                                                                     RechteckVektor(rechteck.x, rechteck.y,
                                                                                    eckpunkt.x,
                                                                                    eckpunkt.y)):
                        # Neue Anordnung wird in einer Liste gespeichert
                        neue_anordnung = []
                        neue_anordnung.extend(aktuelle_anordnung)
                        neue_anordnung.append(RechteckVektor(rechteck.x, rechteck.y,
                                                             eckpunkt.x,
                                                             eckpunkt.y))
                        # Platzverlust der neuen Anordnung wird ermittelt
                        platzverlust = Schrebergaerten.getPlatzverlust(neue_anordnung)

                        # Falls es noch keine beste Anordnung gibt
                        if Schrebergaerten.kleinster_platzverlust != -1:
                            # Falls die Teillösung aussichtslos ist
                            if platzverlust - Schrebergaerten.getUebrigeFlaeche(
                                    benutzte_rechtecke) >= Schrebergaerten.kleinster_platzverlust:
                                continue
                        # Wenn die neue Anordnung vollständig ist
                        if len(neue_anordnung) == len(Schrebergaerten.eingabe):
                            if platzverlust == 0:
                                # perfekte Lösung wird zurückgegeben
                                return neue_anordnung
                            # Lösung ist nicht perfekt, aber die platzsparendste bisher
                            elif platzverlust < Schrebergaerten.kleinster_platzverlust or Schrebergaerten.kleinster_platzverlust == -1:
                                # Beste anordnung und kleinster Platzverlust bisher werden gespeichert
                                Schrebergaerten.beste_anordnung.clear()
                                Schrebergaerten.beste_anordnung.extend(neue_anordnung)
                                Schrebergaerten.kleinster_platzverlust = platzverlust

                        # Falls Anordnung noch nicht komplett
                        else:
                            used = []
                            used.extend(benutzte_rechtecke)
                            used.append(rechteck_index)
                            x = Schrebergaerten.finde_anordnung(neue_anordnung, used)
                            # Wenn es für die nächste Anordnung eine perfekte Lösung gibt...
                            if not x == [-1]:
                                # ... wird diese zurückgegeben
                                return x
        # Es konnte keine perfekte Lösung gefunden werden
        return [-1]

    @staticmethod
    def get_eckpunkte(anordnung):
        # Falls noch keine Anordnung...
        if len(anordnung) == 0:
            # ...fungiert der Ursprung als Eckpunkt
            return [Koordinate(0, 0)]

        # Zunächst werden alle Eckpunkt-Koordinaten in einer Liste gespeichert
        eckpunkte_aller_rechtecke = []
        for rechteck in anordnung:
            eckpunkte_aller_rechtecke.append(Koordinate(rechteck.ox, rechteck.oy))
            eckpunkte_aller_rechtecke.append(Koordinate(rechteck.ox + rechteck.x, rechteck.oy + rechteck.y))
            eckpunkte_aller_rechtecke.append(Koordinate(rechteck.ox + rechteck.x, rechteck.oy))
            eckpunkte_aller_rechtecke.append(Koordinate(rechteck.ox, rechteck.oy + rechteck.y))

        # und in ein Feldersystem umgewandelt, das einer Tabelle gleichkommt
        # Die Felder in denen Rechtecke vorhanden werden auf True gesetzt
        feldersystem = Schrebergaerten.anordnung_in_felder(anordnung)
        eckpunkte_der_anordnung = []
        for eckpunkt in eckpunkte_aller_rechtecke:
            # Ursprung diente bereits als Eckpunkt, deswegen übersprungen
            if eckpunkt.x == 0 and eckpunkt.y == 0:
                continue

            # Schauen ob es sich am Rand um einen Eckpunkt handelt
            if eckpunkt.x == 0:
                if not feldersystem[0][eckpunkt.y] or not feldersystem[0][eckpunkt.y - 1]:
                    eckpunkte_der_anordnung.append(eckpunkt)
                continue

            if eckpunkt.y == 0:
                if not feldersystem[eckpunkt.x][0] or not feldersystem[eckpunkt.x - 1][0]:
                    eckpunkte_der_anordnung.append(eckpunkt)
                continue

            # Prüfen, ob im Umfeld von einem Kästchen ein Feld False ist. Falls ja --> Eckpunkt, da am Rand
            if not feldersystem[eckpunkt.x][eckpunkt.y] or not feldersystem[eckpunkt.x - 1][eckpunkt.y] or not \
                    feldersystem[eckpunkt.x][eckpunkt.y - 1] or not feldersystem[eckpunkt.x - 1][eckpunkt.y - 1]:
                eckpunkte_der_anordnung.append(eckpunkt)
                continue

        return eckpunkte_der_anordnung

    @staticmethod
    # Erhalte Breite und Höhe für das gesamte Vieleck der aktuellen Anordnung
    def get_grenze(anordnung):
        breite = 0
        hoehe = 0
        for rechteck in anordnung:
            # Es wird der Wert für die Breite zurückgegeben, der am weitesten rechts liegt
            if rechteck.ox > breite:
                breite = rechteck.ox
            if rechteck.x + rechteck.ox > breite:
                breite = rechteck.x + rechteck.ox
            # Es wird der Wert für die Höhe zurückgegeben, der am weitesten oben liegt
            if rechteck.y + rechteck.oy > hoehe:
                hoehe = rechteck.y + rechteck.oy
            if rechteck.oy > hoehe:
                hoehe = rechteck.oy
        return [breite, hoehe]

    @staticmethod
    def alle_ausrichtungen(rechteck):
        # Jede mögliche Ausrichtung durch jeweils Tauschen eines oder beider Vorzeichen
        return [Koordinate(rechteck.x, rechteck.y), Koordinate(-rechteck.x, rechteck.y),
                Koordinate(rechteck.x, -rechteck.y), Koordinate(-rechteck.x, -rechteck.y)]

    @staticmethod
    # Prüfen, ob Rechteck valide gesetzt werden kann, ohne Überschneidung
    def ueberschneidung_vorhanden(anordnung, rechteck):
        # Erstmal wird überprüft, ob das zu setzende Rechteck das Koordinatensystem nicht überschneidet
        if rechteck.x + rechteck.ox < 0 or rechteck.y + rechteck.oy < 0:
            return True

        feldersystem_anordnung = Schrebergaerten.anordnung_in_felder(anordnung)
        feldersystem_rechteck = Schrebergaerten.anordnung_in_felder([rechteck])

        if len(feldersystem_rechteck) >= len(feldersystem_anordnung):
            x_range = len(feldersystem_rechteck)
        else:
            x_range = len(feldersystem_anordnung)

        if len(feldersystem_rechteck[0]) >= len(feldersystem_anordnung[0]):
            y_range = len(feldersystem_rechteck[0])
        else:
            y_range = len(feldersystem_anordnung[0])

        # Feldersystem, in das beide einzelenen Feldersysteme reinpassen
        feldersystem_kombi = []
        for x_koordinate in range(x_range):
            feldersystem_kombi.append([])
            for y_koordinate in range(y_range):
                feldersystem_kombi[x_koordinate].append(False)

        # Im großen Feldersystem werden die Felder in denen sich das Rechteck befindet auf True gesetzt
        for x in range(len(feldersystem_rechteck)):
            for y in range(len(feldersystem_rechteck[0])):
                if feldersystem_rechteck[x][y]:
                    feldersystem_kombi[x][y] = True

        # Es wird Feld für Feld im Feldersystem der Anordnung durchgegangen
        for x in range(len(feldersystem_anordnung)):
            for y in range(len(feldersystem_anordnung[0])):
                # Überschneidung des Rechtecks mit der Anordnung
                if feldersystem_anordnung[x][y] and feldersystem_kombi[x][y]:
                    return True

        return False

    @staticmethod
    def anordnung_in_felder(anordnung):
        grenzen = Schrebergaerten.get_grenze(anordnung)
        breite = grenzen[0]
        hoehe = grenzen[1]
        feldersystem = []

        # Tabelle/Feldersystem wird erstellt, das ein Kästchen weiter in die Breite und Höhe geht
        for x_koordinate in range(breite + 1):
            feldersystem.append([])
            for y_koordinate in range(hoehe + 1):
                # Alle Felder des Koordinatensystems werden erstmal auf False gesetzt
                feldersystem[x_koordinate].append(False)

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
                    feldersystem[x][y] = True

        return feldersystem

    @staticmethod
    def getPlatzverlust(anordnung):
        # Platzverlust = Fläche der Anordnung - Fläche aller Rechtecke
        belegte_flaeche = 0
        for rechteck in anordnung:
            belegte_flaeche += abs(rechteck.x * rechteck.y)
        dimensionen = Schrebergaerten.get_grenze(anordnung)
        return dimensionen[0] * dimensionen[1] - belegte_flaeche

    @staticmethod
    # Fläche der übrigbleibenden Rechtecke
    def getUebrigeFlaeche(benutzte_rechtecke):
        flaeche = 0
        for rechteck_index in benutzte_rechtecke:
            flaeche += Schrebergaerten.eingabe[rechteck_index].x * Schrebergaerten.eingabe[rechteck_index].y

        return flaeche


# Klasse für die grafische Ausgabe
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
        painter.setBrush(QBrush(QColor(39, 174, 96), Qt.SolidPattern))

        x_max = 0
        y_max = 0

        for rechteck in Interface.anordnung:
            if rechteck.ox + rechteck.x > x_max:
                x_max = rechteck.ox + rechteck.x
            if rechteck.oy + rechteck.y > y_max:
                y_max = rechteck.oy + rechteck.y

        if x_max > y_max:
            scale = 200 / x_max
        else:
            scale = 200 / y_max

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

print("\n Anordnung wird berechnet... (Dauert bei 5 Schrebergärten ca. 60 Sekunden)")
loesung = Schrebergaerten.finde_anordnung([], [])
app = QApplication(sys.argv)
if loesung != [-1]:
    Interface.anordnung = loesung

else:
    Interface.anordnung = Schrebergaerten.beste_anordnung

print("\n Anordnung gefunden! Interface womöglich im Hintergrund")
print("--> Platzverlust: " + str(Schrebergaerten.getPlatzverlust(Interface.anordnung)))
print("--> Breite: " + str(Schrebergaerten.get_grenze(Interface.anordnung)[0]))
print("--> Höhe: " + str(Schrebergaerten.get_grenze(Interface.anordnung)[1]))
ex = Interface()
sys.exit(app.exec_())

