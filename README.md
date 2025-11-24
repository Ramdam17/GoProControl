# GoPro USB Control

Control GoPro cameras via USB in Python.

## Installation

```bash
# With Poetry
poetry install

# Or with pip
pip install -e .
```

## Usage

### Quick Example

```python
from gopro_usb import GoProUSB

# Initialize with your GoPro serial number
gopro = GoProUSB("C1234567890")

# Power on the camera
gopro.power_on()

# Configure settings
gopro.mode_video()
gopro.set_resolution_5_3k()
gopro.set_fps_240()
gopro.set_lens_linear()

# Record
gopro.record_start()
time.sleep(10)  # Record for 10 seconds
gopro.record_stop()

# Power off
gopro.power_off()
```

### Complete Example

See `example_usage.py` for a complete demonstration including:
- Power on / Power off
- Configuration (5.3K resolution, 240 FPS, Linear Lens)
- Start/stop recording
- Real-time status monitoring

```bash
# Run the example
poetry run python example_usage.py

# Or activate the virtual environment
poetry shell
python example_usage.py
```

## Main Features

### Basic Control
- `power_on()` - Power on the camera
- `power_off()` - Power off the camera
- `record_start()` - Start recording
- `record_stop()` - Stop recording

### Video Configuration
- `set_resolution_5_3k()` - 5.3K resolution
- `set_resolution_5k()` - 5K resolution
- `set_resolution_4k()` - 4K resolution
- `set_resolution_2_7k()` - 2.7K resolution
- `set_resolution_1080()` - 1080p resolution

### FPS Configuration
- `set_fps_240()` - 240 FPS
- `set_fps_200()` - 200 FPS
- `set_fps_120()` - 120 FPS
- `set_fps_60()` - 60 FPS
- `set_fps_30()` - 30 FPS
- `set_fps_24()` - 24 FPS

### Lens Configuration
- `set_lens_linear()` - Linear (recommended for less distortion)
- `set_lens_wide()` - Wide
- `set_lens_narrow()` - Narrow
- `set_lens_superview()` - SuperView
- `set_lens_max_superview()` - Max SuperView
- `set_lens_linear_horizon()` - Linear + Horizon Lock

### Status
- `get_state()` - Get complete state
- `get_status_realtime(interval, duration)` - Real-time monitoring
- `is_busy()` - Check if camera is busy
- `is_encoding()` - Check if encoding is in progress

### Modes
- `mode_video()` - Video mode
- `mode_photo()` - Photo mode
- `mode_timelapse()` - Timelapse mode

### Media
- `get_media_list()` - List files on SD card
- `download_last_media(filename)` - Download last file

## Network Configuration

The class uses the GoPro's IP address based on its serial number:
- IP Format: `172.2{digit3}.1{digit2-3}.51`
- Example: SN "C1234567890" → IP `172.29.190.51`

Make sure that:
1. The GoPro is connected via USB
2. USB control is enabled on the camera
3. Your computer can communicate with the GoPro's IP

## Credits

Based on [goproUSB](https://github.com/drukasz/goproUSB) by Lukasz J. Nowak.

Modifications and additions:
- Complete refactoring into Python class
- OpenCV support for local preview
- Configuration for GoPro Hero 12 Black
- Real-time monitoring support
- Media download support

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

As a derivative of [goproUSB](https://github.com/drukasz/goproUSB), this project complies with the GPL v3.0 terms which require that any modification or derivative work must also be distributed under GPL v3.0.
