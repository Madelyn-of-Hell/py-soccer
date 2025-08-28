# import enum
import sys
# import time
def Attack():
    t=0
    while True:
        t+=1
        print('a'*(t))
        time.sleep(0.5)
def Defense():
    t=0
    while True:
        t+=1
        print('d'*(t))
        time.sleep(0.5)
def Interference():
    t=0
    while True:
        t+=1
        print('i'*(t))
        time.sleep(0.5)

class Protocol():
    Defense = ("Defense",Defense)
    Attack = ("Attack",Attack)
    Interference = ("Interference",Interference)

def protocol_selector() -> Protocol:
    """TODO"""
    return random.choice([Protocol.Attack, Protocol.Defense, Protocol.Interference])

if __name__ == "__main__":
    ls = {"Attack":0, "Defense":0, "Interference":0}
    while True:
        ls[protocol_selector()[0]] += 1
        print(ls)