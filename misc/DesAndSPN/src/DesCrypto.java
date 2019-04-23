import java.util.Scanner;

public class DesCrypto {

	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		byte[] key = new byte[64];
		byte[] text = new byte[64];

		String temp = in.next();
		for (int i = 0; i < 64; i++) {
			key[i] = (byte) (temp.charAt(i) - '0');
		}
		temp = in.next();
		for (int i = 0; i < 64; i++) {
			text[i] = (byte) (temp.charAt(i) - '0');
		}

		byte[] permutedText = InitialPermutation(text);
		byte[] C0D0Key = C0D0Subkey(key);
		byte[] C0 = new byte[28];
		byte[] D0 = new byte[28];
		for (int i = 0; i < 28; i++) {
			C0[i] = C0D0Key[i];
		}
		for (int i = 0; i < 28; i++) {
			D0[i] = C0D0Key[i + 28];
		}

		byte[][] keyMatrix = BuildKeySchedule(C0, D0);

		byte[] cipherText = encrypted(permutedText, keyMatrix);
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < 64; i++) {
			sb.append(cipherText[i]);
		}
		in.close();
		
		System.out.println(sb.toString());
	}

	private static byte[] encrypted(byte[] permutedText, byte[][] keyMatrix) {
		byte[] Ri = new byte[32];
		byte[] Li = new byte[32];
		for (int i = 0; i < 32; i++) {
			Li[i] = permutedText[i];
			Ri[i] = permutedText[i + 32];
		}

		for (int i = 0; i < 16; i++) {
			byte[] temp = Ri;
			Ri = Xor(Li, FestolFunction(Ri, keyMatrix[i]), 32);
			Li = temp;
		}
		byte[] cipherTextPre = new byte[64];
		for (int i = 0; i < 32; i++) {
			cipherTextPre[i] = Ri[i];
			cipherTextPre[i + 32] = Li[i];
		}
		
		int[][] reversePermutation = 
			{
				{40, 8, 48, 16, 56, 24, 64, 32},
	            {39, 7, 47, 15, 55, 23, 63, 31},
	            {38, 6, 46, 14, 54, 22, 62, 30},
	            {37, 5, 45, 13, 53, 21, 61, 29},
	            {36, 4, 44, 12, 52, 20, 60, 28},
	            {35, 3, 43, 11, 51, 19, 59, 27},
	            {34, 2, 42, 10, 50, 18, 58, 26},
	            {33, 1, 41, 9,  49, 17, 57, 25}
			};
		
		byte[] cipherTextPermuted = new byte[64];
		for(int y = 0; y < 8; y++)
		{
			for(int x = 0; x < 8; x++)
			{
				cipherTextPermuted[y*8+x] = cipherTextPre[reversePermutation[y][x]-1];
			}
		}
		
		return cipherTextPermuted;
	}

	private static byte[] Xor(byte[] li, byte[] ri, int len) {
		byte[] ret = new byte[len];
		for (int i = 0; i < len; i++) {
			ret[i] = (byte) ((li[i] ^ ri[i]));
		}
		return ret;
	}

	private static byte[] FestolFunction(byte[] ri, byte[] Keyi) {
		int[][] indexExpansionTable = 
			{ 
				{ 32, 1, 2, 3, 4, 5 },
				{ 4, 5, 6, 7, 8, 9 },
				{ 8, 9, 10, 11, 12, 13 },
				{ 12, 13, 14, 15, 16, 17 },
				{ 16, 17, 18, 19, 20, 21 },
				{ 20, 21, 22, 23, 24, 25 },
				{ 24, 25, 26, 27, 28, 29 },
				{ 28, 29, 30, 31, 32, 1 }
			};
		
		byte[] ERi = new byte[48];
		for (int y = 0; y < 8; y++) {
			for (int x = 0; x < 6; x++) {
				ERi[6 * y + x] = ri[indexExpansionTable[y][x]-1];
			}
		}

		byte[] preSbox = Xor(ERi, Keyi, 48); // 48 long
		int[][][] sboxArr = new int[8][4][16];
		
		int[][] sbox1 = 
			{ 
				{ 14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7 },
				{ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8 },
				{ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0 },
				{ 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 }
			};
		sboxArr[0] = sbox1;
		
		int[][] sbox2 = 
			{ 
				{ 15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10 },
				{ 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5 },
				{ 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15 },
				{ 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 } 
			};
		sboxArr[1] = sbox2;
		
		int[][] sbox3 = 
			{
				{ 10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8 },
				{ 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1 },
				{ 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7 },
				{ 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 }
			};
		sboxArr[2] = sbox3;
		
		int[][] sbox4 = 
			{
				{ 7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15 },
			    { 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9 },
			    { 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4 },
			    { 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14 }
			};
		sboxArr[3] = sbox4;
		
		int[][] sbox5 = 
			{ 
				{ 2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9 },
				{ 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6 },
				{ 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14 },
				{ 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 }
			};
		sboxArr[4] = sbox5;
		
		int[][] sbox6 = 
			{ 
				{ 12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11 },
				{ 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8 },
				{ 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6 },
				{ 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13 }
			};
		sboxArr[5] = sbox6;
		
		int[][] sbox7 = 
			{ 
				{ 4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1 },
				{ 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6 },
				{ 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2 },
				{ 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12 }
		};
		sboxArr[6] = sbox7;
		
		int[][] sbox8 = { 
				{ 13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7 },
				{ 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2 },
				{ 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8 },
				{ 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11 } 
			};
		sboxArr[7] = sbox8;
		
		byte[] sboxPre = new byte[32];
		for(int y = 0; y < 8; y++)
		{
			byte[] sboxInput = new byte[6];
			for(int x = 0; x < 6; x++)
			{
				sboxInput[x] = preSbox[y*6+x];
			}
			int sboxYIndex = (sboxInput[0] << 1) | (sboxInput[5]);
			int sboxXIndex = (sboxInput[1] << 3) 
					| (sboxInput[2] << 2 ) 
					| (sboxInput[3] << 1) 
					| (sboxInput[4]);
		
			int sboxValue = sboxArr[y][sboxYIndex][sboxXIndex]; 
			byte[] temp = intToByteArr(sboxValue);
			for(int i = 0; i < 4; i++)
			{
				sboxPre[y*4 + i] = temp[i];
			}
		}
		
		int[][] functionPermutation = 
			{
				{16, 7, 20, 21},
                {29, 12, 28, 17},
                {1, 15, 23, 26},
                {5, 18, 31, 10},
                {2, 8,  24, 14},
                {32, 27, 3, 9},
                {19, 13, 30, 6},
                {22, 11, 4, 25}
			};
		
		byte[] sboxAns = new byte[32];
		for(int y = 0; y < 8; y++)
		{
			for(int x = 0; x < 4; x++)
			{
				sboxAns[y*4 + x] = sboxPre[functionPermutation[y][x] - 1];
			}
		}
		return sboxAns;
	}

	private static byte[] intToByteArr(int x) 
	{
		byte[] ret = new byte[4];
		for(int i = 3; i >= 0; i--)
		{
			ret[i] = (byte)(x % 2);
			x = x >>> 1;
		}
		return ret;
	}

	private static byte[][] BuildKeySchedule(byte[] c0, byte[] d0) {
		byte[][] keyMatrix = new byte[16][56];
		int[] shiftByIndex = 
			{ 1, 1, 2, 2,
			  2, 2, 2, 2,
			  1, 2, 2, 2,
			  2, 2, 2, 1 };
		byte[] Ci = c0;
		byte[] Di = d0;
		for (int i = 0; i < 16; i++) {
			Ci = shiftBy(Ci, shiftByIndex[i]);
			Di = shiftBy(Di, shiftByIndex[i]);
			byte[] CiDi = new byte[Ci.length + Di.length];
			for (int x = 0; x < 28; x++) {
				CiDi[x] = Ci[x];
			}
			for (int x = 0; x < 28; x++) {
				CiDi[x + 28] = Di[x];
			}

			byte[] CiDiPermuted = PC2(CiDi);
			keyMatrix[i] = CiDiPermuted;

		}
		return keyMatrix;
	}

	private static byte[] PC2(byte[] CiDi) {
		int[][] indexPermutation = 
			{ 
				{ 14, 17, 11, 24, 1, 5 },
				{ 3, 28, 15, 6, 21, 10 },
				{ 23, 19, 12, 4, 26, 8 },					
				{ 16, 7, 27, 20, 13, 2 },
				{ 41, 52, 31, 37, 47, 55 },
				{ 30, 40, 51, 45, 33, 48 },
				{ 44, 49, 39, 56, 34, 53 },
				{ 46, 42, 50, 36, 29, 32 } 
			};

		byte[] output = new byte[48];

		for (int y = 0; y < 8; y++) {
			for (int x = 0; x < 6; x++) {
				output[6 * y + x] = CiDi[indexPermutation[y][x] - 1];
			}
		}

		return output;
	}

	private static byte[] shiftBy(byte[] ci, int x) {
		byte[] ret = new byte[ci.length];
		for (int i = 0; i < ci.length; i++) {
			ret[i] = ci[(i + x) % ci.length];
		}
		return ret;
	}

	/**
	 * This returns a an array in dim compressed form ie you need to use 8y + x
	 * to access [y][x]
	 * 
	 * @param arr
	 *            is the byte array in order
	 * @return
	 */
	public static byte[] InitialPermutation(byte[] text) {
		int[][] indexPermutation = 
			{ 
				{ 58, 50, 42, 34, 26, 18, 10, 2 },
				{ 60, 52, 44, 36, 28, 20, 12, 4 },
				{ 62, 54, 46, 38, 30, 22, 14, 6 },
				{ 64, 56, 48, 40, 32, 24, 16, 8 },
				{ 56, 49, 41, 33, 25, 17, 9, 1 },
				{ 59, 51, 43, 35, 27, 19, 11, 3 },
				{ 61, 53, 45, 37, 29, 21, 13, 5 },
				{ 63, 55, 47, 39, 31, 23, 15, 7 } 
			};

		byte[] output = new byte[64];

		for (int y = 0; y < 8; y++) {
			for (int x = 0; x < 8; x++) {
				output[8 * y + x] = text[indexPermutation[y][x] - 1];
			}
		}
		return output;
	}

	/**
	 * Returns C0 and D0 in a 56 len array
	 * 
	 * @param key
	 * @return
	 */
	public static byte[] C0D0Subkey(byte[] key) {

		int[][] CDIndexPermutation = 
			{ 
				{ 57, 49, 41, 33, 25, 17, 9 },
				{ 1, 58, 50, 42, 34, 26, 18 },
				{ 10, 2, 59, 51, 43, 35, 27 },
				{ 19, 11, 3, 60, 52, 44, 36 },
				{ 63, 55, 47, 39, 31, 23, 15 },
				{ 7, 62, 54, 46, 38, 30, 22 },
				{ 14, 6, 61, 53, 45, 37, 29 },
				{ 21, 13, 5, 28, 20, 12, 4 }
			};

		byte[] output = new byte[56];

		for (int y = 0; y < 8; y++) {
			for (int x = 0; x < 7; x++) {
				output[7 * y + x] = key[CDIndexPermutation[y][x] - 1];
			}
		}
		return output;
	}

}
