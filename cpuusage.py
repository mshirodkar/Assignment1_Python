import subprocess
import time
import sys

threshold = 80  # CPU usage threshold

print("Monitoring CPU usage...\n(Press Ctrl+C to stop)\n")

try:
    while True:
        # Run typeperf command to get CPU usage
        output = subprocess.check_output(
            ['typeperf', r'\Processor(_Total)\% Processor Time', '-sc', '1'],
            stderr=subprocess.DEVNULL
        ).decode(errors='ignore')

        lines = output.strip().splitlines()

        # Skip lines that don't contain actual CPU data
        for line in lines:
            if '%' in line:
                try:
                    usage_str = line.split(',')[1].strip().replace('"', '')
                    usage = float(usage_str)
                    if usage > threshold:
                        print(f"Alert! CPU usage exceeds threshold: {usage:.2f}%")
                except ValueError:
                    continue  # Skip lines that can't be converted
                break  # We only care about the first valid line

        time.sleep(1)

except KeyboardInterrupt:
    print("\nMonitoring stopped by user.")
    sys.exit(0)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
