

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.List;

public class A1 {
    public static void main (String args[]) throws IOException{
        readFile();
    }

    public static String getConsole() throws IOException{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        return br.readLine();
    }

    public static void readFile()throws IOException{
        List<String> lines = Collections.emptyList();
        lines = Files.readAllLines(Paths.get("C:\\Users\\David\\IdeaProjects\\BwInf\\src\\part.txt"), StandardCharsets.UTF_8);
        System.out.println(lines);
        int spaceAmount = 0;
        String names = lines.get(0);

        int ArrayStelle = 0;
        int nameEndbefore = 0;

        for (int i = 0; names.length()-1 >= i;i++) { //Anzahl an Leerzeichen rausfinden -> Wortanzahl und somit wie viele Leute es insgesamt gibt
            if (names.charAt(i) == ' ') spaceAmount++;
        }
        StringBuilder[] allNames = new StringBuilder[spaceAmount + 1];
        for(int i = 0; names.length()-1 >= i; i++){ //String in Array aufteilen
            if (allNames[ArrayStelle] == null) allNames[ArrayStelle] =  new StringBuilder("");
            if(names.charAt(i) == ' ') {
                ArrayStelle++;
            }
            else{
                allNames[ArrayStelle].append(names.charAt(i));
            }

        }
        System.out.println(allNames[0].toString() + allNames[1].toString() + allNames[2].toString());

    }

}
