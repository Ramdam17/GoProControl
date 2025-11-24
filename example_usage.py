"""
GoProUSB Class Usage Example
Demonstrates complete control of a GoPro via USB
"""

from gopro_usb import GoProUSB
import time

SN1 = "C3504224696431"
SN2 = "C3504224677229"
SN3 = "C3504224682139"
SN = SN3


def main():
    # Replace with your GoPro serial number
    # The last 3 digits are used to generate the IP
    # Example: if SN = "C1234567890", will use 172.29.190.51

    SERIAL_NUMBER = SN
    
    print("="*60)
    print("🎥 GoPro USB Control Demo")
    print("="*60)
    
    # Initialisation de la caméra
    gopro = GoProUSB(SERIAL_NUMBER)
    
    try:
        # 1. POWER ON
        print("\n📍 Step 1: Powering on the camera")
        print("-" * 60)
        if not gopro.power_on():
            print("⚠️  Make sure the GoPro is connected via USB")
            return
        time.sleep(2)
        
        # 2. Initial configuration
        print("\n📍 Step 2: Configuring camera")
        print("-" * 60)
        
        # Switch to video mode
        gopro.mode_video()
        time.sleep(1)
        
        # IMPORTANT: For Hero 12 Black, set resolution BEFORE FPS
        # Valid combinations:
        # - 5.3K @ 60 FPS max
        # - 4K @ 120 FPS max
        # - 2.7K @ 240 FPS max
        # - 1080p @ 240 FPS max
        
        # Option 1: 4K @ 120 FPS (high quality + smooth)
        print("⚙️  Setting 4K @ 120 FPS (high quality + smooth)")
        gopro.set_resolution_4k()
        time.sleep(0.5)
        gopro.set_fps_120()
        time.sleep(0.5)
        
        # Option 2: High resolution (uncomment to use 5.3K @ 60 FPS instead)
        # print("⚙️  Setting 5.3K @ 60 FPS (high quality)")
        # gopro.set_resolution_5_3k()
        # time.sleep(0.5)
        # gopro.set_fps_60()
        # time.sleep(0.5)
        
        # Option 3: Slow motion (uncomment to use 2.7K @ 240 FPS instead)
        # print("⚙️  Setting 2.7K @ 240 FPS (slow motion)")
        # gopro.set_resolution_2_7k()
        # time.sleep(0.5)
        # gopro.set_fps_240()
        # time.sleep(0.5)
        
        # Set lens to Linear
        gopro.set_lens_linear()
        time.sleep(1)
        
        print("✅ Configuration complete")
        
        # 3. Status verification
        print("\n📍 Step 3: Status verification")
        print("-" * 60)
        state = gopro.get_state()
        print(f"🔋 Battery: {state['status'].get('70', 'N/A')}%")
        print(f"💾 Free space: {state['status'].get('54', 'N/A')} MB")
        print(f"📊 Resolution: {gopro._get_resolution_name(state['settings'].get('2', 'N/A'))}")
        print(f"🎬 FPS: {gopro._get_fps_name(state['settings'].get('3', 'N/A'))}")
        print(f"🔍 Lens: {gopro._get_lens_name(state['settings'].get('121', 'N/A'))}")
        
        # 4. Start recording
        print("\n📍 Step 4: Starting recording")
        print("-" * 60)
        gopro.record_start()
        
        # 5. Real-time status monitoring during recording
        print("\n📍 Step 5: Real-time monitoring (10 seconds)")
        print("-" * 60)
        print("💡 Status will be displayed every 2 seconds")
        gopro.get_status_realtime(interval=2.0, duration=10.0)
        
        # 6. Stop recording
        print("\n📍 Step 6: Stopping recording")
        print("-" * 60)
        gopro.record_stop()
        time.sleep(2)
        
        # 7. Download last media (optional)
        print("\n📍 Step 7: Download last media")
        print("-" * 60)
        download = input("Do you want to download the last media? (y/n): ")
        if download.lower() == 'y':
            gopro.download_last_media("last_recording")
        
        # 8. POWER OFF
        print("\n📍 Step 8: Powering off the camera")
        print("-" * 60)
        gopro.power_off()
        
        print("\n" + "="*60)
        print("✅ Demo completed successfully!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  User interruption")
        print("Stopping recording if active...")
        gopro.record_stop()
        time.sleep(1)
        gopro.power_off()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Attempting to stop recording...")
        try:
            gopro.record_stop()
            time.sleep(1)
        except:
            pass


def demo_continuous_monitoring():
    """
    Example of continuous status monitoring.
    Press Ctrl+C to stop.
    """
    SERIAL_NUMBER = SN
    gopro = GoProUSB(SERIAL_NUMBER)
    
    print("🎥 Continuous GoPro monitoring")
    print("Press Ctrl+C to stop\n")
    
    try:
        gopro.power_on()
        time.sleep(2)
        
        # Infinite monitoring until Ctrl+C
        gopro.get_status_realtime(interval=1.0)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped")
        gopro.power_off()


def demo_quick_recording():
    """
    Example of a quick 5-second recording.
    """
    SERIAL_NUMBER = SN
    gopro = GoProUSB(SERIAL_NUMBER)
    
    print("🎥 Quick 5-second recording\n")
    
    gopro.power_on()
    time.sleep(2)
    
    gopro.mode_video()
    gopro.set_resolution_5_3k()
    gopro.set_fps_240()
    gopro.set_lens_linear()
    time.sleep(2)
    
    print("🔴 Starting recording...")
    gopro.record_start()
    
    print("⏱️  Recording for 5 seconds...")
    time.sleep(5)
    
    print("⏹️  Stopping recording...")
    gopro.record_stop()
    
    time.sleep(2)
    gopro.power_off()
    
    print("✅ Recording complete!")


if __name__ == "__main__":
    # Complete demonstration
    main()
    
    # To use other examples, uncomment:
    # demo_continuous_monitoring()
    # demo_quick_recording()
