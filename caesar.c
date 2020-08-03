#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Command line must have 2 arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    //Command line's 2nd argument, array [1] members must only contain integers
    int key = atoi(argv[1]);

    for (int i = 0, k = strlen(argv[1]); i < k; i++)
    {
        if (!isdigit(argv[1][i]))
        {    
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }  
    
    //print success and value if input is a valid integer
    printf("Success\n");
    printf("%i\n", key);
    
    //get string from user   
    string p = get_string("plaintext: ");
    
    //print ciphertext
    printf("ciphertext: ");  
    
    //capture each array member of string p
    for (int j = 0, pn = strlen(p); j < pn; j++)
    {
        //if uppercase
        if (p[j] >= 65 && p[j] <= 90)
        {
            printf("%c", (((p[j] + key) - 65) % 26) + 65);
        }
        //if lowercase
        else if (p[j] >= 97 && p[j] <= 122)
        {
            printf("%c", (((p[j] + key) - 97) % 26) + 97);
        }
        //if symbols or numbers
        else
        {
            printf("%c", p[j]);
        }
                            
    }
        
    printf("\n");

    
     
}
