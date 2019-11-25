import bluepy.btle as btle
 
p = btle.Peripheral("AA:BB:CC:DD:EE:FF")
s = p.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
c = s.getCharacteristics()[0]
 
c.write(bytes("Hello world\n", "utf-8"))
p.disconnect()
