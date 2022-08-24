/*
 * CSE_306_ALU.cpp
 *
 * Created: 16-Aug-22 1:51:51 AM
 * Author : sabit
 */

#include <avr/io.h>
#define F_CPU 1000000 // Clock Frequency
#include <util/delay.h>


int main(void)
{
    // Some pins of PORTC can not be used for I/O directly.
    // turn of JTAG to use them
    // o write a 1 to the JTD bit twice consecutively to turn it off
    MCUCSR = (1<<JTD);  MCUCSR = (1<<JTD);

	DDRA = 0x00;				// A[3:0], B[7:4]
	DDRB = 0xF8;				// ALUOp B[2:0]
	DDRD = 0x8f;				// D[7] - Zero Flag | D[3:0] - Output

	uint8_t control_bits;
	uint8_t in1, in2, out;

	while (1)
	{
		control_bits = PINB & 0x07;

		in1 = PINA & 0x0f;
		in2 = (PINA & 0xf0) >> 4;
		out = 0;

		if(control_bits == 0) {
			out = in1 + in2;
		} else if(control_bits == 1){
			out = in1 - in2;
		} else if(control_bits == 2) {
			out = in1 & in2;
		} else if(control_bits == 3) {
			out = in1 | in2;
		} else if(control_bits == 4) {
			out = ~(in1 | in2);
		} else if(control_bits == 5) {
			out = in1 << in2;
		} else if(control_bits == 6) {
			out = in1 >> in2;
		}

		out = out & 0x0f;
		if(!out) {
			out = out | 0x80;
		}

		PORTD = out;
	}
}

