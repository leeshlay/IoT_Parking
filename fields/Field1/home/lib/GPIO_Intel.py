#!/usr/bin/env python

import time, sys, os

IOPins = {
"IO2":  32,
"IO3":  18,
"IO4":  28,
"IO5":  17,
"IO6":  24,
"IO7":  27,
"IO8":  26,
"IO9":  19,
"IO10": 16,
"IO11": 25,
"IO12": 38,
"IO13": 39,
"A0":   37,
"A1":   36,
"A2":   23,
"A3":   22,
"A4":   29,
"A5":   29
}



PinsEnabled = {
"IO2":  False,
"IO3":  False,
"IO4":  False,
"IO5":  False,
"IO6":  False,
"IO7":  False,
"IO8":  False,
"IO9":  False,
"IO10": False,
"IO11": False,
"IO12": False,
"IO13": False,
"A0":   False,
"A1":   False,
"A2":   False,
"A3":   False,
"A4":   False,
"A5":   False,
}


class Intel:

	def __init__(self):
		print "Initial Setup."
		return

	def cmd(self, value, file):
		with open(file, 'w') as File:
			File.write(str(value))
		return

	def setup(self, pin, dir='out'):
		if pin[:1]=="A":
			actpin = IOPins[pin]
			try:
				self.cmd(actpin, '/sys/class/gpio/export')
			except  IOError as e:
				print "Pin already exported"
			self.cmd("out", '/sys/class/gpio/gpio{}/direction'.format(actpin))
			self.cmd("0", '/sys/class/gpio/gpio{}/value'.format(actpin))
		else:
			actpin = IOPins[pin]
			try:
				self.cmd(actpin, '/sys/class/gpio/export')
			except  IOError as e:
				print "Pin already exported"
			self.cmd(dir, '/sys/class/gpio/gpio{}/direction'.format(actpin))
			PinsEnabled[pin] = True
		return 1

	def output(self, pin, value='1'):
		actpin = IOPins[pin]
		if PinsEnabled[pin]:
			self.pullup(pin)
			self.cmd(value, '/sys/class/gpio/gpio{}/value'.format(actpin))
			return 1
		else:
			print "{} has not been set to output.".format(pin)
			return 0

	def input(self, pin):
		if pin[:1]=="A":
			with open('/sys/bus/iio/devices/iio:device0/in_voltage{}_raw'.format(pin[1:]), 'r') as File:
				return File.readline()[:-1]
		else:
			actpin = IOPins[pin]
			if PinsEnabled[pin]:
				self.pullup(pin, 'pullup')
				with open('/sys/class/gpio/gpio{}/value'.format(actpin), 'r') as File:
					return File.readline()[:-1]

	def pullup(self, pin, drive='strong'):
		actpin = IOPins[pin]
		self.cmd(drive, '/sys/class/gpio/gpio{}/drive'.format(actpin))
		return 1

	def cleanup(self):
		for Pin in Pins:
			if Pin[:2] == 'IO':
				actpin = IOPins[pin]
				self.cmd('0', '/sys/class/gpio/gpio{}/value'.format(actpin))
			elif Pin[:3] == 'PWM':
				actpin = IOPins[pin]
				self.cmd('0', '/sys/class/pwm/pwmchip0/pwm{}/enable'.format(actpin))

	
