Please use the provided 7400-lib.circ. The actual library had problem with the 
7483 IC (4-bit Adder).

The problem : C out (14) is marked as input rather than output

If you wish to use the actual library, please resolve the issue by editing the pin.

THANK YOU

Group Members:
	1805046, 1805047, 1805048, 1805052, 1805057


OPEARATIONS

cs2-Cin	cs1	cs0	Opeation
------- ------- ------- ----------------
0	0	0	DEC A
0	0	1	SUB with BORROW
x	1	0	OR
1	0	0	TRANSFER
1	0	1	SUBTRUCT
x	1	1	AND