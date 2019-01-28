from threading import Thread
from serial import Serial, SerialTimeoutException, SerialException
from time import sleep
from res.parser import get_formatted_data


class Server:

    def __init__(self):

        # Initialise a list of clients to remember
        self._clients = dict()

        # Create a list of ports to connect to, first one for LED data, second one for motors data
        self._ports = ["/dev/ttyACM0", "/dev/ttyACM1"]

        # Initialise how much time to wait before attempting to reconnect
        self._RECONNECT_DELAY = 3

        # Iterate over a string with client ports
        for port in self._ports:

            try:
                # Create an instance of the Client and store it
                self._clients[port] = Client(port)
                print("Connected to {0}.".format(port))

            except SerialException:
                print("Failed to connect to {0}".format(port))

        # Change the delay of the second client to 1 sek (to avoid stalling of all motors)
        self._clients[self._ports[1]]._COMMUNICATION_DELAY = 1

        # Run the server
        Thread(target=self._listen).start()
        Thread(target=self._update_data).start()

    def _listen(self):

        # An infinite loop to keep sending the data
        while True:

            # Iterate over all connections
            for port in self._ports:

                # Check if either port wasn't assigned or the client is dead
                if port not in self._clients or not self._clients[port].thread:

                    # Wait 3 seconds to avoid flooding stdio
                    sleep(self._RECONNECT_DELAY)
                    print("Resetting connection to {0}.".format(port))

                    try:
                        # Create an instance of the Client and store it
                        self._clients[port] = Client(port)
                        print("Connected to {0}.".format(port))

                    except SerialException:
                        print("Failed to connect to {0}".format(port))

    def set_data(self, port, data):

        try:
            # Set new data to the client
            self._clients[port].data = data

        except KeyError:
            pass

    def _update_data(self):

        # Read the data to send to Teensy
        strings = get_formatted_data()

        # Keep running
        while True:

            # Iterate over each line
            for data in strings:

                # Split the data for different low-level components
                led_data, motors_data = ",".join(x for x in data.split(",")[:3]),\
                                        ",".join(x for x in data.split(",")[3:])

                # Set the data for LEDs
                self.set_data(self._ports[0], data=led_data)

                # Set the data for motors
                self.set_data(self._ports[1], data=motors_data)


class Client:

    def __init__(self, port):

        # Create a new serial object
        self._serial = Serial(port)

        # Initialise a data storage
        self._data = None

        # Initialise data delay
        self._COMMUNICATION_DELAY = 0.01

        # Assign a new thread to the serial object
        self._thread = Thread(target=self.run)
        self._thread.start()

    @property
    def thread(self):
        return self._thread.is_alive()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    def run(self):

        # Run an infinite loop to keep exchanging data
        while True:

            try:
                # Check if data is valid
                if self.data:

                    # Send the data
                    sleep(self._COMMUNICATION_DELAY)
                    print("Sending: {0}".format(self.data))
                    self._serial.write(bytes(self.data, encoding="UTF-8"))

            except SerialTimeoutException:
                # Inform that the connection has timed out
                print("Connection to {0} timed out. Closing the connection".format(self._serial.port))
                self._serial.close()

            except SerialException:
                # Inform that the connection was lost
                print("Connection to {0} lost. Closing the connection".format(self._serial.port))
                self._serial.close()

            # Ignore None-s
            except TypeError:
                pass


if __name__ == "__main__":
    s = Server()
