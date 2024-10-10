
import interfaces
import sys
from tokenMan import collec_mac_ipv4

class defined_state_codes():
    def __init__(self):
        mac_ipv4_collector = collec_mac_ipv4()  
        self.codes = {
            'neutral_state_code':mac_ipv4_collector.get_mac() + "uieg$%^@gfW#%*--*+43=89=#@DG46H7!@$^&",
            'blocked_state_code': mac_ipv4_collector.get_mac() + "-5=56&*(#$4$opn433*/--+!@sf''8*6fgd",
            'activated_state_code':mac_ipv4_collector.get_mac() + "71#$%@#5^%^#&*jhg&jdS$%0-=)7+_=k*/-"
        }


def main():
    from state import programState, activation_interface
    state_codes = defined_state_codes()
    state = programState()
    state_msg = state.verifyState()
    #print(state_msg)
    if state_msg == state_codes.codes['activated_state_code']:
        mainWind = interfaces.mainInterface()
        mainWind.run_main_interface()
    elif state_msg == state_codes.codes['blocked_state_code']:
        sys.exit()
    elif state_msg == state_codes.codes['neutral_state_code']:

        activation_window = activation_interface()
        activation_window.run_activation_interface()
    else:
        sys.exit()
    

if __name__ == "__main__":
    main()