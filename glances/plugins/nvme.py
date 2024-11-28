import subprocess
import shutil

class PluginNVMe:
    """
    A plugin to retrieve NVMe information using the nvme-cli tool.
    """

    def is_nvme_cli_available(self):
        """
        Check if the 'nvme' command is available on the system.
        """
        if shutil.which("nvme") is None:
            return False
        return True

    def list_nvme_devices(self):
        """
        List all available NVMe devices using the 'nvme list' command.
        """
        if not self.is_nvme_cli_available():
            return "Error: 'nvme' command not found. Ensure 'nvme-cli' is installed."

        devices = []
        try:
            result = subprocess.run(['nvme', 'list'], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Error: Unable to retrieve NVMe device list. {result.stderr}"

            for line in result.stdout.splitlines():
                if "/dev/nvme" in line:
                    device = line.split()[0]  # Extract the device name
                    devices.append(device)

        except Exception as e:
            return f"Unexpected error while listing NVMe devices: {e}"

        return devices

    def get_nvme_data(self):
        """
        Retrieve SMART data for each NVMe device.
        """
        devices = self.list_nvme_devices()
        if isinstance(devices, str):  # Error message
            return {"error": devices}

        nvme_data = {}
        for device in devices:
            try:
                result = subprocess.run(['nvme', 'smart-log', device], capture_output=True, text=True)
                if result.returncode == 0:
                    nvme_data[device] = result.stdout.strip()
                else:
                    nvme_data[device] = f"Error retrieving data: {result.stderr.strip()}"
            except Exception as e:
                nvme_data[device] = f"Error: {e}"

        return nvme_data
