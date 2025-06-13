from protocols import Protocol
import protocols
import time
import multiprocessing
def main():
    current_protocol:Protocol = None
    while True:
        new_protocol:Protocol = protocols.protocol_selector()
        if new_protocol == current_protocol:
            print("Protocol Not Updated")
        else:
            kids = bool(multiprocessing.active_children())
            for active_child in multiprocessing.active_children():
                active_child.terminate()
            if kids: print("Children Terminated")

            current_protocol = new_protocol
            multiprocessing.Process(target=new_protocol.value[0]).start()
            print(f"Protocol {new_protocol.name} Started")
        time.sleep(1)

if __name__ == "__main__":
    main()