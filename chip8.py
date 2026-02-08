#########################
# 	CHIP 8		#
# PYTHON CHIP EMULATION #
#########################

class Chip8:
	def __init__(self):
		#Program Counter -- all Chip8 Emulation
		#starts at 0x200, first 200 are reserved for
		#the runtime
		self.PC = 0x200
		#Stack Pointer, starts at 0x00
		#and has a max size of 17
		self.SP = 0x00
		#vRegisters, stored to do math in 16
		#bit numbers and itnegers
		self.vRegisters = [0] * 16
		#actual stack, what we'll be moving
		#through
		self.stack = [0] * 16
		#constant namespace
		self._NAME = {"NONE": 0, "SYS": 1, "CLS": 2, "JP":3, "RT":4, "CALL":5, "SE":6, "SNE":6}
		self._TYPE = {"IMPL": 0, "ADDR": 1, "VX, BYTE": 2}
	def returnInstruction(self, instruction):
		"""Uses match cases based on a nibble to return a tuple of 
		both the opcode given and the operand provided, and its type defined from
		self._TYPE[XXXX]"""
		#Specify special flags that occur
		#Let's do a bytewise AND comparison
		#and since F is high the value stored will be
		#reflected in 0000s
		#EX: A is 1010 so with F (1111) & it's
		#	1010
		#     & 1111
		#     -------	
		#	1010
		#the rest of the bits becomes 0 because it's
		# 0 & 1 or 0 & 0 = 1
		#now that we know the 'type', we can assign the
		#command type based off of this
		#we also need the next significant nibble to check 
		#the values
		mostSignificantNibble = 0xF & (instruction >> 12)
		secondMostSignificantNibble = 0xF & (instruction >> 8)
		thirdMostSignificantNibble = 0xF & (instruction >> 4)
		leastMostSignificantNibble = 0xF & instruction
		#initialise to nontypes for all, and when 
		#we have implicit functions like RTS and CLS
		#that don't need data we can just
		#set the data to be implicit already
		operationNamespace = self._NAME["NONE"]
		operationData = 0x000
		operationDataType = self._TYPE["IMPL"] #implicit, there's nothing needed
		#we match/case because it's better than if AND we can do some wildacrd
		#operators for certain addresses and it's less confusing
		#in our program flow
		match (mostSignificantNibble):
			case 0x0:
				
				match (thirdMostSignificantNibble, leastMostSignificantNibble):
					case 0xE, 0x0: #0x00E0 CLS (clear screen)
						operationNamespace = self._NAME["CLS"]
					case 0x0, 0xE, 0xE: #0x00EE RT (return from sub)
						operationNamespace = self._NAME["RT"]
					case  _, _:
						operationNamespace = self._NAME["SYS"]
			case 0x1: 
				operationNamespace = self._NAME["JP"]
				operationDataType = self._TYPE["ADDR"]
				operationData = 0x0FFF & instruction
			case 0x2: 
				operationNamespace = self._NAME["CALL"]
				operationDataType = self._TYPE["ADDR"]
				operationData = 0x0FFF & instruction
			case 0x3: 
				operationNamespace = self._NAME["SE"]
				operationDataType = self._TYPE["VX, BYTE"]
				operationData = 0x0FFF & instruction
			case 0x4: 
				operationNamespace = self._NAME["SNE"]
				operationDataType = self._TYPE["VX, BYTE"]
				operationData = 0x0FFF & instruction
			
	def do(self, instruction):
		"""Do the instruction given on the instance of the VM
		Takes an expected 16 bit Little Endian (LE) number
		Returns values if optional kwargs are set"""
		#Specify the instruction type
		instructionType = None 
		print(self.returnInstruction(mostSignificantNibble, secondMostSignificantNibble, thirdMostSignificantNibble, leastMostSignificantNibble))
		
		