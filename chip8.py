#########################
#     CHIP 8            #
# PYTHON CHIP EMULATION #
#########################

from operator import le


class Chip8:
    def __init__(self):
        # Program Counter -- all Chip8 Emulation
        # starts at 0x200, first 200 are reserved for
        # the runtime
        self.PC = 0x200
        # Stack Pointer, starts at 0x00
        # and has a max size of 17
        self.SP = 0x00
        # vRegisters, stored to do math in 16
        # bit numbers and itnegers
        self.vRegisters = [0] * 16
        # actual stack, what we'll be moving
        # through
        self.stack = [0] * 16
        self.debug = True #debug mode, prints registers and outputs
        # constant namespace
        self._NAME = {
            "NONE": 0,
            "SYS ADDR": 1,
            "CLS": 2,
            "JP ADDR": 3,
            "RT": 4,
            "CALL ADDR": 5,
            "SE VX BYTE": 6,
            "SNE VX BYTE": 7,
            "SE VX VY": 9,
            "LD VX BYTE": 10,
            "ADD VX BYTE": 11,
            "LD VX VY": 12,
            "AND VX VY": 13,
            "OR VX VY": 14,
            "XOR VX VY": 15,
            "ADD VX VY": 16,
            "SUB VX VY": 17,
            "SHR VX VY": 18,
            "SUBN VX VY": 19,
            "SHL VX VY": 20,
            "SNE VX VY": 21,
            "LD I ADDR": 22,
            "SKP VX": 23,
            "SNKP VX": 24,
            "LD VX DT": 25,
            "LD VX ST": 26,

        }
        self._TYPE = {
            "IMPL": 0,
            "ADDR": 1,
            "VX, BYTE": 2,
            "VX, VY": 3,
            "VX, VY 8 INSTRUCTION": 4,
            "ADDR + V0": 5,
            "VX KEY": 5,

        }

    def returnInstruction(self, instruction):
        """Uses match cases based on a nibble to return a tuple of
        both the opcode given and the operand provided, and its type defined from
        self._TYPE[XXXX]
        """
        # Specify special flags that occur
        # Let's do a bytewise AND comparison
        # and since F is high the value stored will be
        # reflected in 0000s
        # EX: A is 1010 so with F (1111) & it's
        #     1010
        #     & 1111
        #     -------
        #     1010
        # the rest of the bits becomes 0 because it's
        # 0 & 1 or 0 & 0 = 1
        # now that we know the 'type', we can assign the
        # command type based off of this
        # we also need the next significant nibble to check
        # the values
        mostSignificantNibble = 0xF & (instruction >> 12)
        secondMostSignificantNibble = 0xF & (instruction >> 8)
        thirdMostSignificantNibble = 0xF & (instruction >> 4)
        leastMostSignificantNibble = 0xF & instruction

        # initialise to nontypes for all, and when
        # we have implicit functions like RTS and CLS
        # that don't need data we can just
        # set the data to be implicit already
        operationNamespace = self._NAME["NONE"]
        operationDataType = self._TYPE["IMPL"]  # implicit, there's nothing needed

        # we match/case because it's better than if AND we can do some wildacrd
        # operators for certain addresses and it's less confusing
        # in our program flow
        operationData = 0x0FFF & instruction  # if you don't need this don't access it

        match mostSignificantNibble:
            case 0x0:
                match thirdMostSignificantNibble, leastMostSignificantNibble:
                    case 0xE, 0x0:  # 0x00E0 CLS (clear screen)
                        operationNamespace = self._NAME["CLS"]
                    case 0xE, 0xE:  # 0x00EE RT (return from sub)
                        operationNamespace = self._NAME["RT"]
                    case _, _:
                        operationNamespace = self._NAME["SYS ADDR"]
                        operationDataType = self._TYPE["ADDR"]

            case 0x1:
                operationNamespace = self._NAME["JP ADDR"]  # JP 0x1nnn
                operationDataType = self._TYPE["ADDR"]

            case 0x2:
                operationNamespace = self._NAME["CALL ADDR"]  # CALL 0x2nnn
                operationDataType = self._TYPE["ADDR"]

            case 0x3:
                operationNamespace = self._NAME["SE VX BYTE"]  # SKIP next byte if Vx == kk 0x3xkk
                operationDataType = self._TYPE["VX, BYTE"]

            case 0x4:
                operationNamespace = self._NAME["SNE "]  # Skip if Vx is !+ kk 0x4xkk
                operationDataType = self._TYPE["VX, BYTE"]

            case 0x5:
                operationNamespace = self._NAME["SE VX VY"]  # SKIP next byte if Vx == Vy 0x5xy0
                operationDataType = self._TYPE["VX, VY"]

            case 0x6:
                operationNamespace = self._NAME["LD VX BYTE"]
                operationDataType = self._TYPE["VX, BYTE"]
            case 0x7:
                    operationNamespace = self._NAME["ADD VX BYTE"]
                    operationDataType = self._TYPE["VX, BYTE"]
            case 0x8:
                match leastMostSignificantNibble:
                    case 0: #loads value in vs to vy
                        operationNamespace = self._NAME["LD VX VY"]
                        operationDataType = self._TYPE["VX, VY 8 INSTRUCTION"]
                    case 1: #loads value in vs to vy
                        operationNamespace = self._NAME["OR VX VY"]
                        operationDataType = self._TYPE["VX, VY 8 INSTRUCTION"]
                    case 2: #loads value in vs to vy
                        operationNamespace = self._NAME["AND VX VY"]
                        operationDataType = self._TYPE["VX, VY 8 INSTRUCTION"]
                    case 3: #loads value in vs to vy
                        operationNamespace = self._NAME["XOR VX VY"]
                        operationDataType = self._TYPE["VX, VY 8 INSTRUCTION"]
                    case 4: #loads value in vs to vy
                        operationNamespace = self._NAME["ADD VX VY"]
                        operationDataType = self._TYPE["VX, VY 8 INSTRUCTION"]
                    case 5:
                        operationNamespace = self._NAME["SUB XY VY"]
                        operationDataType = self._TYPE["VX, VY 8 INSTRUCTION"]
                    case 6: #loads value in vs to vy
                        operationNamespace = self._NAME["SHR VX VY"]
                        operationDataType = self._TYPE["VX, VY 8 INSTRUCTION"]
                    case 7: #loads value in vs to vy
                        operationNamespace = self._NAME["SUBN VX VY"]
                        operationDataType = self._TYPE["VX, VY 8 INSTRUCTION"]
            case 0x9:
                operationNamespace = self._NAME["SNE VX VY"]
                operationDataType = self._TYPE["VX, VY 8 INSTRUCTION"]
            case 0xA:
                operationNamespace = self._NAME["LD I ADDR"]
                operationDataType = self._TYPE["ADDR"]
            case 0xB:
                operationNamespace = self._NAME["JP V0 ADDR"]
                operationDataType = self._TYPE["ADDR + V0"]
            case 0xC:
                operationNamespace = self._NAME["RND VX BYTE"]
                operationDataType = self._TYPE["VX, BYTE"]
            case 0xD:
                operationNamespace = self._NAME["DRW VX VY NIBBLE"]
                operationDataType = self._TYPE["VX, VY NIBBLE"]
            case 0xE:
                match thirdMostSignificantNibble, leastMostSignificantNibble:
                    case 0x9, 0xE: #Skips next instruction if key Vx is press
                        operationNamespace = self._NAME["SKP VX"]
                        operationDataType = self._TYPE["VX KEY"]
                    case 0xA, 0x1: #Skips next instruction if key Vx is press
                        operationNamespace = self._NAME["SNKP VX"]
                        operationDataType = self._TYPE["VX KEY"]
            case 0xF:
                match thirdMostSignificantNibble, leastMostSignificantNibble:
                    case 0x0, 0x7:
                        operationNamespace = self._NAME["LD VX DT"]
                        operationDataType = self._TYPE["VX KEY"]
                    case 0x1, 0x8:
                        operationNamespace = self._NAME["LD VX ST"]
                        operationDataType = self._TYPE["VX KEY"]
                    case 0x1, 0xE:
                        operationNamespace = self._NAME["LD VX ST"]
                        operationDataType = self._TYPE["VX KEY"]
                    case 0x2, 0x9:
                            operationNamespace = self._NAME["LD F VX"]
                            operationDataType = self._TYPE["VX KEY"]
                    case 0x5, 0x5:
                            operationNamespace = self._NAME["LD I VX"]
                            operationDataType = self._TYPE["VX KEY"]
                    case 0x6, 0x5:
                            operationNamespace = self._NAME["LD VX I"]
                            operationDataType = self._TYPE["VX KEY"]
        return operationData, operationDataType, operationNamespace


    def do(self, instruction):
        """Do the instruction given on the instance of the VM
        Takes an expected 16 bit Little Endian (LE) number
        Returns values if optional kwargs are set
        """
        # Specify the instruction type
        operationData, operationDataType, operationNamespace = self.returnInstruction(instruction)
        match operationDataType:
            case 2: #VX, BYTE -- all instructions that use VX, BYTE addressing ?xkk
                vx = (operationData >> 4) >> 4 #vx register
                nnByte = 0x00FF & operationData #nnbyte, made from two nibbles at the end
                match operationNamespace:
                    case 10: #LD VX BYTE
                        ###############
                        # LD VX BYTE  #
                        ###############
                        # Transfers the immediate byte KK
                        # to the register VX
                        self.vRegisters[vx] = nnByte
                        if self.debug: print(f"DEBUG: Setting V{vx} <- {self.vRegisters[vx]}")
                    case 11: #ADD VX BYTE
                        ###############
                        # ADD VX BYTE  #
                        ###############
                        # Adds byte KK and Vx and outputs it
                        # to the register VX
                        self.vRegisters[vx] = (nnByte + self.vRegisters[vx]) & 0xFF #adds wrap
                        if self.debug: print(f"DEBUG: Setting V{vx} <- {self.vRegisters[vx]}")
                    case 6: #SE VX BYTE
                        ###############
                        # SE VX BYTE  #
                        ###############
                        # Skip next instruction if the value in vx == kk
                        vxisByte = True if vx == nnByte else False
                        if vxisByte:
                            self.PC += 2 #skips by an extra 2
                        if self.debug and vxisByte: print(f"DEBUG: Skipping next instruction -> V{vx} is {self.vRegisters[vx]} == {nnByte}")
                        if self.debug and not vxisByte: print(f"DEBUG: No skip -> V{vx} is {self.vRegisters[vx]} != {nnByte}")
                    case 7: #SNE VX BYTE
                        ###############
                        # SNE VX BYTE  #
                        ###############
                        # Skip next instruction if the value in vx != kk
                        vxisByte = True if vx == nnByte else False
                        if not vxisByte:
                            self.PC += 2 #skips by an extra 2
                        if self.debug and not vxisByte: print(f"DEBUG: Skipping next instruction -> V{vx} is {self.vRegisters[vx]} != {nnByte}")
                        if self.debug and vxisByte: print(f"DEBUG: No skip -> V{vx} is {self.vRegisters[vx]} == {nnByte}")
        self.PC += 2
    def test(self):
        ...
