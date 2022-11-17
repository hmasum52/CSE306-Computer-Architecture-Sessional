/*
 * CSE_306-CONTROL.cpp
 *
 * Created: 15-Aug-22 3:31:50 PM
 * Author : sabit
 */ 

#define F_CPU 1000000UL
#include <avr/io.h>
#include <util/delay.h>

uint16_t CONTROL_ROM[1<<4] = {0x902, 0x505, 0x500, 0x503, 0x903, 0x640, 0x901, 0x501, 0x021, 0x502, 0x008, 0x904, 0x011, 0x780, 0x900, 0x506};

int main(void)
{
	// Some pins of PORTC can not be used for I/O directly.
	// turn of JTAG to use them
	// o write a 1 to the JTD bit twice consecutively to turn it off
	MCUCSR = (1<<JTD);  MCUCSR = (1<<JTD);
	
    DDRA = 0xF0; // A[3:0] - Opcode Input
	
	// Control Unit Bits : C[3:0]B[7:0]
	// C[reg_dst[1], alu_src[1], mem_to_reg[1], reg_write[1]] B[mem_read[1], mem_write[1], branch[1], branch_neq[1], jump[1], alu_op[3]]
	DDRB = 0xFF;
	DDRC = 0xFF;
	
	uint8_t opcode = ~0;
	
    while (1) 
    {
		if (opcode != (0x0F & PINA)) {
			opcode = (0x0F & PINA);
			PORTB = CONTROL_ROM[opcode];
			PORTC = (CONTROL_ROM[opcode] >> 8);
			_delay_ms(50);
		}
    }
}

