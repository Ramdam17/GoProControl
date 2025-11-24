"""
Debug script to check available settings on GoPro Hero 12 Black
"""

from gopro_usb import GoProUSB
import json

SN = "C3504224682139"  # SN3 from example_usage.py
gopro = GoProUSB(SN)

print("🔍 Checking GoPro Hero 12 Black settings...\n")

try:
    gopro.power_on()
    
    print("✅ External control enabled\n")
    
    # Get current state
    state = gopro.get_state()
    
    print("=" * 60)
    print("CURRENT SETTINGS")
    print("=" * 60)
    
    # Display all settings
    if 'settings' in state:
        print("\n📊 Available settings:")
        for setting_id, value in sorted(state['settings'].items()):
            print(f"  Setting {setting_id}: {value}")
    
    print("\n" + "=" * 60)
    print("STATUS INFO")
    print("=" * 60)
    
    # Display status
    if 'status' in state:
        print(f"\n🔋 Battery: {state['status'].get('70', 'N/A')}%")
        print(f"📹 Recording: {'YES' if state['status'].get('10', 0) == 1 else 'NO'}")
        print(f"⚙️  Mode: {gopro._get_mode_name(state['status'].get('43', 0))}")
        print(f"💾 SD free: {state['status'].get('54', 'N/A')} MB")
    
    # Try to identify resolution setting
    print("\n" + "=" * 60)
    print("TESTING RESOLUTIONS")
    print("=" * 60)
    
    # Test different resolution options for Hero 12
    resolutions_to_test = [
        (1, "4K"),
        (24, "5K"),
        (27, "5.3K (Hero 12)"),
        (100, "5.3K (option 100)"),
    ]
    
    print("\nTesting which resolution options work:\n")
    for option, name in resolutions_to_test:
        try:
            import requests
            url = f"{gopro.base_url}/gopro/camera/setting?setting=2&option={option}"
            response = gopro.session.get(url, timeout=2)
            if response.status_code == 200:
                print(f"✅ {name} (option={option}) - WORKS")
            else:
                print(f"❌ {name} (option={option}) - Error {response.status_code}")
        except Exception as e:
            print(f"❌ {name} (option={option}) - {str(e)[:50]}")
    
    print("\n" + "=" * 60)
    print("TESTING FPS")
    print("=" * 60)
    
    # Test FPS options
    fps_to_test = [
        (0, "240 FPS"),
        (1, "120 FPS"),
        (5, "60 FPS"),
        (8, "30 FPS"),
        (10, "24 FPS"),
    ]
    
    print("\nTesting which FPS options work:\n")
    for option, name in fps_to_test:
        try:
            url = f"{gopro.base_url}/gopro/camera/setting?setting=3&option={option}"
            response = gopro.session.get(url, timeout=2)
            if response.status_code == 200:
                print(f"✅ {name} (option={option}) - WORKS")
            else:
                print(f"❌ {name} (option={option}) - Error {response.status_code}")
        except Exception as e:
            print(f"❌ {name} (option={option}) - {str(e)[:50]}")
    
    # Save full state to file for analysis
    with open('gopro_full_state.json', 'w') as f:
        json.dump(state, f, indent=2)
    print(f"\n💾 Full state saved to: gopro_full_state.json")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
