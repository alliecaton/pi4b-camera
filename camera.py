#!/usr/bin/env python3
"""
Raspberry Pi HQ Camera Control Class
Provides camera preview and photo capture functionality with GPIO button support
"""

import time
import os
import threading
from datetime import datetime
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO


class PiCameraController:
    """
    Raspberry Pi Camera Controller with GPIO button support
    """
    
    def __init__(self, button_pin=0, preview_size=(1640, 1232), still_size=(4056, 3040)):
        """
        Initialize the camera controller
        
        Args:
            button_pin (int): GPIO pin number for shutter button (default: 0)
            preview_size (tuple): Preview resolution (width, height)
            still_size (tuple): Still capture resolution (width, height)
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
        
        # Initialize GPIO
        self._setup_gpio()
        
        # Initialize camera
        self._initialize_camera()
    
    def _create_photos_dir(self):
        """Create photos directory if it doesn't exist"""
        if not os.path.exists(self.photos_dir):
            os.makedirs(self.photos_dir)
            print(f"Created {self.photos_dir} directory")
    
    def _setup_gpio(self):
        """Setup GPIO for button input"""
        try:
            GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            # Add button press detection with debouncing
            GPIO.add_event_detect(
                self.button_pin, 
                GPIO.FALLING, 
                callback=self._button_pressed, 
                bouncetime=300  # 300ms debounce
            )
            print(f"GPIO button setup complete on pin {self.button_pin}")
            
        except Exception as e:
            print(f"Error setting up GPIO: {e}")
            print("Button functionality will not be available")
    
    def _initialize_camera(self):
        """Initialize the camera with configurations"""
        try:
            self.picam2 = Picamera2()
            
            # Preview configuration
            self.preview_config = self.picam2.create_preview_configuration(
                main={"size": self.preview_size},
                lores={"size": (640, 480), "format": "YUV420"}
            )
            
            # Still capture configuration
            self.still_config = self.picam2.create_still_configuration(
                main={"size": self.still_size},
                buffer_count=1
            )
            
            print("Camera initialized successfully")
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            raise
    
    def _button_pressed(self, channel):
        """
        Callback function for button press
        
        Args:
            channel: GPIO channel that triggered the callback
        """
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
                print("Stopping camera preview...")
                self.picam2.stop_preview()
                self.picam2.stop()
                self.preview_active = False
                print("Preview stopped")
            else:
                print("Preview not active")
                
        except Exception as e:
            print(f"Error stopping preview: {e}")
    
    #!/usr/bin/env python3
"""
Raspberry Pi HQ Camera Control Class
Provides camera preview and photo capture functionality with GPIO button support
"""

import time
import os
import threading
from datetime import datetime
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO


class PiCameraController:
    """
    Raspberry Pi Camera Controller with GPIO button support
    """
    
    def __init__(self, button_pin=0, preview_size=(1640, 1232), still_size=(4056, 3040)):
        """
        Initialize the camera controller
        
        Args:
            button_pin (int): GPIO pin number for shutter button (default: 0)
            preview_size (tuple): Preview resolution (width, height)
            still_size (tuple): Still capture resolution (width, height)
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
        
        # Initialize GPIO
        self._setup_gpio()
        
        # Initialize camera
        self._initialize_camera()
    
    def _create_photos_dir(self):
        """Create photos directory if it doesn't exist"""
        if not os.path.exists(self.photos_dir):
            os.makedirs(self.photos_dir)
            print(f"Created {self.photos_dir} directory")
    
    def _setup_gpio(self):
        """Setup GPIO for button input"""
        try:
            GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            # Add button press detection with debouncing
            GPIO.add_event_detect(
                self.button_pin, 
                GPIO.FALLING, 
                callback=self._button_pressed, 
                bouncetime=300  # 300ms debounce
            )
            print(f"GPIO button setup complete on pin {self.button_pin}")
            
        except Exception as e:
            print(f"Error setting up GPIO: {e}")
            print("Button functionality will not be available")
    
    def _initialize_camera(self):
        """Initialize the camera with configurations"""
        try:
            self.picam2 = Picamera2()
            
            # Preview configuration
            self.preview_config = self.picam2.create_preview_configuration(
                main={"size": self.preview_size},
                lores={"size": (640, 480), "format": "YUV420"}
            )
            
            # Still capture configuration
            self.still_config = self.picam2.create_still_configuration(
                main={"size": self.still_size},
                buffer_count=1
            )
            
            print("Camera initialized successfully")
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            raise
    
    def _button_pressed(self, channel):
        """
        Callback function for button press
        
        Args:
            channel: GPIO channel that triggered the callback
        """
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
                print("Stopping camera preview...")
                self.picam2.stop_preview()
                self.picam2.stop()
                self.preview_active = False
                print("Preview stopped")
            else:
                print("Preview not active")
                
        except Exception as e:
            print(f"Error stopping preview: {e}")
    
    def capture_photo(self):
        """
        Capture a photo at full resolution
        
        Returns:
            str: Path to captured photo file, or None if failed
        """
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.photos_dir}/photo_{timestamp}.jpg"
            
            print(f"Capturing photo: {filename}")
            
            # Check if we need to switch to still configuration
            current_config = self.picam2.camera_configuration()
            needs_config_switch = current_config['main']['size'] != self.still_config['main']['size']
            
            if needs_config_switch:
                print("Switching to high-resolution mode...")
                was_preview_active = self.preview_active
                
                if self.preview_active:
                    self.picam2.stop_preview()
                
                self.picam2.stop()
                self.picam2.configure(self.still_config)
                self.picam2.start()
                
                if was_preview_active:
                    self.picam2.start_preview(Preview.QTGL)
                
                time.sleep(1)  # Allow camera to adjust
            
            # Capture the image
            self.picam2.capture_file(filename)
            
            # Switch back to preview mode if needed
            if needs_config_switch and self.preview_active:
                print("Returning to preview mode...")
                self.picam2.stop_preview()
                self.picam2.stop()
                self.picam2.configure(self.preview_config)
                self.picam2.start_preview(Preview.QTGL)
                self.picam2.start()
            
            # Get file info
            if os.path.exists(filename):
                file_size = os.path.getsize(filename) / (1024 * 1024)
                print(f"Photo saved successfully: {filename}")
                print(f"File size: {file_size:.1f} MB")
                return filename
            else:
                print("Error: Photo file was not created")
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
    
    def run_interactive_mode(self):
        """Run the camera in interactive command mode"""
        print("\nCamera Interactive Mode")
        print("=" * 25)
        
        # Display camera info
        camera_info = self.get_camera_info()
        if camera_info:
            print("\nCamera Information:")
            print("-" * 20)
            for key, value in camera_info.items():
                print(f"{key}: {value}")
        
        # Start preview
        self.start_preview()
        
        print(f"\nCamera Preview Controls:")
        print("Press 'c' + Enter to capture a photo")
        print("Press 'q' + Enter to quit")
        print("Press 's' + Enter to show camera status")
        print(f"OR press the hardware button on GPIO {self.button_pin}")
        print("-" * 40)
        
        try:
            while self.is_running:
                command = input("Command (c/s/q): ").lower().strip()
                
                if command == 'c':
                    filename = self.capture_photo()
                    if filename:
                        # Placeholder for post-processing
                        self.apply_post_processing(filename)
                        
                elif command == 's':
                    self._show_status()
                    
                elif command == 'q':
                    print("Quitting...")
                    self.is_running = False
                    break
                    
                else:
                    print("Invalid command. Use 'c' to capture, 's' for status, 'q' to quit.")
                    
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.is_running = False
    
    def _show_status(self):
        """Show current camera status"""
        print(f"Camera Status:")
        print(f"  Preview active: {self.preview_active}")
        print(f"  Running: {self.is_running}")
        print(f"  Photos directory: {self.photos_dir}")
        print(f"  Button pin: {self.button_pin}")
        print(f"  Preview size: {self.preview_size}")
        print(f"  Still size: {self.still_size}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("Cleaning up...")
            self.is_running = False
            
            if self.preview_active:
                self.stop_preview()
            
            if self.picam2:
                self.picam2.close()
            
            GPIO.cleanup()
            print("Cleanup completed successfully")
            
        except Exception as e:
            print(f"Error during cleanup: {e}")


def main():
    """Main function to run the camera controller"""
    camera = None
    
    try:
        # Initialize camera controller
        # Change button_pin if you're using a different GPIO pin
        camera = PiCameraController(button_pin=0)
        
        # Run in interactive mode
        camera.run_interactive_mode()
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Always cleanup
        if camera:
            camera.cleanup()


if __name__ == "__main__":
    print("Raspberry Pi HQ Camera Controller (Class-Based)")
    print("=" * 50)
    main()
    
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
    
    def run_interactive_mode(self):
        """Run the camera in interactive command mode"""
        print("\nCamera Interactive Mode")
        print("=" * 25)
        
        # Display camera info
        camera_info = self.get_camera_info()
        if camera_info:
            print("\nCamera Information:")
            print("-" * 20)
            for key, value in camera_info.items():
                print(f"{key}: {value}")
        
        # Start preview
        self.start_preview()
        
        print(f"\nCamera Preview Controls:")
        print("Press 'c' + Enter to capture a photo")
        print("Press 'q' + Enter to quit")
        print("Press 's' + Enter to show camera status")
        print(f"OR press the hardware button on GPIO {self.button_pin}")
        print("-" * 40)
        
        try:
            while self.is_running:
                command = input("Command (c/s/q): ").lower().strip()
                
                if command == 'c':
                    filename = self.capture_photo()
                    if filename:
                        # Placeholder for post-processing
                        self.apply_post_processing(filename)
                        
                elif command == 's':
                    self._show_status()
                    
                elif command == 'q':
                    print("Quitting...")
                    self.is_running = False
                    break
                    
                else:
                    print("Invalid command. Use 'c' to capture, 's' for status, 'q' to quit.")
                    
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.is_running = False
    
    def _show_status(self):
        """Show current camera status"""
        print(f"Camera Status:")
        print(f"  Preview active: {self.preview_active}")
        print(f"  Running: {self.is_running}")
        print(f"  Photos directory: {self.photos_dir}")
        print(f"  Button pin: {self.button_pin}")
        print(f"  Preview size: {self.preview_size}")
        print(f"  Still size: {self.still_size}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("Cleaning up...")
            self.is_running = False
            
            if self.preview_active:
                self.stop_preview()
            
            if self.picam2:
                self.picam2.close()
            
            GPIO.cleanup()
            print("Cleanup completed successfully")
            
        except Exception as e:
            print(f"Error during cleanup: {e}")


def main():
    """Main function to run the camera controller"""
    camera = None
    
    try:
        # Initialize camera controller
        # Change button_pin if you're using a different GPIO pin
        camera = PiCameraController(button_pin=0)
        
        # Run in interactive mode
        camera.run_interactive_mode()
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Always cleanup
        if camera:
            camera.cleanup()


if __name__ == "__main__":
    print("Raspberry Pi HQ Camera Controller (Class-Based)")
    print("=" * 50)
    main()