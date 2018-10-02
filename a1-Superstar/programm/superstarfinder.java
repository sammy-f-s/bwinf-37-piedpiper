
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
    //Um zu speichern, wie viele Anfragen benötigt wurden

    public static void main(String args[]) throws IOException {
            System.out.print("Der Superstar ist: " + findsuperstar() + "\n" + inquiriesAmount + " Anfragen");
    }

    private static String findsuperstar() throws IOException {

        boolean doesntFollow, getsFollowed;
        //Bedingung für Superstar: er folgt nicht, wird aber von allen gefolgt
        String filepath = chooseFile();
        //Pfad der Datei wird gesetzt
        List<String> allNames = (splitFile(filepath));
        //Die erste Zeile der Datei, die alle Mitglieder auflistet, wird in ein Array aufgeteilt,
        //sodass jedes Mitglied seine eigene Zeile bekommt
        List<String> allData = Files.readAllLines(Paths.get(filepath), StandardCharsets.ISO_8859_1);
        allData.remove(0);
        //Die erste Zeile der Datei wird in ein Array umgewandelt
        List<String> nonRelevantMembers = new ArrayList<>();
        //Diese Liste speichert alle Mitglieder, die vom Verfahren ausgeschlossen wurden, da sie schon die Bedingung nicht erfüllen,
        // dass sie keiner Person folgen
        List<String> allNamesSorted = new ArrayList<>(allNames);
        String nameBuffer;

        for (int i = 0; allNames.size() - 1 >= i; i++) {

            if (searchInListFor(nonRelevantMembers,allNames.get(i))){
                continue;
            }

            doesntFollow = true;
            getsFollowed = true;

            for (int j = 0; allNames.size() - 1 >= j; j++) {
                //Das gleiche wie vorher, nur mit der nächsten Bedingung
                if (!allNamesSorted.get(j).contains(allNames.get(i)) && !anfrage(allNamesSorted.get(j), allNames.get(i), allData)) {
                    //Falls eine Person nicht dem nun potentiellen Superstar folgt, wird abgebrochen
                    // Die zweite Bedingung ist da um auszuschließen dass abgebrochen wird, wenn die Person nicht sich selber folgt
                    getsFollowed = false;
                    break;
                }
                if (!allNamesSorted.get(j).contains(allNames.get(i)) && !searchInListFor(nonRelevantMembers, allNamesSorted.get(j))){
                    nonRelevantMembers.add(allNamesSorted.get(j));
                    //Name zur Liste der nicht relevanten Mitglieder hinzufügen
                    nameBuffer = allNamesSorted.get(j);
                    allNamesSorted.remove(j);
                    allNamesSorted.add(nameBuffer);
                    //Ans Ende der Liste setzten

                }
            }

            if (getsFollowed) {
                //Falls die Bedingung 2 (getsFollowed) nicht vorher von der vorherigen for-schleife auf false gesetzt worden ist,
                //wird die Überprüfung fortgesetzt
                for (int j = 0; allNames.size() - 1 >= j; j++) {
                    if (!allNamesSorted.get(j).contains(allNames.get(i)) && anfrage(allNames.get(i), allNamesSorted.get(j), allData)) {
                        //Falls die Person irgendjemandem folgt, wird direkt abgebrochen und die nächste Person ausprobiert
                        doesntFollow = false;
                        break;
                    }
                }
            } else continue;

            if (doesntFollow) {
                //Falls die Bedingungen 1 (doesntFollow) nicht vorher von der vorherigen for-Schleife auf false gesetzt worden ist,
                // wird der von der ersten for-schleife ausgewählte potenzielle Superstar zurückgegeben, da dieses Mitglied der Superstar
                //sein muss
                return allNames.get(i);
            }
        }
        return "Niemand";
    }

    private static List<String> splitFile(String filepath) throws IOException {
        //String in Array aufteilen -> jeder Name hat eine Zeile
        List<String> lines = Files.readAllLines(Paths.get(filepath), StandardCharsets.ISO_8859_1);
        int listLocation = 0;
        String names = lines.get(0);

        List<StringBuilder> allNames = new ArrayList<>();
        allNames.add(new StringBuilder());
        for (int i = 0; names.length() - 1 >= i; i++) {
            if (names.charAt(i) == ' ') {
                //Bei Leerzeichen in nächste Zeile
                listLocation++;
                allNames.add(new StringBuilder());
            } else {
                allNames.set(listLocation, allNames.get(listLocation).append(names.charAt(i)));
                //Sonst wird der aktuelle Buchstabe der aktuellen Stelle angehängt
            }
        }
        return toStringList(allNames);
    }

    private static boolean anfrage(String name1, String name2, List<String> allData) { //Anfrage: ob X, Y folgt
        inquiriesAmount++;
        //Anfragenzähler
        for (int i = 0; allData.size() - 1 >= i; i++) {
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

    private static boolean searchInListFor(List<String> listToSearch, String searchFor){
        for(int i = 0; listToSearch.size()-1 >= i;i++){
            if((listToSearch.get(i)).contains(searchFor)){
                return true;
            }
        }
        return false;

    }

    private static List<String> toStringList(List<StringBuilder> listToConvert){
        List<String> list = new ArrayList<>();
        for (int i = 0; listToConvert.size()-1 >= i; i++) {
            list.add(listToConvert.get(i).toString());
        }
        return list;
    }
}

