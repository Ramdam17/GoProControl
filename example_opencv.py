"""
OpenCV Live Preview Example
Demonstrates how to capture and display the GoPro preview stream using OpenCV
"""

import cv2
from gopro_usb import GoProUSB
import time

# Your GoPro serial numbers
SN3 = "C3504224682139"

def demo_preview_display():
    """Display live preview from GoPro using OpenCV"""
    
    gopro = GoProUSB(SN3)
    
    try:
        # 1. Power on camera
        print("=" * 50)
        print("1. Powering on GoPro...")
        gopro.power_on()
        time.sleep(3)
        
        # 2. Configure camera to 4K, 120fps, Linear
        print("\n" + "=" * 50)
        print("2. Configuring camera (4K, 120fps, Linear)...")
        gopro.set_resolution_4k()
        time.sleep(1)
        gopro.set_fps_120()
        time.sleep(1)
        gopro.set_lens_linear()
        time.sleep(1)
        
        # 3. Start preview mode
        print("\n" + "=" * 50)
        print("3. Starting preview...")
        if gopro.start_preview():
            stream_url = gopro.get_stream_url()
            print(f"\n📹 Opening stream: {stream_url}")
            
            # 3. Open video stream with OpenCV
            cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
            
            # Set buffer size to reduce latency
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if not cap.isOpened():
                print("❌ Failed to open stream")
                print("💡 Make sure you have ffmpeg installed:")
                print("   brew install ffmpeg")
                return
            
            print("\n✅ Stream opened successfully!")
            print("📺 Displaying preview at 640x480... (Press 'q' to quit)")
            
            frame_count = 0
            start_time = time.time()
            
            while True:
                ret, frame = cap.read()
                
                if ret:
                    # Resize to 640x480 for display
                    display_frame = cv2.resize(frame, (640, 480))
                    
                    # Calculate FPS
                    frame_count += 1
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed if elapsed > 0 else 0
                    
                    # Add FPS overlay
                    cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Display resized frame
                    cv2.imshow('GoPro Preview', display_frame)
                    
                    # Check for 'q' key to quit
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print("⚠️  No frame received, retrying...")
                    time.sleep(0.1)
            
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
        
        # 4. Stop preview
        print("\n" + "=" * 50)
        print("4. Stopping preview...")
        gopro.stop_preview()
        
        # 5. Power off
        print("\n" + "=" * 50)
        print("5. Powering off...")
        gopro.power_off()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        gopro.stop_preview()
        gopro.power_off()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        gopro.stop_preview()
        gopro.power_off()


def demo_frame_processing():
    """Capture frames and apply simple processing"""
    
    gopro = GoProUSB(SN3)
    
    try:
        print("Starting preview with frame processing...")
        gopro.power_on()
        time.sleep(3)
        
        # Configure camera to 4K, 120fps, Linear
        print("Configuring camera (4K, 120fps, Linear)...")
        gopro.set_resolution_4k()
        time.sleep(1)
        gopro.set_fps_120()
        time.sleep(1)
        gopro.set_lens_linear()
        time.sleep(1)
        
        if gopro.start_preview():
            stream_url = gopro.get_stream_url()
            cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if not cap.isOpened():
                print("❌ Failed to open stream")
                return
            
            print("📺 Processing frames... (Press 'q' to quit)")
            
            while True:
                ret, frame = cap.read()
                
                if ret:
                    # Resize to 640x480 for display
                    display_frame = cv2.resize(frame, (640, 480))
                    cv2.imshow('Original', display_frame)
                    
                    # Grayscale
                    gray = cv2.cvtColor(display_frame, cv2.COLOR_BGR2GRAY)
                    cv2.imshow('Grayscale', gray)
                    
                    # Edge detection
                    edges = cv2.Canny(gray, 100, 200)
                    cv2.imshow('Edges', edges)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            
            cap.release()
            cv2.destroyAllWindows()
        
        gopro.stop_preview()
        gopro.power_off()
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
        gopro.stop_preview()
        gopro.power_off()


def demo_save_frames():
    """Save frames from the preview stream"""
    
    gopro = GoProUSB(SN3)
    
    try:
        print("Starting preview for frame capture...")
        gopro.power_on()
        time.sleep(3)
        
        # Configure camera to 4K, 120fps, Linear
        print("Configuring camera (4K, 120fps, Linear)...")
        gopro.set_resolution_4k()
        time.sleep(1)
        gopro.set_fps_120()
        time.sleep(1)
        gopro.set_lens_linear()
        time.sleep(1)
        
        if gopro.start_preview():
            stream_url = gopro.get_stream_url()
            cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if not cap.isOpened():
                print("❌ Failed to open stream")
                return
            
            print("📸 Press SPACE to save frame, 'q' to quit")
            
            frame_number = 0
            
            while True:
                ret, frame = cap.read()
                
                if ret:
                    # Resize to 640x480 for display only
                    display_frame = cv2.resize(frame, (640, 480))
                    cv2.imshow('Preview', display_frame)
                    
                    key = cv2.waitKey(1) & 0xFF
                    
                    if key == ord(' '):  # Space bar
                        # Save original resolution frame
                        filename = f"gopro_frame_{frame_number:04d}.jpg"
                        cv2.imwrite(filename, frame)
                        print(f"💾 Saved: {filename}")
                        frame_number += 1
                    
                    elif key == ord('q'):
                        break
            
            cap.release()
            cv2.destroyAllWindows()
        
        gopro.stop_preview()
        gopro.power_off()
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
        gopro.stop_preview()
        gopro.power_off()


if __name__ == "__main__":
    print("GoPro OpenCV Preview Examples")
    print("=" * 50)
    print()
    print("Choose an example:")
    print("1. Simple preview display")
    print("2. Frame processing (grayscale, edges)")
    print("3. Save frames")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        demo_preview_display()
    elif choice == "2":
        demo_frame_processing()
    elif choice == "3":
        demo_save_frames()
    else:
        print("Invalid choice, running default preview...")
        demo_preview_display()
