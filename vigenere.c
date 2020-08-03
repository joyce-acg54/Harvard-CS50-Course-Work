#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
int shift(char key);
int main(int argc, string argv[])
{
    // Command line must have 2 arguments
    if (argc != 2)
    {
        printf("Usage: ./vigenere key\n");
        return 1;
    }
    //Command line's 2nd argument, array [1] members must only contain a string
    for (int i = 0, k = strlen(argv[1]); i < k; i++)
    {
        if (isdigit(argv[1][i]))
        {    
            printf("Usage: ./vigenere key\n");
            return 1;
        }
    }
    
    //prompt to get plain text string
    string p = get_string("plaintext: ");
    
    //return to cipher text string
    printf("ciphertext: ");
    
    //capture each array member of string p
    //capture keys generated from strings with shift
    //add each key from keys to each char of string plain UNTIL ALL KEYS ARE USED UP
    //kn is the lenght of keys
    int kn = strlen(argv[1]);
    
    for (int j = 0; j < kn; j++)
    {
        //if uppercase
        if (p[j] >= 65 && p[j] <= 90)
        {
            printf("%c", (((p[j] + shift(argv[1][j])) - 65) % 26) + 65);
        }
        //if lowercase
        else if (p[j] >= 97 && p[j] <= 122)
        {
            printf("%c", (((p[j] + shift(argv[1][j])) - 97) % 26) + 97);
        }
        //if symbols or numbers
        else
        {
            printf("%c", p[j]);
        }
        
    }
    
    //repeat ciphering from last i of keys
    //key should be initialized from 0, but plaintext should be initialized from length of key
    //cn = strlen(p) is length of plaintext
    int cn = strlen(p);
    
    for (int k = kn; k < cn; k++)
    {
        //if uppercase
        if (p[k] >= 65 && p[k] <= 90)
        {
            printf("%c", (((p[k] + shift(argv[1][k - kn])) - 65) % 26) + 65);
        }
        //if lowercase
        else if (p[k] >= 97 && p[k] <= 122)
        {
            printf("%c", (((p[k] + shift(argv[1][k - kn])) - 97) % 26) + 97);
        }
        //if symbols or numbers
        else
        {
            printf("%c", p[k]);
        }
         
    }   
       
    printf("\n");    
        
}
    
//create function shift to be used and declared above
int shift(char key)
{
    int num;
    if (key >= 65 && key <= 90)
    {
        return num = key - 65;

    }
    else if (key >= 97 && key <= 122)
    {
        return num = key - 97;
    }
    else
    {
        return 0;
    }
}


