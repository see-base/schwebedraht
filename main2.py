from pygame import mixer
import socket
import os


vfx = { "fail" : ["Pesthoernchen.png"],
                    "start" : [],
                    "ziel" : ["star.png"]
    }
sfx = [] # 0 = fail, 1 = start, 2 = bonus, 3 = ende

#init UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("127.0.0.1", 4444))

#init audio-system
try:
	mixer.init()
	sfx.append(mixer.Sound("medien/fail.wav"))
	sfx.append(mixer.Sound("medien/start.wav"))
	sfx.append(mixer.Sound("medien/bonus.wav"))
	sfx.append(mixer.Sound("medien/end.wav"))


def main():
    while True:
        ID, INT, BAT, F = serial_decoder()

        if F in range(90, 110): # frequenz um 100 khz, mit +-10 khz toleranz
            aktion(1) #uebergibt das segment als zahl
        elif F in range(190, 210):
            aktion(2)
        elif F in range(290, 310):
            aktion(3)
        elif F in range(390, 410):
            aktion(4)
        else:
            aktion(0)

def serial_decoder():
    input_string = input() #ser.readline()
    input_split = input_string.split(";")

    return (int(input_split[0][3:]),
        int(input_split[1][4:]),
        int(input_split[2][4:]),
        int(input_split[3][2:]))

def aktion(segment):
    effekt(segment)

def effekt(segment):
    if segment == 1:
        visueller_effekt(1)
		audio_effekt(1)
    elif segment == 2:
        visueller_effekt(2)
		audio_effekt(2)
    elif segment == 3:
        visueller_effekt(2)
		audio_effekt(2)
    elif segment == 4:
        visueller_effekt(3)
		audio_effekt(3)
    else:
        visueller_effekt(0)
		audio_effekt(0)

def visueller_effekt(vfx_index):
	if vfx_index == 0:
		sock.send(bytes("medien/zoom_exponential:" + str(0), "UTF-8"))
		sock.send(bytes("medien/effekt/bildname:" + str("Pesthoernchen.png"), "UTF-8"))
		sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))
	elif vfx_index == 1:
		sock.send(bytes("medien/ausw:" + str("0"), "UTF-8")) # ausblenden auswertung-node
		sock.send(bytes("medien/punkte/punkte:{} | {}".format(punkte, p_multiplikator), "UTF-8"))
		sock.send(bytes("medien/hintergrund/alpha:" + str("1"), "UTF-8"))
	elif vfx_index == 2:
		sock.send(bytes("medien/zoom_exponential:" + str(1), "UTF-8"))
		sock.send(bytes("medien/effekt/bildname:" + str("star.png"), "UTF-8"))
		sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))
	elif vfx_index == 3:
		sock.send(bytes("medien/punkte/punkte:" + str("Auswertung:"), "UTF-8"))
		sock.send(bytes("medien/hintergrund/alpha:" + str("0"), "UTF-8")) #ausblenden "See-Base"
		sock.send(bytes("medien/ausw:" + str("1"), "UTF-8")) #einblenden auswertung-node

		#sock.send(bytes("medien/auswertung/punkte:" + str(punkte), "UTF-8")) # Gesamtpunkte
		sock.send(bytes("medien/auswertung/zeit:" + str("%.4f" %(zeit - startzeit)), "UTF-8")) # Gesamtzeit
		sock.send(bytes("medien/auswertung/nick:" + str(nick), "UTF-8")) # Unique Nickname

		sock.send(bytes("medien/auswertung/segment1a:" + str("Zeit: %.2f"%(seg1[2])), "UTF-8")) # 1. Segment - Zeit
		sock.send(bytes("medien/auswertung/segment1b:" + str(str(seg1[3]) +" x Berührt"), "UTF-8"))  # 1. Segment - Beruehrungen
		sock.send(bytes("medien/auswertung/segment2a:" + str("Zeit: %.2f"%(seg2[2])), "UTF-8")) # 2. Segment - Zeit
		sock.send(bytes("medien/auswertung/segment2b:" + str(str(seg2[3]) +" x Berührt"), "UTF-8"))  #2. Segment - Beruehrungen
		sock.send(bytes("medien/auswertung/segment3a:" + str("Zeit: %.2f"%(seg3[2])), "UTF-8")) # 3. Segment - Zeit
		sock.send(bytes("medien/auswertung/segment3b:" + str(str(seg3[3]) +" x Berührt"), "UTF-8"))  #3. Segment - Beruehrungen
		sock.send(bytes("medien/auswertung/segment4a:" + str("Zeit: %.2f"%(seg4[2])), "UTF-8")) # 4. Segment - Zeit
		sock.send(bytes("medien/auswertung/segment4b:" + str(str(seg4[3]) +" x Berührt"), "UTF-8"))  #4. Segment - Beruehrungen
		sock.send(bytes("medien/auswertung/segment5a:" + str("Zeit: %.2f"%(seg5[2])), "UTF-8")) # 5. Segment - Zeit
		sock.send(bytes("medien/auswertung/segment5b:" + str(str(seg5[3]) +" x Berührt"), "UTF-8"))  #5. Segment - Beruehrungen

def audio_effekt(sfx_index):
	if len(sfx > 0):
		mixer.Sound.play(sfx[sfx_index])
