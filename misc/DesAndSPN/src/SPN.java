import java.util.Scanner;
import java.util.HashMap;
import java.lang.StringBuilder;

public class SPN {
    public static void main(String[] args) {
   	 // create key
   	 int[] K = { 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1 };
   	 Scanner rdr = new Scanner(System.in);
   	 // String plaintext = rdr.next();
   	 // int rounds = rdr.nextInt();

   	 // int[] K = { 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1,
   	 // 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1 };

   	 String plaintext = "26B7";
   	 int rounds = 4;
   	 HashMap<Character, int[]> hexMap = new HashMap<Character, int[]>();
   	 hexMap = initHexMap(hexMap);
   	 HashMap<Character, Character> sBoxMap = initSBoxMap();
   	 int[] first = hexMap.get(plaintext.charAt(0));
   	 int[] second = hexMap.get(plaintext.charAt(1));
   	 int[] third = hexMap.get(plaintext.charAt(2));
   	 int[] fourth = hexMap.get(plaintext.charAt(3));
   	 int[] pText = concatenate(first, second, third, fourth);
   	 int[] curr = pText;
   	 // run through all the rounds, except the last
   	 for (int i = 0; i < rounds - 1; i++) {// changed
   		 int[] tempSubKey = subkey(i, K);
   		 curr = xor(curr, tempSubKey);
   		 curr = sbox(curr, sBoxMap, hexMap);
   		 curr = permutation(curr);
   	 } // final round
   	 int[] finalRoundKey = subkey(rounds - 1, K);// changed
   	 curr = xor(curr, finalRoundKey);
   	 curr = sbox(curr, sBoxMap, hexMap);
   	 int[] whitening = subkey(rounds, K);// changed
   	 curr = xor(curr, whitening);
   	 // transfer back to hex
   	 // changed
   	 StringBuilder ciphertext = new StringBuilder();
   	 for (int i = 0; i < 13; i += 4) {
   		 int[] temp = { curr[i], curr[i + 1], curr[i + 2], curr[i + 3] };
   		 ciphertext.append(bin2Hex(temp));
   	 }
   	 // print the ciphertext out
   	 System.out.println(ciphertext);
   	 rdr.close();
    }

    // convert hex to binary
    private static HashMap<Character, int[]> initHexMap(HashMap<Character, int[]> hexMap) {
   	 hexMap.put('0', new int[] { 0, 0, 0, 0 });
   	 hexMap.put('1', new int[] { 0, 0, 0, 1 });
   	 hexMap.put('2', new int[] { 0, 0, 1, 0 });
   	 hexMap.put('3', new int[] { 0, 0, 1, 1 });
   	 hexMap.put('4', new int[] { 0, 1, 0, 0 });
   	 hexMap.put('5', new int[] { 0, 1, 0, 1 });
   	 hexMap.put('6', new int[] { 0, 1, 1, 0 });
   	 hexMap.put('7', new int[] { 0, 1, 1, 1 });
   	 hexMap.put('8', new int[] { 1, 0, 0, 0 });
   	 hexMap.put('9', new int[] { 1, 0, 0, 1 });
   	 hexMap.put('A', new int[] { 1, 0, 1, 0 });
   	 hexMap.put('B', new int[] { 1, 0, 1, 1 });
   	 hexMap.put('C', new int[] { 1, 1, 0, 0 });
   	 hexMap.put('D', new int[] { 1, 1, 0, 1 });
   	 hexMap.put('E', new int[] { 1, 1, 1, 0 });
   	 hexMap.put('F', new int[] { 1, 1, 1, 1 });
   	 return hexMap;
    }

    // converty binary to hexadecimal
    private static char bin2Hex(int bin[]) {
   	 // initialize
   	 int val = 0;
   	 char hex = 'g';
   	 // get decimal representationfor bin
   	 for (int i = 0; i < 4; i++) {
   		 val += Math.pow(2, i) * bin[3 - i];
   	 }
   	 // convert to char
   	 switch (val) {
   	 case 10:
   		 hex = 'A';
   		 break;
   	 case 11:
   		 hex = 'B';
   		 break;
   	 case 12:
   		 hex = 'C';
   		 break;
   	 case 13:
   		 hex = 'D';
   		 break;
   	 case 14:
   		 hex = 'E';
   		 break;
   	 case 15:
   		 hex = 'F';
   		 break;
   	 default:
   		 hex = Integer.toString(val).charAt(0);
   	 }
   	 return hex;
    }

    // grab subkeys method
    private static int[] subkey(int subNum, int[] k) {
   	 int[] ans = new int[16];
   	 int count = 0;

   	 for (int i = subNum * 4; i < (subNum * 4) + 16; i++) {
   		 ans[count] = k[i];
   		 count++;
   	 }
   	 return ans;
    }

    // concatenate 4 integer arrays into 1
    private static int[] concatenate(int[] first, int[] second, int[] third, int[] fourth) {
   	 int[] ans = new int[first.length + second.length + third.length + fourth.length];
   	 int count = 0;
   	 for (int i = 0; i < first.length; i++) {
   		 ans[count] = first[i];
   		 count++;
   	 }
   	 for (int i = 0; i < second.length; i++) {
   		 ans[count] = second[i];
   		 count++;
   	 }
   	 for (int i = 0; i < third.length; i++) {
   		 ans[count] = third[i];
   		 count++;
   	 }
   	 for (int i = 0; i < fourth.length; i++) {
   		 ans[count] = fourth[i];
   		 count++;
   	 }
   	 return ans;
    }

    // xor a value with a key
    private static int[] xor(int[] key, int[] input) {
   	 int[] ans = new int[16];
   	 for (int i = 0; i < 16; i++) {
   		 ans[i] = (key[i] + input[i]) % 2;
   	 }
   	 return ans;
    }

    // creates sbox mapping
    private static HashMap<Character, Character> initSBoxMap() {
   	 HashMap<Character, Character> sBoxMap = new HashMap<Character, Character>();
   	 sBoxMap.put('0', 'E');
   	 sBoxMap.put('1', '4');
   	 sBoxMap.put('2', 'D');
   	 sBoxMap.put('3', '1');
   	 sBoxMap.put('4', '2');
   	 sBoxMap.put('5', 'F');
   	 sBoxMap.put('6', 'B');
   	 sBoxMap.put('7', '8');
   	 sBoxMap.put('8', '3');
   	 sBoxMap.put('9', 'A');
   	 sBoxMap.put('A', '6');
   	 sBoxMap.put('B', 'C');
   	 sBoxMap.put('C', '5');
   	 sBoxMap.put('D', '9');
   	 sBoxMap.put('E', '0');
   	 sBoxMap.put('F', '7');
   	 return sBoxMap;
    }

    // S-box value
    private static int[] sbox(int[] input, HashMap<Character, Character> sMap, HashMap<Character, int[]> hexMap) {
   	 int[] ans = new int[16];
   	 for (int i = 0; i < 13; i += 4) {
   		 // changed
   		 int[] temp = { input[i], input[i + 1], input[i + 2], input[i + 3] };
   		 /*
   		  * for (int j = 0; j < 4; j++) { temp[j] = input[i]; }
   		  */
   		 // transfer from binary to hex
   		 char hex = bin2Hex(temp);
   		 // put this through the sbox hashmap
   		 hex = sMap.get(hex);
   		 // pull the answer out and transfer from hex to binary
   		 temp = hexMap.get(hex);
   		 // changed
   		 for (int j = 0; j < 4; j++) {
   			 ans[i + j] = temp[j];
   		 }
   	 }
   	 return ans;
    }

    // permutation key
    // changed
    private static int[] permutation(int[] input) {
   	 int[] ans = { input[0], input[4], input[8], input[12], input[1], input[5], input[9], input[13], input[2],
   			 input[6], input[10], input[14], input[3], input[7], input[11], input[15] };
   	 return ans;
    }
}
