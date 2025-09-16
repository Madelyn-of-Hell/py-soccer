from pybricks.hubs import PrimeHub
from bleradio.bleradio import BLERadio
channels = {
    'Bricked down': {
        'broadcast': 20,
        'observe': 21
    },
    'Bricked up':   {
        'broadcast': 21,
        'observe': 20
    }
}

hub = PrimeHub()
channel_pair = channels[hub.system.info()['name']]
radio = BLERadio(channel_pair['broadcast'], [channel_pair['observe']])

old_data = None

while True:

    new_data = radio.observe(channel_pair['observe'])
    strength = radio.signal_strength(channel_pair['observe'])

    if new_data == old_data:
        continue

    processed_data = new_data + 1
    old_data = processed_data
    print(processed_data)
    radio.broadcast(processed_data)
