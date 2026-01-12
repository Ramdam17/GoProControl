"""
Multi-Camera GoPro Control Example
Controls 3 GoPro cameras simultaneously via USB
"""

from gopro_usb import GoProUSB
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# GoPro Serial Numbers
SN1 = "C3504224696431"
SN2 = "C3504224677229"
SN3 = "C3504224682139"

CAMERAS = {
    "Camera 1": SN1,
    "Camera 2": SN2,
    "Camera 3": SN3,
}


def power_on_camera(name: str, gopro: GoProUSB) -> bool:
    """Power on a single camera"""
    try:
        print(f"🔌 [{name}] Powering on...")
        result = gopro.power_on()
        if result:
            print(f"✅ [{name}] Powered on successfully")
        else:
            print(f"❌ [{name}] Failed to power on")
        return result
    except Exception as e:
        print(f"❌ [{name}] Error: {e}")
        return False


def configure_camera(name: str, gopro: GoProUSB) -> bool:
    """Configure a single camera (4K @ 120 FPS, Linear)"""
    try:
        print(f"⚙️  [{name}] Configuring...")
        
        gopro.mode_video()
        time.sleep(1)
        
        gopro.set_resolution_4k()
        time.sleep(1)
        
        gopro.set_fps_120()
        time.sleep(1)
        
        gopro.set_lens_linear()
        time.sleep(1)
        
        # Verify configuration was applied
        state = gopro.get_state()
        actual_fps = gopro._get_fps_name(state['settings'].get('3', 'N/A'))
        actual_res = gopro._get_resolution_name(state['settings'].get('2', 'N/A'))
        actual_lens = gopro._get_lens_name(state['settings'].get('121', 'N/A'))
        
        print(f"✅ [{name}] Configured: {actual_res} @ {actual_fps}, {actual_lens}")
        return True
            
    except Exception as e:
        print(f"❌ [{name}] Configuration error: {e}")
        return False


def start_recording_camera(name: str, gopro: GoProUSB) -> bool:
    """Start recording on a single camera"""
    try:
        print(f"🔴 [{name}] Starting recording...")
        result = gopro.record_start()
        if result:
            print(f"✅ [{name}] Recording started")
        return result
    except Exception as e:
        print(f"❌ [{name}] Recording start error: {e}")
        return False


def stop_recording_camera(name: str, gopro: GoProUSB) -> bool:
    """Stop recording on a single camera"""
    try:
        print(f"⏹️  [{name}] Stopping recording...")
        result = gopro.record_stop()
        if result:
            print(f"✅ [{name}] Recording stopped")
        return result
    except Exception as e:
        print(f"❌ [{name}] Recording stop error: {e}")
        return False


def power_off_camera(name: str, gopro: GoProUSB) -> bool:
    """Power off a single camera"""
    try:
        print(f"🔌 [{name}] Powering off...")
        result = gopro.power_off()
        if result:
            print(f"✅ [{name}] Powered off")
        return result
    except Exception as e:
        print(f"❌ [{name}] Power off error: {e}")
        return False


def get_camera_status(name: str, gopro: GoProUSB) -> dict:
    """Get status of a single camera"""
    try:
        state = gopro.get_state()
        status = {
            "name": name,
            "battery": state['status'].get('70', 'N/A'),
            "free_space": state['status'].get('54', 'N/A'),
            "recording": state['status'].get('8', 0) == 1,
            "resolution": gopro._get_resolution_name(state['settings'].get('2', 'N/A')),
            "fps": gopro._get_fps_name(state['settings'].get('3', 'N/A')),
            "lens": gopro._get_lens_name(state['settings'].get('121', 'N/A')),
        }
        return status
    except Exception as e:
        return {"name": name, "error": str(e)}


def display_all_status(cameras_gopro: dict):
    """Display status for all cameras in a formatted table"""
    print("\n" + "=" * 80)
    print("📊 CAMERA STATUS")
    print("=" * 80)
    print(f"{'Camera':<12} {'Battery':<10} {'Free Space':<12} {'Recording':<12} {'Resolution':<12} {'FPS':<8} {'Lens':<10}")
    print("-" * 80)
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(get_camera_status, name, gopro): name 
                   for name, gopro in cameras_gopro.items()}
        
        statuses = []
        for future in as_completed(futures):
            statuses.append(future.result())
        
        # Sort by camera name
        statuses.sort(key=lambda x: x.get('name', ''))
        
        for status in statuses:
            if 'error' in status:
                print(f"{status['name']:<12} ❌ Error: {status['error']}")
            else:
                rec_icon = "🔴 Yes" if status['recording'] else "⚪ No"
                print(f"{status['name']:<12} {status['battery']}%{'':<6} {status['free_space']} MB{'':<4} {rec_icon:<12} {status['resolution']:<12} {status['fps']:<8} {status['lens']:<10}")
    
    print("=" * 80)


def main():
    print("=" * 80)
    print("🎥 MULTI-CAMERA GOPRO CONTROL")
    print("   Controlling 3 cameras simultaneously")
    print("=" * 80)
    
    # Initialize all cameras
    cameras_gopro = {}
    for name, sn in CAMERAS.items():
        cameras_gopro[name] = GoProUSB(sn)
        print(f"📷 {name}: SN {sn}")
    
    try:
        # 1. POWER ON all cameras simultaneously
        print("\n" + "=" * 80)
        print("📍 STEP 1: Powering on all cameras")
        print("=" * 80)
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(power_on_camera, name, gopro): name 
                       for name, gopro in cameras_gopro.items()}
            for future in as_completed(futures):
                pass  # Results already printed in the function
        
        time.sleep(3)
        
        # 2. CONFIGURE all cameras SEQUENTIALLY (avoid USB conflicts)
        print("\n" + "=" * 80)
        print("📍 STEP 2: Configuring all cameras (4K @ 120 FPS, Linear)")
        print("   ⚠️  Configuring one at a time to avoid USB conflicts")
        print("=" * 80)
        
        for name, gopro in cameras_gopro.items():
            configure_camera(name, gopro)
            time.sleep(2)  # Wait between cameras
        
        time.sleep(2)
        
        # 3. Display initial status
        print("\n" + "=" * 80)
        print("📍 STEP 3: Initial status")
        display_all_status(cameras_gopro)
        
        # 4. START RECORDING on all cameras simultaneously
        print("\n" + "=" * 80)
        print("📍 STEP 4: Starting recording on all cameras")
        print("=" * 80)
        
        # Use barrier to sync start time
        start_time = time.time() + 1  # Start in 1 second
        print(f"⏱️  Synchronized start in 1 second...")
        
        def sync_start_recording(name, gopro, target_time):
            wait_time = target_time - time.time()
            if wait_time > 0:
                time.sleep(wait_time)
            return start_recording_camera(name, gopro)
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(sync_start_recording, name, gopro, start_time): name 
                       for name, gopro in cameras_gopro.items()}
            for future in as_completed(futures):
                pass
        
        # 5. Monitor during recording
        print("\n" + "=" * 80)
        print("📍 STEP 5: Recording in progress (10 seconds)")
        print("=" * 80)
        
        for i in range(5):
            time.sleep(2)
            display_all_status(cameras_gopro)
        
        # 6. STOP RECORDING on all cameras simultaneously
        print("\n" + "=" * 80)
        print("📍 STEP 6: Stopping recording on all cameras")
        print("=" * 80)
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(stop_recording_camera, name, gopro): name 
                       for name, gopro in cameras_gopro.items()}
            for future in as_completed(futures):
                pass
        
        time.sleep(3)
        
        # 7. Final status
        print("\n" + "=" * 80)
        print("📍 STEP 7: Final status")
        display_all_status(cameras_gopro)
        
        # 8. POWER OFF all cameras
        print("\n" + "=" * 80)
        print("📍 STEP 8: Powering off all cameras")
        print("=" * 80)
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(power_off_camera, name, gopro): name 
                       for name, gopro in cameras_gopro.items()}
            for future in as_completed(futures):
                pass
        
        print("\n" + "=" * 80)
        print("✅ MULTI-CAMERA DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  User interruption - stopping all cameras...")
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Stop recording
            futures = [executor.submit(stop_recording_camera, name, gopro) 
                       for name, gopro in cameras_gopro.items()]
            time.sleep(2)
            # Power off
            futures = [executor.submit(power_off_camera, name, gopro) 
                       for name, gopro in cameras_gopro.items()]
        
        print("🛑 All cameras stopped")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Attempting to stop all cameras...")
        
        for name, gopro in cameras_gopro.items():
            try:
                gopro.record_stop()
                gopro.power_off()
            except:
                pass


def demo_continuous_monitoring():
    """
    Continuously monitor all 3 cameras.
    Press Ctrl+C to stop.
    """
    print("🎥 Multi-Camera Continuous Monitoring")
    print("Press Ctrl+C to stop\n")
    
    cameras_gopro = {}
    for name, sn in CAMERAS.items():
        cameras_gopro[name] = GoProUSB(sn)
    
    try:
        # Power on all
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(power_on_camera, name, gopro) 
                       for name, gopro in cameras_gopro.items()]
        
        time.sleep(3)
        
        # Continuous monitoring
        while True:
            display_all_status(cameras_gopro)
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped")
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(power_off_camera, name, gopro) 
                       for name, gopro in cameras_gopro.items()]


if __name__ == "__main__":
    # Full multi-camera demo
    main()
    
    # For continuous monitoring only:
    # demo_continuous_monitoring()
