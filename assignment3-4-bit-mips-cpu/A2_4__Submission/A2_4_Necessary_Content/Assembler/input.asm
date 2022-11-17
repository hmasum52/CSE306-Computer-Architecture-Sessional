 		addi $t1, $zero, 3		// $t1 = 3 	// addi ok				^
 		subi $t2, $zero, -2		// $t2 = 2 	// subi ok 		        ^
 		add $t0, $t1, $t2 		// $t0 = 5 	// add ok				^
		sub $t3, $t1, $t2		// $t3 = 1	// sub ok 			    ^
	nor $t4, $t0, $t2		// $t4 = -8 	// nor ok, all regs ok	^	
	sw $t1, 3($t2)		// m[5] = 3	// sw ok 	                    ^
		srl $t2, $t2, 1		// $t2 = 1 	// srl ok				    ^
 		beq $t2, $t3, label1		// branching will execute // beq ok ^	
 		j end
 label1:	sll $t3, $t3, 1		// $t3 = 2	// sll ok				^
 		lw $t2, 4($t2)		// $t2 = 3	// lw ok                    ^
		push $t1			// m[F] = 3 // push ok                  ^
 		push $t2			// m[E] = 3 // push ok		            ^
 		j label2			// jump will execute // j ok		    
label3:    or $t0, $t0, $t2		// $t0 = 7 	// or ok    	        ^
		andi $t2, $t4, 1 		// $t2 = 0 	// and ok			    ^
		ori $t1, $t1, 5		// $t1 = 7 	// ori ok			        ^
		pop $t2 			// $t2 = 3 	// pop ok			        ^
 		and $t1, $t2, $t4		// $t1 = 0 	// andi ok			    ^
 		pop $t1			// $t1 = 3 	// pop ok				        ^
j end				// jump will execute // j ok			        ^
label2:    beq $t0, $t2, end	// branching will not execute // beq not ok ^
        j label3                                                    ^
end:
