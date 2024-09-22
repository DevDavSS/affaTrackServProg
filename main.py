from state import programState, activation_interface
import interfaces
import sys


def main():

    state = programState()
    state_msg = state.verifyState()
    if state_msg == "011000010011100100100111001010010011":
        mainWind = interfaces.mainInterface()
        mainWind.run_main_interface()
    elif state_msg == "10001101000110010011001010010010010001100110100111":
        sys.exit()
    elif state_msg == "0100010010101110100110100101010100100000100100001000100010000111111001001001001001011":

        activation_window = activation_interface()
        activation_window.run_activation_interface()
    else:
        sys.exit()
    

if __name__ == "__main__":
    main()