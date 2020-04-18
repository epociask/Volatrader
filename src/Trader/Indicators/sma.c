#include<stdio.h>
#include "sma.h"



float SMA(float [] n){
	
	float total = 0;
	int len = sizeof(n)/sizeof(n[0]);

	for(int i = 0; i < len; i++)	
	total += n[i];
	

	return total / len;


}
