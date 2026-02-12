##################################
# CHIP 8 EMULATOR -- PYTHON 3.10 #
# MADE BY LUCAS FRIAS @ FEB 2026 #
# 	MIT LICENSE 2.0          #
##################################

#### IMPORTS
## LOCAL IMPORTS
import chip8 #my local instruction emulator
import interfacer #communicates between pygame
## EXTERNAL IMPORTS
import sys
import pygame


#### VARIABLES
devMode = True #enables a testing mode of every functio

if __name__ == "__main__":
	print("Welcome to Chip8Py")
	c8 = chip8.Chip8()
	if devMode:
		print("Instruction test mode....")
		instructions = [0x7A12, 0x3A12]
		print(len(instructions))
		for instruction in instructions:
			print("Cool")
			c8.do(instruction)
