from qrcode_scanner import HIDScanner
from qrcode_scanner.exceptions import (
    DeviceConnectionError,
    DeviceNotFoundError,
    DeviceReadError,
)

# Connect to a specific device (USB Keyboard)
vendor_id = 0x1D82  # Replace with your device's vendor ID
product_id = 0x5CA0  # Replace with your device's product ID


try:
    # Open the HID device
    scanner = HIDScanner(vendor_id, product_id)

    scanner.connect()
    print("Connected to device")
    print("Manufacturer:", scanner.device.get_manufacturer_string())  # type: ignore
    print("Product:", scanner.device.get_product_string())  # type: ignore

    while True:
        try:
            print("Listening for scans...")
            # Read data from the scanner
            scanned_text = scanner.read()  # the read function is blocking
            if scanned_text:
                print("=== SCAN COMPLETE ===")
                print("Scanned text:", scanned_text)
        except DeviceNotFoundError:
            print("Device not found or not connected")
            break
        except DeviceReadError as e:
            print(f"Device read error: {e}")
            break
        except DeviceConnectionError as e:
            print(f"Device connection error: {e}")
            break

except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    scanner.close()
    print("HID device closed")
