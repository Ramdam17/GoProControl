"""
Retest resolution changes with proper delays
"""

from gopro_usb import GoProUSB
import time

SN = "C3504224682139"
gopro = GoProUSB(SN)

print("🔍 Retesting resolution changes on Hero 12 Black\n")

gopro.power_on()
time.sleep(2)

# Get initial state
state = gopro.get_state()
print(f"📊 Initial Resolution: {gopro._get_resolution_name(state['settings'].get('2', 'N/A'))} (id={state['settings'].get('2')})")
print(f"🎬 Initial FPS: {gopro._get_fps_name(state['settings'].get('3', 'N/A'))} (id={state['settings'].get('3')})")
print(f"🔍 Initial Lens: {gopro._get_lens_name(state['settings'].get('121', 'N/A'))} (id={state['settings'].get('121')})\n")

print("="*60)
print("Test 1: Try changing to 5.3K (option 27)")
print("="*60)

try:
    url = f"{gopro.base_url}/gopro/camera/setting?setting=2&option=27"
    print(f"URL: {url}")
    response = gopro.session.get(url, timeout=5)
    print(f"Response: {response.status_code}")
    if response.status_code == 200:
        print("✅ Request successful")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
    
    time.sleep(1)
    state = gopro.get_state()
    new_res = state['settings'].get('2', 'N/A')
    print(f"📊 New Resolution: {gopro._get_resolution_name(new_res)} (id={new_res})\n")
except Exception as e:
    print(f"❌ Exception: {e}\n")

print("="*60)
print("Test 2: Try other common resolution options")
print("="*60)

common_options = [
    (1, "4K"),
    (4, "2.7K"),
    (9, "1080p"),
    (24, "5K"),
    (26, "5.3K (alt)"),
    (27, "5.3K (Hero 12)"),
]

for option, name in common_options:
    try:
        url = f"{gopro.base_url}/gopro/camera/setting?setting=2&option={option}"
        response = gopro.session.get(url, timeout=3)
        status = "✅" if response.status_code == 200 else f"❌ ({response.status_code})"
        print(f"{status} Option {option:2d} - {name}")
        if response.status_code == 200:
            time.sleep(0.5)
    except Exception as e:
        print(f"❌ Option {option:2d} - {name} - Error: {str(e)[:40]}")

print("\n" + "="*60)
print("Test 3: Check if resolution changed")
print("="*60)
state = gopro.get_state()
final_res = state['settings'].get('2', 'N/A')
print(f"📊 Final Resolution: {gopro._get_resolution_name(final_res)} (id={final_res})")
print(f"🎬 Final FPS: {gopro._get_fps_name(state['settings'].get('3', 'N/A'))} (id={state['settings'].get('3')})")
print(f"🔍 Final Lens: {gopro._get_lens_name(state['settings'].get('121', 'N/A'))} (id={state['settings'].get('121')})")
