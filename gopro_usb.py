# GoPro USB Controller
# Inspired by goproUSB by Lukasz J. Nowak
# Adapted for USB control with power management and real-time status

import requests
import datetime
import time
from typing import Optional, Dict, Any


class GoProUSB:
    """
    Class to control a GoPro via USB.
    
    Args:
        sn: Camera serial number (used to generate the base URL)
    """
    
    def __init__(self, sn: str):
        """
        Initialize the connection with the GoPro.
        
        Args:
            sn: Camera serial number (last 3 digits are used for the IP)
        """
        self.base_url = f'http://172.2{sn[-3]}.1{sn[-2:]}.51'
        self.session = requests.Session()
        self._last_status = {}
        
    # ==========================================
    # Camera state and information
    # ==========================================
    
    def get_state(self) -> Dict[str, Any]:
        """
        Retrieve the complete camera state.
        
        Returns:
            Dict containing the camera state
        """
        url = self.base_url + '/gopro/camera/state'
        response = self.session.get(url)
        response.raise_for_status()
        self._last_status = response.json()
        return self._last_status
    
    def get_status_realtime(self, interval: float = 1.0, duration: Optional[float] = None) -> None:
        """
        Display camera status in real-time.
        
        Args:
            interval: Interval between each update (in seconds)
            duration: Total monitoring duration (None = infinite, Ctrl+C to stop)
        """
        start_time = time.time()
        try:
            while True:
                if duration and (time.time() - start_time) >= duration:
                    break
                    
                state = self.get_state()
                
                # Display key information
                print("\n" + "="*50)
                print(f"⏰ {datetime.datetime.now().strftime('%H:%M:%S')}")
                print(f"🔋 Battery: {state['status'].get('70', 'N/A')}%")
                print(f"📹 Recording: {'YES' if state['status'].get('10', 0) == 1 else 'NO'}")
                print(f"⚙️  Mode: {self._get_mode_name(state['status'].get('43', 0))}")
                print(f"🔴 Busy: {'YES' if state['status'].get('8', 0) == 1 else 'NO'}")
                print(f"💾 SD available: {state['status'].get('54', 'N/A')} MB")
                print(f"📊 Resolution: {self._get_resolution_name(state['settings'].get('2', 'N/A'))}")
                print(f"🎬 FPS: {self._get_fps_name(state['settings'].get('3', 'N/A'))}")
                print(f"🔍 Lens: {self._get_lens_name(state['settings'].get('121', 'N/A'))}")
                print("="*50)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
    
    def _get_mode_name(self, mode_id: int) -> str:
        """Convert mode ID to readable name."""
        modes = {
            0: "Video",
            1: "Photo", 
            2: "Timelapse"
        }
        return modes.get(mode_id, f"Unknown ({mode_id})")
    
    def _get_resolution_name(self, res_id: int) -> str:
        """Convert resolution ID to readable name."""
        resolutions = {
            1: "4K",
            4: "2.7K",
            6: "2.7K 4:3",
            7: "1440p",
            9: "1080p",
            18: "4K 4:3",
            24: "5K",
            25: "5K 4:3",
            100: "5.3K"
        }
        return resolutions.get(res_id, f"Unknown ({res_id})")
    
    def _get_fps_name(self, fps_id: int) -> str:
        """Convert FPS ID to readable name."""
        fps_map = {
            0: "240",
            1: "120",
            2: "100",
            5: "60",
            6: "50",
            8: "30",
            9: "25",
            10: "24",
            13: "200"
        }
        return fps_map.get(fps_id, f"Unknown ({fps_id})")
    
    def _get_lens_name(self, lens_id: int) -> str:
        """Convert lens ID to readable name."""
        lenses = {
            2: "Narrow",
            3: "Superview",
            4: "Linear",
            7: "Max Superview",
            8: "Linear + Horizon",
            19: "Wide"
        }
        return lenses.get(lens_id, f"Unknown ({lens_id})")
    
    def get_datetime(self) -> requests.Response:
        """Get the camera's date and time."""
        url = self.base_url + '/gopro/camera/get_date_time'
        response = self.session.get(url)
        return response
    
    def set_datetime_now(self) -> requests.Response:
        """Synchronize the camera's date/time with current time."""
        url = self.base_url + datetime.datetime.now().strftime(
            '/gopro/camera/set_date_time?date=%Y_%m_%d&time=%H_%M_%S'
        )
        response = self.session.get(url)
        return response
    
    # ==========================================
    # Camera control
    # ==========================================
    
    def keep_alive(self) -> requests.Response:
        """Keep the connection active with the camera."""
        url = self.base_url + '/gopro/camera/keep_alive'
        response = self.session.get(url)
        return response
    
    def power_on(self) -> bool:
        """
        Power on the camera (via Wake-on-LAN or USB).
        Note: The GoPro must be connected via USB and in sleep mode.
        
        Returns:
            True if the command succeeded
        """
        try:
            # Try to enable USB control
            self.usb_enable()
            time.sleep(1)
            
            # IMPORTANT: Enable external control to allow settings changes
            self.set_control_external()
            time.sleep(0.5)
            
            # Check if the camera responds
            state = self.get_state()
            print("✅ Camera powered on and connected")
            return True
        except Exception as e:
            print(f"❌ Power on error: {e}")
            return False
    
    def power_off(self) -> bool:
        """
        Power off the camera.
        Note: Uses sleep mode for quick shutdown.
        
        Returns:
            True if the command succeeded
        """
        try:
            # Disable USB control to allow shutdown
            self.usb_disable()
            print("✅ Camera in sleep mode")
            return True
        except Exception as e:
            print(f"❌ Power off error: {e}")
            return False
    
    def usb_enable(self) -> requests.Response:
        """Enable wired USB control."""
        url = self.base_url + '/gopro/camera/control/wired_usb?p=1'
        response = self.session.get(url)
        return response
    
    def usb_disable(self) -> requests.Response:
        """Disable wired USB control."""
        url = self.base_url + '/gopro/camera/control/wired_usb?p=0'
        response = self.session.get(url)
        return response
    
    def set_control_idle(self) -> requests.Response:
        """Set the UI controller to idle mode."""
        url = self.base_url + '/gopro/camera/control/set_ui_controller?p=0'
        response = self.session.get(url)
        return response
    
    def set_control_external(self) -> requests.Response:
        """Set external control."""
        url = self.base_url + '/gopro/camera/control/set_ui_controller?p=2'
        response = self.session.get(url)
        return response
    
    # ==========================================
    # Recording
    # ==========================================
    
    def record_start(self) -> bool:
        """
        Start recording.
        
        Returns:
            True if recording started successfully
        """
        try:
            url = self.base_url + '/gopro/camera/shutter/start'
            response = self.session.get(url)
            response.raise_for_status()
            
            # Verify that recording has started
            time.sleep(0.5)
            state = self.get_state()
            if state['status'].get('10', 0) == 1:
                print("🔴 Recording started")
                return True
            else:
                print("⚠️  Recording did not start (check mode)")
                return False
        except Exception as e:
            print(f"❌ Recording start error: {e}")
            return False
    
    def record_stop(self) -> bool:
        """
        Stop recording.
        Note: Recording stop is asynchronous - the camera needs time to finalize the file.
        
        Returns:
            True if stop command was sent successfully
        """
        try:
            url = self.base_url + '/gopro/camera/shutter/stop'
            response = self.session.get(url)
            response.raise_for_status()
            
            print("⏹️  Recording stop requested")
            
            # Wait for camera to process (asynchronous operation)
            # Check status multiple times with increasing delays
            max_attempts = 5
            for attempt in range(max_attempts):
                time.sleep(1.0 if attempt == 0 else 0.5)
                state = self.get_state()
                
                # Check if recording has stopped
                if state['status'].get('10', 0) == 0:
                    print("✅ Recording stopped and file saved")
                    return True
                
                # Check if camera is busy encoding
                if state['status'].get('8', 0) == 1:
                    print(f"   ⏳ Encoding file... ({attempt + 1}/{max_attempts})")
                else:
                    print(f"   ⏳ Finalizing... ({attempt + 1}/{max_attempts})")
            
            # Final check
            state = self.get_state()
            if state['status'].get('10', 0) == 0:
                print("✅ Recording stopped")
                return True
            else:
                print("⚠️  Recording stop may still be processing in background")
                return True  # Command was sent, even if status not updated yet
                
        except Exception as e:
            print(f"❌ Recording stop error: {e}")
            return False
    
    # ==========================================
    # Modes and presets
    # ==========================================
    
    def mode_video(self) -> requests.Response:
        """Switch to Video mode."""
        url = self.base_url + '/gopro/camera/presets/set_group?id=1000'
        response = self.session.get(url)
        print("📹 Video mode enabled")
        return response
    
    def mode_photo(self) -> requests.Response:
        """Switch to Photo mode."""
        url = self.base_url + '/gopro/camera/presets/set_group?id=1001'
        response = self.session.get(url)
        return response
    
    def mode_timelapse(self) -> requests.Response:
        """Switch to Timelapse mode."""
        url = self.base_url + '/gopro/camera/presets/set_group?id=1002'
        response = self.session.get(url)
        return response
    
    # ==========================================
    # Resolution settings
    # ==========================================
    
    def set_resolution_5_3k(self) -> bool:
        """
        Set resolution to 5.3K.
        Note: For Hero 12 Black, use option 100
        
        Returns:
            True if the setting was applied successfully
        """
        try:
            # Hero 12 Black uses option 100 for 5.3K
            url = self.base_url + '/gopro/camera/setting?setting=2&option=100'
            response = self.session.get(url)
            response.raise_for_status()
            print("📊 Resolution: 5.3K")
            return True
        except Exception as e:
            print(f"❌ Resolution setting error: {e}")
            return False
    
    def set_resolution_5k(self) -> requests.Response:
        """Set resolution to 5K."""
        url = self.base_url + '/gopro/camera/setting?setting=2&option=24'
        response = self.session.get(url)
        return response
    
    def set_resolution_4k(self) -> requests.Response:
        """Set resolution to 4K."""
        url = self.base_url + '/gopro/camera/setting?setting=2&option=1'
        response = self.session.get(url)
        return response
    
    def set_resolution_2_7k(self) -> requests.Response:
        """Set resolution to 2.7K."""
        url = self.base_url + '/gopro/camera/setting?setting=2&option=4'
        response = self.session.get(url)
        return response
    
    def set_resolution_1080(self) -> requests.Response:
        """Set resolution to 1080p."""
        url = self.base_url + '/gopro/camera/setting?setting=2&option=9'
        response = self.session.get(url)
        return response
    
    # ==========================================
    # FPS settings (Frames Per Second)
    # ==========================================
    
    def set_fps_240(self) -> bool:
        """
        Set framerate to 240 FPS.
        
        Returns:
            True if the setting was applied successfully
        """
        try:
            url = self.base_url + '/gopro/camera/setting?setting=3&option=0'
            response = self.session.get(url)
            response.raise_for_status()
            print("🎬 FPS: 240")
            return True
        except Exception as e:
            print(f"❌ FPS setting error: {e}")
            return False
    
    def set_fps_200(self) -> requests.Response:
        """Set framerate to 200 FPS."""
        url = self.base_url + '/gopro/camera/setting?setting=3&option=13'
        response = self.session.get(url)
        return response
    
    def set_fps_120(self) -> requests.Response:
        """Set framerate to 120 FPS."""
        url = self.base_url + '/gopro/camera/setting?setting=3&option=1'
        response = self.session.get(url)
        return response
    
    def set_fps_60(self) -> requests.Response:
        """Set framerate to 60 FPS."""
        url = self.base_url + '/gopro/camera/setting?setting=3&option=5'
        response = self.session.get(url)
        return response
    
    def set_fps_30(self) -> requests.Response:
        """Set framerate to 30 FPS."""
        url = self.base_url + '/gopro/camera/setting?setting=3&option=8'
        response = self.session.get(url)
        return response
    
    def set_fps_24(self) -> requests.Response:
        """Set framerate to 24 FPS."""
        url = self.base_url + '/gopro/camera/setting?setting=3&option=10'
        response = self.session.get(url)
        return response
    
    # ==========================================
    # Lens settings
    # ==========================================
    
    def set_lens_linear(self) -> bool:
        """
        Set lens to Linear mode (for video).
        
        Returns:
            True if the setting was applied successfully
        """
        try:
            url = self.base_url + '/gopro/camera/setting?setting=121&option=4'
            response = self.session.get(url)
            response.raise_for_status()
            print("🔍 Lens: Linear")
            return True
        except Exception as e:
            print(f"❌ Lens setting error: {e}")
            return False
    
    def set_lens_wide(self) -> requests.Response:
        """Set lens to Wide mode."""
        url = self.base_url + '/gopro/camera/setting?setting=121&option=0'
        response = self.session.get(url)
        return response
    
    def set_lens_narrow(self) -> requests.Response:
        """Set lens to Narrow mode."""
        url = self.base_url + '/gopro/camera/setting?setting=121&option=2'
        response = self.session.get(url)
        return response
    
    def set_lens_superview(self) -> requests.Response:
        """Set lens to SuperView mode."""
        url = self.base_url + '/gopro/camera/setting?setting=121&option=3'
        response = self.session.get(url)
        return response
    
    def set_lens_max_superview(self) -> requests.Response:
        """Set lens to Max SuperView mode."""
        url = self.base_url + '/gopro/camera/setting?setting=121&option=7'
        response = self.session.get(url)
        return response
    
    def set_lens_linear_horizon(self) -> requests.Response:
        """Set lens to Linear + Horizon Lock mode."""
        url = self.base_url + '/gopro/camera/setting?setting=121&option=8'
        response = self.session.get(url)
        return response
    
    # ==========================================
    # Camera state - Utilities
    # ==========================================
    
    def is_busy(self) -> bool:
        """
        Check if the camera is busy.
        
        Returns:
            True if the camera is busy
        """
        state = self.get_state()
        return state['status'].get('8', 0) != 0
    
    def is_encoding(self) -> bool:
        """
        Check if encoding is in progress.
        
        Returns:
            True if encoding is active
        """
        state = self.get_state()
        return state['status'].get('10', 0) != 0
    
    def wait_until_ready(self, timeout: float = 30.0) -> bool:
        """
        Wait until the camera is ready (not busy, not encoding).
        
        Args:
            timeout: Maximum wait time in seconds
            
        Returns:
            True if the camera is ready, False if timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.is_busy() and not self.is_encoding():
                return True
            time.sleep(0.5)
        return False
    
    # ==========================================
    # Media management
    # ==========================================
    
    def get_media_list(self) -> requests.Response:
        """Get the list of media files on the SD card."""
        url = self.base_url + '/gopro/media/list'
        response = self.session.get(url)
        return response
    
    def download_last_media(self, output_filename: str) -> bool:
        """
        Download the last captured media file.
        
        Args:
            output_filename: Output file name (extension will be adjusted automatically)
            
        Returns:
            True if the download succeeded
        """
        try:
            # Wait until encoding is finished
            while self.is_encoding():
                time.sleep(1)
            
            ml = self.get_media_list()
            media_data = ml.json()
            
            if not media_data['media']:
                print("❌ No media found on the camera")
                return False
            
            last_dir = media_data['media'][-1]['d']
            last_file = media_data['media'][-1]['fs'][-1]['n']
            
            url = f"{self.base_url}/videos/DCIM/{last_dir}/{last_file}"
            
            # Adjust file extension
            extension = last_file.split('.')[-1]
            output_filename = output_filename.rsplit('.', 1)[0] + f'.{extension}'
            
            print(f"⬇️  Downloading {last_file}...")
            
            with self.session.get(url, stream=True) as request:
                request.raise_for_status()
                with open(output_filename, "wb") as f:
                    for chunk in request.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            print(f"✅ File downloaded: {output_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Download error: {e}")
            return False
    
    # ==========================================
    # Auto Power Down
    # ==========================================
    
    def set_auto_power_off_never(self) -> requests.Response:
        """Disable automatic power off."""
        url = self.base_url + '/gopro/camera/setting?setting=59&option=0'
        response = self.session.get(url)
        return response
    
    def set_auto_power_off_5min(self) -> requests.Response:
        """Set automatic power off to 5 minutes."""
        url = self.base_url + '/gopro/camera/setting?setting=59&option=4'
        response = self.session.get(url)
        return response
    
    # ==========================================
    # Livestreaming
    # ==========================================
    
    def start_preview(self) -> bool:
        """
        Start webcam/preview mode for local streaming.
        The stream is available at: udp://172.2X.1XX.51:8554
        
        Returns:
            True if preview started successfully
        """
        try:
            print("📹 Starting preview mode...")
            
            # Start webcam mode (provides UDP stream)
            url = self.base_url + '/gopro/webcam/start'
            response = self.session.get(url)
            response.raise_for_status()
            
            time.sleep(2)
            
            # Get the stream URL
            stream_url = f"udp://{self.base_url.split('//')[1].split(':')[0]}:8554"
            
            print(f"✅ Preview started!")
            print(f"📺 Stream URL: {stream_url}")
            print(f"💡 Use with OpenCV: cv2.VideoCapture('{stream_url}')")
            
            return True
            
        except Exception as e:
            print(f"❌ Preview start error: {e}")
            return False
    
    def stop_preview(self) -> bool:
        """
        Stop webcam/preview mode.
        
        Returns:
            True if preview stopped successfully
        """
        try:
            print("⏹️  Stopping preview...")
            url = self.base_url + '/gopro/webcam/stop'
            response = self.session.get(url)
            response.raise_for_status()
            
            time.sleep(1)
            print("✅ Preview stopped")
            return True
            
        except Exception as e:
            print(f"❌ Preview stop error: {e}")
            return False
    
    def get_stream_url(self) -> str:
        """
        Get the UDP stream URL for OpenCV capture.
        
        Returns:
            UDP stream URL
        """
        ip = self.base_url.split('//')[1].split(':')[0]
        return f"udp://{ip}:8554"
