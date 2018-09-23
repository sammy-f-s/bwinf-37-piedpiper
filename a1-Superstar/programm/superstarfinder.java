import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class superstarfinder {
    public static void main(String args[]) throws IOException {
        int inquiryAmount = 0; //um die herauszufinden, wie viele Anfragen benötigt worden sind
        boolean doesntFollow, getsFollowed; //Bedingung für Superstar: er folgt nicht, wird aber von allen gefolgt
        String filepath = chooseFile();
        StringBuilder allNames[] = splitFile(filepath);
        String superstars[] = new String[allNames.length - 1];
        int arrayLocation = 0;
        for (int i = 0; allNames.length - 1 >= i; i++) {
            doesntFollow = true;
            getsFollowed = true;
            for (int j = 0; allNames.length - 1 >= j; j++) {

                if (anfrage(allNames[i].toString(), allNames[j].toString(), filepath)) { //Falls die Person irgendjemandem folgt, wird direkt abgebrochen und die nächste Person ausprobiert
                    doesntFollow = false;
                    break;
                }

                inquiryAmount++;
            }

            if (doesntFollow) {
                for (int j = 0; allNames.length - 1 >= j; j++) { //Das gleiche wie vorher, nur mit der nächsten Bedingung
                    if (!anfrage(allNames[j].toString(), allNames[i].toString(), filepath) && allNames[j] != allNames[i]) {
                        getsFollowed = false;
                        break;
                    }
                    inquiryAmount++;
                }
            }

            if (getsFollowed && doesntFollow) { //Falls beide Bedingungen zutreffen wird die Person der Liste hinzugefügt
                superstars[arrayLocation] = allNames[i].toString();
                arrayLocation++;
            }
        }

        for (int i = 0; arrayLocation - 1 >= i; i++) {
            System.out.println(superstars[i] + " ist ein Superstar");
        }
        System.out.println(inquiryAmount + " Anfragen");

    }

    private static StringBuilder[] splitFile(String filepath) throws IOException {  //String in Array aufteilen -> jeder Name hat eine Zeile
        List<String> lines;
        lines = Files.readAllLines(Paths.get(filepath), StandardCharsets.ISO_8859_1);
        //System.out.println(lines);
        int spaceAmount = 0;
        int arrayLocation = 0;
        String names = lines.get(0);

        for (int i = 0; names.length() - 1 >= i; i++) { //Anzahl an Leerzeichen rausfinden -> Wortanzahl und somit wie viele Leute es insgesamt gibt -> Arraygröße
            if (names.charAt(i) == ' ') spaceAmount++;
        }
        StringBuilder[] allNames = new StringBuilder[spaceAmount + 1];
        for (int i = 0; names.length() - 1 >= i; i++) {
            if (allNames[arrayLocation] == null) allNames[arrayLocation] = new StringBuilder();
            if (names.charAt(i) == ' ') {
                arrayLocation++;
            } else {
                allNames[arrayLocation].append(names.charAt(i));
            }

        }
        return allNames;

    }

    private static boolean anfrage(String name1, String name2, String filepath) throws IOException { //Anfrage: ob X, Y folgt
        List<String> lines;
        lines = Files.readAllLines(Paths.get(filepath), StandardCharsets.ISO_8859_1); //Einlesen der Datei
        for (int i = 1; lines.size() - 1 >= i; i++) {  //Durch alle Zeilen durchgehen und schauen ob der
            if ((lines.get(i)).contains(name1 + " " + name2)) {
                return true;
            }
        }
        return false;

    }

    private static String chooseFile() {
        JFileChooser chooser = new JFileChooser();
        FileNameExtensionFilter filter = new FileNameExtensionFilter("Textdateien", "txt");
        chooser.setFileFilter(filter);
        int chosen = chooser.showOpenDialog(null);

        if (chosen == JFileChooser.APPROVE_OPTION) {
            return chooser.getSelectedFile().getPath();
        } else System.exit(0);
        return null;
    }
}
