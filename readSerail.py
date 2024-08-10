import serial
import time
import re
import json

def list_serial_ports():
    """List available serial ports."""
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def parse_data(data_string):
    """Parse the data string into a dictionary."""
    # Define the regex pattern for extracting key-value pairs
    pattern = r"(\w+): ([\d.-]+)"
    
    # Find all matches in the data string
    matches = re.findall(pattern, data_string)
    
    # Convert matches to a dictionary
    data_dict = {key: float(value) if '.' in value or 'e' in value else int(value) for key, value in matches}
    
    return data_dict

def main():
    # List available serial ports
    print("Available serial ports:")
    ports = list_serial_ports()
    for i, port in enumerate(ports):
        print(f"{i}: {port}")

    # Prompt user to select a port
    try:
        port_index = int(input("Select a port number: "))
        selected_port = ports[port_index]
    except (ValueError, IndexError):
        print("Invalid selection. Exiting.")
        return

    # Initialize serial communication
    try:
        ser = serial.Serial(selected_port, 9600, timeout=1)  # Adjust baud rate as needed
        print(f"Listening on port {selected_port}...")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return

    try:
        while True:
            if ser.in_waiting > 0:  # Check if there's data waiting
                raw_data = ser.readline().decode('utf-8', errors='replace').strip()  # Read and decode data
                if raw_data:
                    # print(f"Raw data: {raw_data}")  # Print raw data for debugging
                    # Parse and convert to JSON
                    parsed_data = parse_data(raw_data)
                    if parsed_data:  # Only print if there's actual parsed data
                        json_data = json.dumps(parsed_data, indent=4)  # Convert dictionary to JSON
                        print(f"JSON data:\n{json_data}")
                # else:
                    # print("No data available... Waiting for data...")
            time.sleep(0.1)  # Sleep briefly to avoid busy-waiting
    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        ser.close()  # Close the serial port
        print("Serial port closed.")

if __name__ == "__main__":
    main()

'''

Eventid: 128, Spo2: 96.30, Heart: 89, Pres: 123.80, Temp: 37.30, Audio: 84, Xval: 0.20, Yval: 3.00, Zval: -4.60
JSON data:
{
    "Eventid": 156,
    "Spo2": 99.9,
    "Heart": 98,
    "Pres": 110.2,
    "Temp": 36.1,
    "Audio": 75,
    "Xval": 1.2,
    "Yval": -3.7,
    "Zval": -8.8
}
'''