#include <stdio.h>
#include <stdlib.h>
#include "sma.h"
float SMA(float arr [], int n);


float SMA(float arr[], int n)
{
	
	float total = 0;
	for(int i = 0; i < n; i++)
		total+=arr[n];


	return (float)total/n;
	
}

int main(){

return 0;

}
