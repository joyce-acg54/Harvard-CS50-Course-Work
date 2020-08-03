#include <cs50.h>
#include <stdio.h>

int main(void)
{
    
    int h = get_int("Height: ");
    while ((h < 1) || (h > 8))  
    {
        h = get_int("Height: ");
    }
    
    //rows
    for (int i = 1; i <= h; i++)
    {
        //spaces
        for (int k = 1; k <= h - i; k++)
        {
            printf(" ");
        }
        //#
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        
        
        printf("  ");
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        
        printf("\n");
    }
      
}


