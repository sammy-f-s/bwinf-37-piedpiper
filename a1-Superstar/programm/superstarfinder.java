
import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
//Für die Dateiauswahl
import java.io.IOException;
import java.nio.charset.StandardCharsets;
//Für das Einlesen der Datei in der  ISO_8859_1 Kodierung
import java.nio.file.Files;
//Für das Einlesen der Datei
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class superstarfinder {
    private static int inquiriesAmount = 0;

    //Um zu speichern, wie viele Anfragen benötigt worden sind
    public static void main(String args[]) throws IOException {

        System.out.println("Der Superstar ist: " + findsuperstar() + "\n " + inquiriesAmount + " Anfragen");
        //Ausgabe des Superstars und der verwendeten Anfragen

    }

    private static String findsuperstar() throws IOException {

        boolean doesntFollow, getsFollowed;
        //Bedingung für Superstar: er folgt nicht, wird aber von allen gefolgt
        String filepath = chooseFile();
        //Pfad der Datei wird gesetzt
        StringBuilder allNames[] = splitFile(filepath);
        List<String> allData = Files.readAllLines(Paths.get(filepath), StandardCharsets.ISO_8859_1);
        //Die erste Zeile der Datei wird in ein Array umgewandelt, sodass nacheinander jeder Name anschließend ausprobiert wird
        //Dieser String speichert später den Superstar
        List<String> nonRelevantMembers = new ArrayList<>();
        //Diese Liste speichert alle Mitglieder, die vom Verfahren ausgeschlossen wurden, da sie schon die Bedingung nicht erfüllen,
        // dass sie keiner Person folgen

        for (int i = 0; allNames.length - 1 >= i; i++) {
            if (nonRelevantMembers.contains(allNames[i].toString())) continue;
            doesntFollow = true;
            getsFollowed = true;

            for (int j = 0; allNames.length - 1 >= j; j++) {
                //Das gleiche wie vorher, nur mit der nächsten Bedingung
                if (!anfrage(allNames[j].toString(), allNames[i].toString(), allData) && allNames[j] != allNames[i]) {
                    //Falls eine Person nicht dem nun potentiellen Superstar folgt, wird abgebrochen
                    // Die zweite Bedingung ist da um auszuschließen dass abgebrochen wird, wenn die Person nicht sich selber folgt
                    getsFollowed = false;
                    break;
                } else if (!nonRelevantMembers.contains(allNames[j].toString())) {
                    nonRelevantMembers.add(allNames[j].toString());
                }
            }

            if (getsFollowed) {
                for (int j = 0; allNames.length - 1 >= j; j++) {
                    if (anfrage(allNames[i].toString(), allNames[j].toString(), allData)) {
                        //Falls die Person irgendjemandem folgt, wird direkt abgebrochen und die nächste Person ausprobiert
                        doesntFollow = false;
                        break;
                    }
                }
            } else continue;

            if (getsFollowed && doesntFollow) {
                //Falls die beiden Bedingungen nicht vorher von den zwei anderen for-Schleifen auf false gesetzt worden sind,
                // wird die Person als Superstar gesetzt und die Suche abgebrochen
                return allNames[i].toString();
            }
        }
        return "Niemand";
    }

    private static StringBuilder[] splitFile(String filepath) throws IOException {
        //String in Array aufteilen -> jeder Name hat eine Zeile
        List<String> lines = Files.readAllLines(Paths.get(filepath), StandardCharsets.ISO_8859_1);
        int spaceAmount = 0;
        int arrayLocation = 0;
        String names = lines.get(0);

        for (int i = 0; names.length() - 1 >= i; i++) { //Anzahl an Leerzeichen rausfinden ->
            // Wortanzahl und somit wie viele Leute es insgesamt gibt -> dies wird für die Arraygröße benötigt
            if (names.charAt(i) == ' ') spaceAmount++;
        }
        StringBuilder[] allNames = new StringBuilder[spaceAmount + 1];
        for (int i = 0; names.length() - 1 >= i; i++) {
            //Alle Namen werden eine eigene Zeile gebracht
            if (allNames[arrayLocation] == null)
                allNames[arrayLocation] = new StringBuilder();
            //Die Stelle muss erstmal als StringBuilder Objekt initialisiert werden
            if (names.charAt(i) == ' ') {
                //Wenn erkannt wird, dass ein Leerzeichen vorhanden ist, wird in die nächste Stelle des Arrays gegangen
                arrayLocation++;
            } else {
                allNames[arrayLocation].append(names.charAt(i));
                //Sonst wird der aktuelle Buchstabe der aktuellen Stelle im Array angehängt
            }
        }
        return allNames;
    }

    private static boolean anfrage(String name1, String name2, List<String> allData) { //Anfrage: ob X, Y folgt
        inquiriesAmount++;
        for (int i = 2; allData.size() - 1 >= i; i++) {
            //Durch alle Zeilen durchgehen und schauen ob X und Y, in dieser Reihenfolge, mit Leerzeichen dazwischen,
            // in einer Zeile stehen
            if ((allData.get(i)).contains(name1 + " " + name2)) {
                return true;
            }
        }
        return false;

    }

    private static String chooseFile() {
        JFileChooser chooser = new JFileChooser();
        FileNameExtensionFilter filter = new FileNameExtensionFilter("Textdateien", "txt");
        //Nur .txt Dateien werden anezeigt
        chooser.setFileFilter(filter);
        int chosen = chooser.showOpenDialog(null);

        if (chosen == JFileChooser.APPROVE_OPTION) {
            //Wenn Ok gedrückt wird, wird der Pfad der Datei zurückgegeben
            return chooser.getSelectedFile().getPath();
        } else System.exit(0);
        //Sonst wird beendet
        return null;
    }
}
