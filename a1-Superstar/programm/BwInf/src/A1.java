

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
        int anfragenAmount = 0;
        boolean doesntFollow = false;
        boolean getsFollowed = false;
        StringBuilder namen[] = splitFile();
        String superstars[] = new String[namen.length-1];
        int ArrayStelle = 0;
        for(int i = 0; namen.length-1 >= i;i++) {
            doesntFollow = true;
            getsFollowed = true;
            for (int j = 0; namen.length - 1 >= j; j++) {

                if (anfrage(namen[i].toString(), namen[j].toString()) == true) {
                    doesntFollow = false;
                    break;
                }

                anfragenAmount++;
            }

            if(doesntFollow == true) {
                for (int j = 0; namen.length - 1 >= j; j++) {
                    if (!anfrage(namen[j].toString(), namen[i].toString()) && namen[j] != namen[i]) {
                        getsFollowed = false;
                        break;
                    }
                    anfragenAmount++;
                }
            }

        if(getsFollowed == true && doesntFollow == true){
            superstars[ArrayStelle] = namen[i].toString();
            ArrayStelle++;
        }
        }

        for(int i = 0; ArrayStelle-1 >= i; i++){
            System.out.println(superstars[i]+ " ist ein Superstar");
        }
        System.out.println(anfragenAmount+" Anfragen");

    }

    public static String getConsole() throws IOException{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        return br.readLine();
    }

    public static StringBuilder[] splitFile()throws IOException{
        List<String> lines = Collections.emptyList();
        lines = Files.readAllLines(Paths.get("C:\\Users\\David\\IdeaProjects\\bwinf-sammy-david\\a1-Superstar\\programm\\BwInf\\src\\part.txt"), StandardCharsets.UTF_16);
        System.out.println(lines);
        int spaceAmount = 0;
        int ArrayStelle = 0;
        String names = lines.get(0);

        for (int i = 0; names.length()-1 >= i;i++) { //Anzahl an Leerzeichen rausfinden -> Wortanzahl und somit wie viele Leute es insgesamt gibt
            if (names.charAt(i) == ' ') spaceAmount++;
        }
        StringBuilder[] allNames = new StringBuilder[spaceAmount + 1];
        for(int i = 0; names.length()-1 >= i; i++){ //String in Array aufteilen -> jeder Name hat eine Zeile
            if (allNames[ArrayStelle] == null) allNames[ArrayStelle] =  new StringBuilder("");
            if(names.charAt(i) == ' ') {
                ArrayStelle++;
            }
            else{
                allNames[ArrayStelle].append(names.charAt(i));
            }

        }
        return allNames;

    }

    public static boolean anfrage(String name1, String name2)throws IOException{
        List<String> lines = Collections.emptyList();
        lines = Files.readAllLines(Paths.get("C:\\Users\\David\\IdeaProjects\\bwinf-sammy-david\\a1-Superstar\\programm\\BwInf\\src\\part.txt"), StandardCharsets.UTF_16);
        for(int i = 1;lines.size()-1 >= i;i++){
            if((lines.get(i)).contains(name1 + " " + name2)){
                return true;
            }
        }
        return false;

    }

}
