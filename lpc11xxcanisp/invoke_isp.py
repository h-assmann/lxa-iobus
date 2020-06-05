import canopen
from time import sleep
import struct

class CanOpen:
    """Minimal Setup to controll one ethmux"""
    def __init__(self, channel="can0", node_id=1):
        self.node_id = node_id
        self.network = canopen.Network()
        self.network.connect(channel=channel, bustype='socketcan')
        self.node = self.network.add_node(self.node_id)

    def setup(self):
        """Setup one node with a new node_id"""
        """Warning this expects only one CANOpen node on the network!"""
        self.network.lss.send_switch_state_global(self.network.lss.CONFIGURATION_STATE)
        self.network.lss.configure_node_id(1)
        self.network.lss.send_switch_state_global(self.network.lss.WAITING_STATE)

    def invoke_isp(self):
        """set port state"""
        self.node.sdo.download(0x2b07, 0, struct.pack("I", 0x12345678))

def invoke_rom_loader():
    can = CanOpen()
    can.setup()

    try:
        can.invoke_isp()
    except canopen.sdo.exceptions.SdoCommunicationError:
        pass

if __name__ == "__main__":
    invoke_rom_loader()
