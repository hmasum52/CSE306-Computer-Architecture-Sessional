/*
 * CSE_306_DATA_MEMORY.cpp
 *
 * Created: 15-Aug-22 4:22:26 PM
 * Author : sabit
 */ 

#define F_CPU 1000000UL
#include <avr/io.h>
#include <util/delay.h>

#define CLK_		0x04
#define RESET_		0x08
#define MEM_READ_	0x02
#define MEM_WRITE_	0x01

uint8_t MEMORY[1<<4];

void memory_reset() {
	for (int i=0; i<16; i++)
		MEMORY[i] = 0;
}

int main(void)
{
	// Some pins of PORTC can not be used for I/O directly.
	// turn of JTAG to use them
	// o write a 1 to the JTD bit twice consecutively to turn it off
	MCUCSR = (1<<JTD);  MCUCSR = (1<<JTD);
	
    DDRA = 0xF0;	// A[0] - Memory Write | A[1] - Memory Read | A[2] - Clock | A[3] - Reset
	DDRB = 0x00;	// Address B[3:0] | Write Data B[7:4]
	
	DDRC = 0xFF;	// C[3:0] - Data Read
	
	memory_reset();
	
	uint8_t last_control_input = 0b0000, current_control_input;
	uint8_t last_write_data_address = 0b0000, current_write_data_address;
	
    while (1) 
    {
		current_control_input = PINA & 0xF;
		current_write_data_address = PINB;
		if (current_control_input & RESET_) {
			memory_reset();
			_delay_ms(100);
		} else if ((last_control_input ^ current_control_input) & CLK_) {			// EDGE
			if (last_control_input & CLK_) {						// NEG-EDGE - for writing
				if (last_control_input & MEM_WRITE_) {
					MEMORY[last_write_data_address & 0xF] = (last_write_data_address >> 4);
				}
			}
			_delay_ms(100);
		} 
		if (current_control_input & MEM_READ_) {
			PORTC = MEMORY[current_write_data_address & 0xF];
		}
			
		last_control_input = current_control_input;
		last_write_data_address = current_write_data_address;
	}
}

