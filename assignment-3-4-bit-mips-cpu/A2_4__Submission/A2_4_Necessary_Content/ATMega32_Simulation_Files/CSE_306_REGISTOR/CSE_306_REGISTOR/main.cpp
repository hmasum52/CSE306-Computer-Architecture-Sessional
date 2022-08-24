/*
 * CSE_306_REGISTOR.cpp
 *
 * Created: 16-Aug-22 12:57:43 AM
 * Author : sabit
 */ 

#define F_CPU 1000000UL
#include <avr/io.h>
#include <util/delay.h>

#define WRITE_REG_	0x01
#define CLK_		0x02
#define RESET_		0x04
#define OUTPUT_		0x08

uint8_t REGISTOR[8] = {0};

int main(void)
{
	// Some pins of PORTC can not be used for I/O directly.
	// turn of JTAG to use them
	// o write a 1 to the JTD bit twice consecutively to turn it off
	MCUCSR = (1<<JTD);  MCUCSR = (1<<JTD);
	
    DDRA = 0x00;	// A[3:0] - SrcReg1, A[7:4] - SrcReg2
	DDRB = 0x00;	// B[3:0] - DstReg, B[7:4] - Write Data
	
	DDRC = 0xFF;	// C[3:0] - $1, C[7:4] - $2
	DDRD = 0xF0;	// D[0] - WriteReg, D[1] - CLK, D[2] - RESET
	
	uint8_t src, dst_data, last_control = 0, current_control;
	
    while (1) 
    {
		src = PINA;
		dst_data = PINB;
		current_control = PIND;
		
		PORTC = (REGISTOR[(src>>4)&0x7]<<4) | (REGISTOR[src&0x7]);
		if (current_control&RESET_) {
			for (uint8_t i=0; i<8; i++) REGISTOR[i] = 0;
			_delay_ms(100);
			continue;
		}
		
		if ((current_control^last_control)&CLK_) {							// EDGE
			if ((last_control&CLK_) && (last_control&WRITE_REG_)) {	// NEGATIVE EDGE with WRITE INSTRUCTION
				REGISTOR[dst_data&0x7] = (dst_data>>4);
				PORTD = dst_data & 0xf0;
			}
			_delay_ms(100);
		}
		
		last_control = current_control;
    }
}

