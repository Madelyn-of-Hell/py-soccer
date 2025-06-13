import enum
import random
import time
def Attack():
    t=0
    while True:
        t+=1
        print('a'*(t))
        time.sleep(1)
def Defense():
    t=0
    while True:
        t+=1
        print('d'*(t))
        time.sleep(1)
def Interference():
    t=0
    while True:
        t+=1
        print('i'*(t))
        time.sleep(1)

class Protocol(enum.Enum):
    Defense = (Defense,)
    Attack = (Attack,)
    Interference = (Interference,)

def protocol_selector() -> Protocol:
    """TODO"""
    return random.choice([Protocol.Attack, Protocol.Defense, Protocol.Attack])

if __name__ == "__main__":
    while True:
        print(protocol_selector())