import minimalmodbus
import time

def setuprs485( id ):
	rs485 = minimalmodbus.Instrument('/dev/ttyAMA0', id , mode='rtu')
	rs485.debug = True
	rs485.CLOSE_PORT_AFTER_EACH_CALL = True
	rs485.serial.baudrate = 2400   # Baud
	rs485.serial.bytesize = 8
	rs485.serial.parity   = minimalmodbus.serial.PARITY_NONE
	rs485.serial.stopbits = 1
	rs485.serial.timeout  = 1   # seconds
	return rs485

def readcurr( idslave ):
	rs485 = setuprs485(idslave)
	curr = rs485.read_float(6, functioncode=4, numberOfRegisters=2)
	time.sleep(1)
	return curr

def readenergy( idslave ):
	rs485 = setuprs485(idslave)
	totalace = rs485.read_float(342, functioncode=4, numberOfRegisters=2)
	time.sleep(1)
	return totalace


# --------------------- Readable value Power Analyser --------------------------#
# voltage = rs485.read_float(0, functioncode=4, numberOfRegisters=2)
# current = rs485.read_float(6, functioncode=4, numberOfRegisters=2)
# activepower = rs485.read_float(12, functioncode=4, numberOfRegisters=2)
# apparentpower = rs485.read_float(18, functioncode=4, numberOfRegisters=2)
# reactivepower = rs485.read_float(24, functioncode=4, numberOfRegisters=2)
# powerfactor = rs485.read_float(30, functioncode=4, numberOfRegisters=2)
# readct = rs485.read_float(50, functioncode=3, numberOfRegisters=2)
# frequency = rs485.read_float(70, functioncode=4, numberOfRegisters=2)
# importactiveeenergy = rs485.read_float(72, functioncode=4, numberOfRegisters=2)
# exportactiveenergy = rs485.read_float(74, functioncode=4, numberOfRegisters=2)
# importreactiveeenergy = rs485.read_float(76, functioncode=4, numberOfRegisters=2)
# exportreactiveenergy = rs485.read_float(78, functioncode=4, numberOfRegisters=2)
# totalactiveenergy = rs485.read_float(342, functioncode=4, numberOfRegisters=2)
# totalreactiveenergy = rs485.read_float(344, functioncode=4, numberOfRegisters=2)
