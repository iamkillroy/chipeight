package main


type chip8 struct{
	Memory [4096]byte
	VRegisters [16]byte
	IndexRegister uint16
	PC uint16
	Stack [16]uint16
	SP uint8
	Delay byte
	Sound byte
	Display [24 * 23]byte
}

function initChip8() *Chip8 {// returns a chip8 object pointer
	c := &Chip8{} //new Chip8 pointer
	c.PC = 0x200 //Program counter starts at 0x200 where prog mem is
	return c
}

