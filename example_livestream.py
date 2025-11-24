"""
Livestream demo for GoPro Hero 12 Black
Demonstrates streaming to RTMP server (YouTube, Twitch, custom server, etc.)
"""

from gopro_usb import GoProUSB
import time

SN1 = "C3504224696431"
SN2 = "C3504224677229"
SN3 = "C3504224682139"
SN = SN3


def demo_youtube_livestream():
    """
    Demo: Livestream to YouTube
    
    To get your YouTube stream key:
    1. Go to YouTube Studio
    2. Click "Create" > "Go Live"
    3. Copy your Stream Key
    4. Use RTMP URL: rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY
    """
    
    gopro = GoProUSB(SN)
    
    print("="*60)
    print("🎥 GoPro Livestream Demo - YouTube")
    print("="*60)
    
    # YOUR RTMP URL HERE
    RTMP_URL = "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY_HERE"
    
    # Or use a custom RTMP server
    # RTMP_URL = "rtmp://your-server.com:1935/live/stream_key"
    
    try:
        # 1. Power on
        print("\n📍 Step 1: Powering on camera")
        print("-" * 60)
        gopro.power_on()
        time.sleep(2)
        
        # 2. Start livestream
        print("\n📍 Step 2: Starting livestream")
        print("-" * 60)
        
        # Options: resolution="1080p" or "720p" or "480p"
        #          fov="wide" or "linear" or "narrow"
        if gopro.start_livestream(
            rtmp_url=RTMP_URL,
            resolution="1080p",
            fov="wide"
        ):
            # 3. Monitor livestream
            print("\n📍 Step 3: Monitoring livestream (30 seconds)")
            print("-" * 60)
            print("💡 Livestream is active - check your streaming platform")
            
            for i in range(6):
                time.sleep(5)
                status = gopro.get_livestream_status()
                print(f"   📡 {(i+1)*5}s - Active: {status['active']} | "
                      f"Resolution: {status['resolution']} | FOV: {status['fov']}")
            
            # 4. Stop livestream
            print("\n📍 Step 4: Stopping livestream")
            print("-" * 60)
            gopro.stop_livestream()
        
        # 5. Power off
        print("\n📍 Step 5: Powering off")
        print("-" * 60)
        gopro.power_off()
        
        print("\n" + "="*60)
        print("✅ Livestream demo completed!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        print("Stopping livestream...")
        gopro.stop_livestream()
        time.sleep(1)
        gopro.power_off()
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        try:
            gopro.stop_livestream()
        except:
            pass


def demo_custom_rtmp_server():
    """
    Demo: Livestream to custom RTMP server
    
    You can use this with:
    - YouTube: rtmp://a.rtmp.youtube.com/live2/stream_key
    - Twitch: rtmp://live.twitch.tv/app/stream_key
    - Facebook: rtmps://live-api-s.facebook.com:443/rtmp/stream_key
    - Custom server (e.g., nginx-rtmp, OBS streaming)
    """
    
    gopro = GoProUSB(SN)
    
    print("="*60)
    print("🎥 GoPro Livestream Demo - Custom RTMP")
    print("="*60)
    
    # Configure your RTMP URL here
    RTMP_URL = input("\n📡 Enter your RTMP URL: ")
    
    if not RTMP_URL or not RTMP_URL.startswith("rtmp"):
        print("❌ Invalid RTMP URL")
        return
    
    try:
        gopro.power_on()
        time.sleep(2)
        
        # Start with different quality options
        print("\n📋 Quality options:")
        print("1. 1080p Wide (best quality)")
        print("2. 720p Wide (balanced)")
        print("3. 480p Wide (low bandwidth)")
        print("4. 1080p Linear (less distortion)")
        
        choice = input("\nSelect quality (1-4): ").strip()
        
        quality_map = {
            "1": ("1080p", "wide"),
            "2": ("720p", "wide"),
            "3": ("480p", "wide"),
            "4": ("1080p", "linear"),
        }
        
        resolution, fov = quality_map.get(choice, ("1080p", "wide"))
        
        if gopro.start_livestream(RTMP_URL, resolution=resolution, fov=fov):
            print("\n✅ Livestream is running!")
            print("Press Ctrl+C to stop...")
            
            # Keep streaming until interrupted
            while True:
                time.sleep(5)
                status = gopro.get_livestream_status()
                if not status['active']:
                    print("⚠️  Livestream stopped unexpectedly")
                    break
                print(f"   📡 Streaming... ({status['resolution']} {status['fov']})")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping livestream...")
        gopro.stop_livestream()
        time.sleep(1)
        gopro.power_off()
        print("✅ Stream stopped")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        gopro.stop_livestream()


def demo_monitor_only():
    """
    Demo: Just check livestream status without starting
    """
    gopro = GoProUSB(SN)
    
    gopro.power_on()
    time.sleep(1)
    
    status = gopro.get_livestream_status()
    
    print("\n📡 Current Livestream Status:")
    print(f"   Active: {status['active']}")
    print(f"   Resolution: {status['resolution']}")
    print(f"   FOV: {status['fov']}")
    print(f"   Status Code: {status['status_code']}")


if __name__ == "__main__":
    print("\n🎥 GoPro Livestream Examples\n")
    print("Choose demo:")
    print("1. YouTube livestream (30s demo)")
    print("2. Custom RTMP server (manual)")
    print("3. Check status only")
    
    choice = input("\nSelect (1-3): ").strip()
    
    if choice == "1":
        demo_youtube_livestream()
    elif choice == "2":
        demo_custom_rtmp_server()
    elif choice == "3":
        demo_monitor_only()
    else:
        print("Invalid choice")
