# QR Code Scanner

A Python library for reading QR codes from both HID (Human Interface Device) scanners and Serial devices. This library supports multiple connection types to accommodate different QR code scanner configurations.

## Features

- **HID Support**: Treats QR code scanners as keyboard input devices and decodes their scanned data
- **Serial Support**: Direct serial communication for devices that output raw text data
- Support for multiple keyboard layouts (HID mode)
- Automatic character decoding
- Robust error handling
- Non-blocking and blocking read operations
- Device discovery utilities

## Installation

Install using pip:

```bash
pip install qrcode-scanner
```

Or using Poetry:

```bash
poetry add qrcode-scanner
```

## Requirements

- Python 3.10+
- hidapi (for HID devices)
- pyserial (for Serial devices)

## Quick Start

### HID Scanner Usage

```python
from qrcode_scanner import HIDScanner
from qrcode_scanner.exceptions import DeviceConnectionError, DeviceNotFoundError, DeviceReadError

# Replace with your device's vendor ID and product ID
VENDOR_ID = 0x1D82
PRODUCT_ID = 0x5CA0

try:
    # Initialize and connect to the scanner
    scanner = HIDScanner(vendor_id=VENDOR_ID, product_id=PRODUCT_ID)
    scanner.connect()

    print("Connected to device")
    print("Manufacturer:", scanner.device.get_manufacturer_string())
    print("Product:", scanner.device.get_product_string())

    # Start reading QR codes
    while True:
        try:
            print("Listening for scans...")
            scanned_text = scanner.read()  # Blocking read operation
            if scanned_text:
                print("=== SCAN COMPLETE ===")
                print("Scanned text:", scanned_text)
        except DeviceNotFoundError:
            print("Device not found or not connected")
            break
        except (DeviceReadError, DeviceConnectionError) as e:
            print(f"Device error: {e}")
            break

except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    scanner.close()
    print("HID device closed")
```

### Serial Scanner Usage

```python
from qrcode_scanner import SerialScanner, serial_ports
from qrcode_scanner.exceptions import DeviceConnectionError, DeviceNotConnectedError

# List available serial ports
print("Available serial ports:")
ports = serial_ports()
for port in ports:
    print(f"  - {port}")

# Configure the serial connection
port = "/dev/ttyACM0"  # Adjust for your system (Windows: "COM3", etc.)
baudrate = 9600

try:
    # Create and connect to the serial scanner
    scanner = SerialScanner(
        port=port,
        baudrate=baudrate,
        timeout=1  # timeout in seconds
    )

    scanner.connect()
    print(f"Connected to serial device on {port}")

    while True:
        print("Waiting for data...")
        try:
            # Read data from the scanner (blocking call)
            scanned_text = scanner.read()
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
finally:
    scanner.close()
    print("Serial device closed")
```

## Serial Scanner Configuration

The `SerialScanner` class supports various configuration options:

```python
scanner = SerialScanner(
    port="/dev/ttyACM0",  # Serial port
    baudrate=9600,        # Baud rate (default: 9600)
    parity=serial.PARITY_NONE,    # Parity (default: NONE)
    stopbits=serial.STOPBITS_ONE, # Stop bits (default: 1)
    bytesize=serial.EIGHTBITS,    # Byte size (default: 8)
    timeout=1             # Read timeout in seconds (default: 1)
)
```

Common baud rates for QR scanners: 9600, 19200, 38400, 115200

## Error Handling

The library includes several exception classes to handle different error scenarios:

- `DeviceNotFoundError`: When the specified device cannot be found
- `DeviceConnectionError`: When there are issues connecting to the device
- `DeviceNotConnectedError`: When trying to read from a disconnected device
- `DeviceReadError`: When reading from the device fails
- `UnknownCharacterError`: When encountering unknown character codes (HID only)

## Device Discovery

### Finding HID Device IDs

To find your HID device's vendor and product IDs:

```python
from qrcode_scanner import devices

# List all connected HID devices
for device in devices():
    print(f"Vendor ID: 0x{device['vendor_id']:04X}")
    print(f"Product ID: 0x{device['product_id']:04X}")
    print(f"Product Name: {device.get('product_string', 'N/A')}")
    print("---")
```

### Finding Serial Ports

To discover available serial ports:

```python
from qrcode_scanner import serial_ports

# List all available serial ports
ports = serial_ports()
for port in ports:
    print(f"Available port: {port}")
```

## Choosing Between HID and Serial

**Use HID Scanner when:**

- Your QR scanner emulates a keyboard
- Scanner appears as an HID device in your system
- You need to decode keyboard scan codes

**Use Serial Scanner when:**

- Your QR scanner outputs raw text data over serial
- Scanner connects via USB-to-Serial adapter
- Device sends complete text strings followed by newline characters
- You want simpler, more direct communication

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
