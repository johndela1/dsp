/*compile with -lm */
#include <math.h>
#include <stdio.h>
#include <unistd.h>
#define PI 3.14159265359

int main()
{
	
	int sampleRate = 8000;
	double amplitude = 0.25 *  0x7fff;
	short output;
	double freq = 10;
	int n;
	for (n = 0; n < sampleRate; n++)
	{
		output = (short)(amplitude * sin(( 2*PI*n *
			freq) / sampleRate));
		write(1, &output, sizeof(short));
	}
}
