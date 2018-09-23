import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class superstarfinder {
    public static void main(String args[]) throws IOException {
        int inquiriesAmount = 0; //um die herauszufinden, wie viele Anfragen benötigt worden sind
        boolean doesntFollow, getsFollowed; //Bedingung für Superstar: er folgt nicht, wird aber von allen gefolgt
        String filepath = chooseFile(); //Pfad der Datei wird gesetzt
        StringBuilder allNames[] = splitFile(filepath); //Die erste Zeile der Datei wird in ein Array umgewandelt, sodass nacheinander jeder Name anschließend ausprobiert wird
        String superstars[] = new String[allNames.length - 1]; //Dieses Array wird alle Superstars speichern
        int arrayLocation = 0;
        for (int i = 0; allNames.length - 1 >= i; i++) {
            doesntFollow = true;
            getsFollowed = true;
            for (int j = 0; allNames.length - 1 >= j; j++) {

                if (anfrage(allNames[i].toString(), allNames[j].toString(), filepath)) { //Falls die Person irgendjemandem folgt, wird direkt abgebrochen und die nächste Person ausprobiert
                    doesntFollow = false;
                    break;
                }

                inquiriesAmount++; //Da eine Anfrage gestellt worden ist, wird der Zähler um einen hoch gesetzt um am Ende zu sehen, wie viele Anfragen gestellt worden ist
            }

            if (doesntFollow) {
                for (int j = 0; allNames.length - 1 >= j; j++) { //Das gleiche wie vorher, nur mit der nächsten Bedingung
                    if (!anfrage(allNames[j].toString(), allNames[i].toString(), filepath) && allNames[j] != allNames[i]) { //Falls eine Person nicht dem nun potentiellen Superstar folgt, wird abgebrochen. Die zweite Bedingung ist da um auszuschließen dass abgebrochen wird, wenn die Person nicht sich selber folgt
                        getsFollowed = false;
                        break;
                    }
                    inquiriesAmount++;
                }
            }

            if (getsFollowed && doesntFollow) { //Falls die beiden Bedingungen nicht vorher von den zwei anderen for-Schleifen auf false gesetzt worden sind, wird die Person zur Liste der Superstars hinzugefügt
                superstars[arrayLocation] = allNames[i].toString();
                arrayLocation++;
            }
        }

        for (int i = 0; arrayLocation - 1 >= i; i++) {
            System.out.println(superstars[i] + " ist ein Superstar"); //Ausgabe der Superstars
        }
        System.out.println(inquiriesAmount + " Anfragen"); //Ausgabe der verwendeten Anfragen

    }

    private static StringBuilder[] splitFile(String filepath) throws IOException {  //String in Array aufteilen -> jeder Name hat eine Zeile
        List<String> lines;
        lines = Files.readAllLines(Paths.get(filepath), StandardCharsets.ISO_8859_1);
        //System.out.println(lines);
        int spaceAmount = 0;
        int arrayLocation = 0;
        String names = lines.get(0);

        for (int i = 0; names.length() - 1 >= i; i++) { //Anzahl an Leerzeichen rausfinden -> Wortanzahl und somit wie viele Leute es insgesamt gibt -> dies wird für die Arraygröße benötigt
            if (names.charAt(i) == ' ') spaceAmount++;
        }
        StringBuilder[] allNames = new StringBuilder[spaceAmount + 1];
        for (int i = 0; names.length() - 1 >= i; i++) { //Alle Namen werden eine eigene Zeile gebracht
            if (allNames[arrayLocation] == null) allNames[arrayLocation] = new StringBuilder(); //Die Stelle muss erstmal als StringBuilder Objekt initialisiert werden
            if (names.charAt(i) == ' ') { //Wenn erkannt wird, dass ein Leerzeichen vorhanden ist, wird in die nächste Stelle des Arrays gegangen
                arrayLocation++;
            } else {
                allNames[arrayLocation].append(names.charAt(i)); //Sonst wird der aktuelle Buchstabe der aktuellen Stelle im Array angehängt
            }

        }
        return allNames;

    }

    private static boolean anfrage(String name1, String name2, String filepath) throws IOException { //Anfrage: ob X, Y folgt
        List<String> lines;
        lines = Files.readAllLines(Paths.get(filepath), StandardCharsets.ISO_8859_1); //Einlesen der Datei
        for (int i = 1; lines.size() - 1 >= i; i++) {  //Durch alle Zeilen durchgehen und schauen ob X und Y, in dieser Reihenfolge, stehen
            if ((lines.get(i)).contains(name1 + " " + name2)) {
                return true;
            }
        }
        return false;

    }

    private static String chooseFile() {
        JFileChooser chooser = new JFileChooser();
        FileNameExtensionFilter filter = new FileNameExtensionFilter("Textdateien", "txt"); //Nur .txt Dateien werden anezeigt
        chooser.setFileFilter(filter);
        int chosen = chooser.showOpenDialog(null);

        if (chosen == JFileChooser.APPROVE_OPTION) { //Wenn Ok gedrückt wird, wird der Pfad der Datei zurückgegeben
            return chooser.getSelectedFile().getPath();
        } else System.exit(0); //Sonst wird beendet
        return null;
    }
}
