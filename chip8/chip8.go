package chip8

type Chip8 struct{
	Memory [4096]byte
	VRegisters [16]byte
	IndexRegister uint16
	PC uint16
	Stack [16]uint16
	SP uint8
	Delay byte
	Sound byte
	Display [64 * 32]byte
	CharMemory [15][5]byte
}

func NewChip8() *Chip8 {// returns a chip8 object pointer
	c := &Chip8{} //new Chip8 pointer
	c.PC = 0x200 //Program counter starts at 0x200 where prog mem is
	//okay let's try and init our CharMemory with the default Chip8 characters
	
	return c
}

func displayScreen() bool{
	return false;
}
