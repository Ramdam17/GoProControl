"""
Test changing presets on Hero 12 Black instead of individual settings
"""

from gopro_usb import GoProUSB
import time

SN = "C3504224682139"
gopro = GoProUSB(SN)

print("🔍 Testing preset changes on Hero 12 Black\n")

gopro.power_on()
time.sleep(1)

# Get current state
state = gopro.get_state()
print(f"📊 Current resolution: {state['settings'].get('2', 'N/A')}")
print(f"🎬 Current FPS: {state['settings'].get('3', 'N/A')}")
print(f"🔍 Current lens: {state['settings'].get('121', 'N/A')}\n")

print("="*60)
print("Testing different presets:")
print("="*60)

# Try different video presets
presets = [
    (0, "Standard"),
    (1, "Activity"),
    (2, "Cinematic"),
    (3, "Slo-Mo"),  # Might be slow motion
    (4, "Ultra Slo-Mo"),
    (5, "Basic"),
]

for preset_id, name in presets:
    print(f"\n🎬 Trying preset {preset_id}: {name}")
    try:
        url = f"{gopro.base_url}/gopro/camera/presets/load?id={preset_id}"
        response = gopro.session.get(url, timeout=3)
        if response.status_code == 200:
            print(f"   ✅ Preset loaded successfully")
            time.sleep(1)
            
            # Check what changed
            state = gopro.get_state()
            res = state['settings'].get('2', 'N/A')
            fps = state['settings'].get('3', 'N/A')
            lens = state['settings'].get('121', 'N/A')
            print(f"   📊 Resolution: {gopro._get_resolution_name(res)}")
            print(f"   🎬 FPS: {gopro._get_fps_name(fps)}")
            print(f"   🔍 Lens: {gopro._get_lens_name(lens)}")
        else:
            print(f"   ❌ Error {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")
    time.sleep(0.5)

print("\n" + "="*60)
print("Final state:")
print("="*60)
state = gopro.get_state()
print(f"📊 Resolution: {gopro._get_resolution_name(state['settings'].get('2', 'N/A'))}")
print(f"🎬 FPS: {gopro._get_fps_name(state['settings'].get('3', 'N/A'))}")
print(f"🔍 Lens: {gopro._get_lens_name(state['settings'].get('121', 'N/A'))}")
