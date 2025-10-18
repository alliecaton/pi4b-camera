#!/usr/bin/env python3
"""
Raspberry Pi HQ Camera Control Class
Provides camera preview and photo capture functionality with gpiozero button support
"""

import time
import os
from datetime import datetime
from picamera2 import Picamera2, Preview
from gpiozero import Button


class PiCameraController:
    """
    Raspberry Pi Camera Controller with gpiozero button support
    """
    
    def __init__(self, button_pin=16, preview_size=(800, 600), still_size=(2028, 1520)):
        """
        Initialize the camera controller
        
        Args:
            button_pin (int): GPIO pin number for shutter button (default: 16)
            preview_size (tuple): Preview resolution (width, height) - lower for power efficiency
            still_size (tuple): Still capture resolution (width, height) - higher quality
        """
        self.button_pin = button_pin
        self.preview_size = preview_size
        self.still_size = still_size
        self.photos_dir = "photos"
        
        # Camera and state management
        self.picam2 = None
        self.is_running = False
        self.preview_active = False
        
        # Create photos directory
        self._create_photos_dir()
        
        # Initialize button
        self._setup_button()
        
        # Initialize camera
        self._initialize_camera()
    
    def _create_photos_dir(self):
        """Create photos directory if it doesn't exist"""
        if not os.path.exists(self.photos_dir):
            os.makedirs(self.photos_dir)
            print(f"Created {self.photos_dir} directory")
    
    def _setup_button(self):
        """Setup button with gpiozero"""
        try:
            self.button = Button(self.button_pin, pull_up=True)
            self.button.when_pressed = self._on_button_pressed
            print(f"Button setup complete on pin {self.button_pin}")
            
        except Exception as e:
            print(f"Error setting up button: {e}")
            print("Button functionality will not be available")
    
    def _initialize_camera(self):
        """Initialize the camera with configurations"""
        try:
            self.picam2 = Picamera2()
            
            # Preview configuration - low resolution for power efficiency
            self.preview_config = self.picam2.create_preview_configuration(
                main={"size": self.preview_size},
                lores={"size": (640, 480), "format": "YUV420"}
            )
            
            # Still capture configuration - higher resolution for quality photos
            self.still_config = self.picam2.create_still_configuration(
                main={"size": self.still_size},
                lores={"size": (640, 480), "format": "YUV420"}
            )
            
            print("Camera initialized successfully")
            print(f"Preview resolution: {self.preview_size}")
            print(f"Still capture resolution: {self.still_size}")
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            raise
    
    def _on_button_pressed(self):
        """Callback function for button press"""
        if self.is_running:
            print("Button pressed - capturing photo!")
            self.capture_photo()
    
    def start_preview(self):
        """Start the camera preview"""
        try:
            if not self.preview_active:
                print("Starting camera preview...")
                self.picam2.configure(self.preview_config)
                self.picam2.start_preview(Preview.QTGL)
                self.picam2.start()
                self.preview_active = True
                self.is_running = True
                print("Preview started successfully")
            else:
                print("Preview already active")
                
        except Exception as e:
            print(f"Error starting preview: {e}")
    
    def stop_preview(self):
        """Stop the camera preview"""
        try:
            if self.preview_active:
                self.picam2.stop_preview()
                self.picam2.stop()
                self.preview_active = False
            else:
                print("Preview not active")
                
        except Exception as e:
            print(f"Error stopping preview: {e}")
    
    def capture_photo(self):
        """
        Capture a photo at still capture resolution (higher quality than preview)
        
        Returns:
            str: Path to captured photo file, or None if failed
        """
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.photos_dir}/photo_{timestamp}.jpg"
            
            # Switch to still configuration for higher resolution capture
            self.picam2.switch_mode_and_capture_file(self.still_config, filename)
            
            # Get file info
            if os.path.exists(filename):
                print(f"Photo captured at {self.still_size} resolution: {filename}")
                return filename
            else:
                return None
                
        except Exception as e:
            print(f"Error capturing photo: {e}")
            return None
    
    def apply_post_processing(self, image_path):
        """
        Apply post-processing effects to an image
        Placeholder for future implementation
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: Path to processed image, or None if failed
        """
        # TODO: Implement grain, filters, and other effects
        print(f"Post-processing placeholder for: {image_path}")
        print("Future: Add grain, filters, vintage effects, etc.")
        return image_path
    
    def get_camera_info(self):
        """
        Get camera properties and information
        
        Returns:
            dict: Camera properties
        """
        try:
            if self.picam2:
                return self.picam2.camera_properties
            return None
        except Exception as e:
            print(f"Error getting camera info: {e}")
            return None
    
    def run(self):
        """Start the camera preview and keep it running"""
        self.start_preview()
        
        try:
            print("Camera running. Press Ctrl+C to exit.")
            while self.is_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.is_running = False
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("Cleaning up...")
            self.is_running = False
            
            if self.preview_active:
                self.stop_preview()
            
            if self.picam2:
                self.picam2.close()
            
            if hasattr(self, 'button'):
                self.button.close()
            
            print("Cleanup completed successfully")
            
        except Exception as e:
            print(f"Error during cleanup: {e}")


def main():
    """Main function to run the camera controller"""
    camera = None
    
    try:
        # Initialize camera controller with optimized resolutions
        # Preview: 800x600 for low power on 3.5" display
        # Still capture: 2028x1520 for higher quality photos
        camera = PiCameraController(
            button_pin=16,
            preview_size=(800, 600),
            still_size=(2028, 1520)
        )
        
        # Run camera
        camera.run()
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        if camera:
            camera.cleanup()


if __name__ == "__main__":
    main()