#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float x;
    do
    {
        x = get_float("Change: ");
    }
    while (x < 0);
    int c = round(x * 100);
    
    //how many quarters are used?  
    int q = c / 25;
    c = c % 25;
    
    //how many dimes are used?
    int d = c / 10;
    c = c % 10;
        
    //how many nickels are used?
    int n = c / 5;
    c = c % 5;
    
    //how many pennies are used?
    int p = c / 1;
    c = c % 1;
           
    printf("%i\n", q + d + n + p);  
   
  
}



