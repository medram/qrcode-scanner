from qrcode_scanner import SerialScanner, serial_ports
from qrcode_scanner.exceptions import DeviceConnectionError, DeviceNotConnectedError

# List available serial ports
print("Available serial ports:")
ports = serial_ports()
for port in ports:
    print(f"  - {port}")

if not ports:
    print("No serial ports found!")
    exit(1)

# Configure the serial connection (adjust parameters as needed)
port = "/dev/ttyACM0"  # or '/dev/ttyS0' on Linux, 'COM3' on Windows
baudrate = 9600

try:
    # Create and connect to the serial scanner
    scanner = SerialScanner(
        port=port, baudrate=baudrate, timeout=1  # timeout in seconds
    )

    scanner.connect()
    print(f"Connected to serial device on {port}")

    while True:
        try:
            print("Waiting for data...")
            # Read data from the scanner
            scanned_text = scanner.read()  # the read function is blocking
            if scanned_text:
                print("=== SCAN COMPLETE ===")
                print("Scanned text:", scanned_text)
            else:
                print("No data received (timeout)")
        except DeviceNotConnectedError:
            print("Device not connected")
            break
        except DeviceConnectionError as e:
            print(f"Device connection error: {e}")
            break

except KeyboardInterrupt:
    print("Program terminated by user")
except DeviceConnectionError as e:
    print(f"Failed to connect to serial device: {e}")
    print(f"Make sure the device is connected to {port}")
    print("Available ports:", ports)
finally:
    if "scanner" in locals():
        scanner.close()
        print("Serial device closed")
