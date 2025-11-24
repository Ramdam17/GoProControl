"""
Test which resolution options are actually available on Hero 12 Black
"""

from gopro_usb import GoProUSB
import time

SN = "C3504224682139"  # SN3 from example_usage.py
gopro = GoProUSB(SN)

print("🔍 Testing available resolution options on Hero 12 Black\n")

gopro.power_on()
time.sleep(1)

# Current setting
state = gopro.get_state()
current_res = state['settings'].get('2', 'N/A')
current_fps = state['settings'].get('3', 'N/A')
print(f"📊 Current resolution setting: {current_res}")
print(f"🎬 Current FPS setting: {current_fps}\n")

# Test a wide range of resolution options
print("Testing resolution options (setting=2):\n")
for option in range(0, 50):
    try:
        url = f"{gopro.base_url}/gopro/camera/setting?setting=2&option={option}"
        response = gopro.session.get(url, timeout=2)
        if response.status_code == 200:
            print(f"✅ Option {option:2d} - WORKS")
            time.sleep(0.3)
        elif response.status_code == 403:
            print(f"🚫 Option {option:2d} - Forbidden (incompatible with current settings)")
        else:
            print(f"❌ Option {option:2d} - Error {response.status_code}")
    except Exception as e:
        print(f"❌ Option {option:2d} - {str(e)[:40]}")
    time.sleep(0.1)

print("\n" + "="*60)
print("Testing FPS options (setting=3):\n")
for option in [0, 1, 2, 5, 6, 8, 9, 10, 13]:
    try:
        url = f"{gopro.base_url}/gopro/camera/setting?setting=3&option={option}"
        response = gopro.session.get(url, timeout=2)
        if response.status_code == 200:
            print(f"✅ Option {option:2d} - WORKS")
            time.sleep(0.3)
        elif response.status_code == 403:
            print(f"🚫 Option {option:2d} - Forbidden (incompatible with current settings)")
        else:
            print(f"❌ Option {option:2d} - Error {response.status_code}")
    except Exception as e:
        print(f"❌ Option {option:2d} - {str(e)[:40]}")
    time.sleep(0.1)

# Check final state
print("\n" + "="*60)
state = gopro.get_state()
final_res = state['settings'].get('2', 'N/A')
final_fps = state['settings'].get('3', 'N/A')
print(f"📊 Final resolution setting: {final_res}")
print(f"🎬 Final FPS setting: {final_fps}")
