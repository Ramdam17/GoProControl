"""
Test basic recording with current settings on Hero 12 Black
"""

from gopro_usb import GoProUSB
import time

SN = "C3504224682139"
gopro = GoProUSB(SN)

print("🔍 Testing basic recording on Hero 12 Black\n")

gopro.power_on()
time.sleep(1)

# Check current settings
state = gopro.get_state()
print(f"📊 Current Resolution: {gopro._get_resolution_name(state['settings'].get('2', 'N/A'))}")
print(f"🎬 Current FPS: {gopro._get_fps_name(state['settings'].get('3', 'N/A'))}")
print(f"🔍 Current Lens: {gopro._get_lens_name(state['settings'].get('121', 'N/A'))}")
print(f"🔋 Battery: {state['status'].get('70', 'N/A')}%")
print(f"💾 SD free: {state['status'].get('54', 'N/A')} MB\n")

print("="*60)
print("Testing recording with current settings")
print("="*60)

# Try to record for 5 seconds
print("\n🔴 Starting recording...")
if gopro.record_start():
    print("✅ Recording started successfully!\n")
    
    # Monitor for 5 seconds
    for i in range(5):
        time.sleep(1)
        state = gopro.get_state()
        is_recording = state['status'].get('10', 0) == 1
        print(f"   ⏱️  {i+1}s - Recording: {'YES' if is_recording else 'NO'}")
    
    print("\n⏹️  Stopping recording...")
    if gopro.record_stop():
        print("✅ Recording stopped successfully!\n")
    else:
        print("❌ Failed to stop recording\n")
else:
    print("❌ Failed to start recording\n")

print("="*60)
print("✅ Basic recording test complete")
print("="*60)
