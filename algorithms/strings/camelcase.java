//https://www.hackerrank.com/challenges/camelcase

import java.util.Scanner;

public class camelcase {
    public static int camelCase(String s){
        int num = 0;

        char[] letters = s.toCharArray();
        for(char letter:letters){
            if (letter >= 65 && letter < 97){
                num += 1;
            }
        }

        return num+1;
    }

    public static void main(String[] args) {
        String s = null;
        //s = "iAmACamelCaseWord";

        Scanner scanner = new Scanner(System.in);
        s = scanner.nextLine();
        System.out.println(camelCase(s));
        scanner.close();
    }
}
