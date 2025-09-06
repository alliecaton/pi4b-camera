#!/usr/bin/env python3
"""
Raspberry Pi HQ Camera Control Script
Provides camera preview and photo capture functionality
"""

import time
import os
from datetime import datetime
from picamera2 import Picamera2, Preview
import cv2

def main():
    # Initialize the camera
    picam2 = Picamera2()
    
    # Configure camera settings
    # For preview, use a smaller resolution for better performance
    preview_config = picam2.create_preview_configuration(
        main={"size": (1640, 1232)},  # Good balance of quality and performance
        lores={"size": (640, 480), "format": "YUV420"}
    )
    
    # For still capture, use full resolution
    still_config = picam2.create_still_configuration(
        main={"size": (4056, 3040)},  # Full HQ camera resolution
        buffer_count=1
    )
    
    try:
        print("Initializing camera...")
        picam2.configure(preview_config)
        
        # Start the camera preview
        print("Starting preview...")
        picam2.start_preview(Preview.QTGL)  # Use Qt OpenGL preview
        picam2.start()
        
        print("\nCamera Preview Controls:")
        print("Press 'c' + Enter to capture a photo")
        print("Press 'q' + Enter to quit")
        print("Press 's' + Enter to switch to still mode and back")
        print("-" * 40)
        
        # Create photos directory if it doesn't exist
        photos_dir = "photos"
        if not os.path.exists(photos_dir):
            os.makedirs(photos_dir)
        
        while True:
            command = input("Command (c/s/q): ").lower().strip()
            
            if command == 'c':
                # Capture photo
                capture_photo(picam2, still_config, photos_dir)
                
            elif command == 's':
                # Switch to still configuration temporarily
                print("Switching to still mode...")
                picam2.stop_preview()
                picam2.stop()
                picam2.configure(still_config)
                picam2.start_preview(Preview.QTGL)
                picam2.start()
                
                input("Press Enter to capture or any key to return to preview mode...")
                capture_photo(picam2, still_config, photos_dir)
                
                # Switch back to preview mode
                print("Returning to preview mode...")
                picam2.stop_preview()
                picam2.stop()
                picam2.configure(preview_config)
                picam2.start_preview(Preview.QTGL)
                picam2.start()
                
            elif command == 'q':
                print("Quitting...")
                break
                
            else:
                print("Invalid command. Use 'c' to capture, 's' for still mode, 'q' to quit.")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up
        try:
            picam2.stop_preview()
            picam2.stop()
            picam2.close()
            print("Camera closed successfully.")
        except:
            pass

def capture_photo(picam2, still_config, photos_dir):
    """Capture a photo and save it with timestamp"""
    try:
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{photos_dir}/photo_{timestamp}.jpg"
        
        print(f"Capturing photo: {filename}")
        
        # Switch to still configuration if not already
        current_config = picam2.camera_configuration()
        if current_config['main']['size'] != still_config['main']['size']:
            print("Switching to high-resolution mode for capture...")
            picam2.stop_preview()
            picam2.stop()
            picam2.configure(still_config)
            picam2.start()
            time.sleep(2)  # Allow time for camera to adjust
        
        # Capture the image
        picam2.capture_file(filename)
        print(f"Photo saved: {filename}")
        
        # Get file size for confirmation
        file_size = os.path.getsize(filename) / (1024 * 1024)  # Convert to MB
        print(f"File size: {file_size:.1f} MB")
        
    except Exception as e:
        print(f"Error capturing photo: {e}")

def check_camera_info():
    """Display camera information"""
    try:
        picam2 = Picamera2()
        print("Camera Information:")
        print("-" * 20)
        camera_properties = picam2.camera_properties
        for key, value in camera_properties.items():
            print(f"{key}: {value}")
        picam2.close()
    except Exception as e:
        print(f"Error getting camera info: {e}")

if __name__ == "__main__":
    print("Raspberry Pi HQ Camera Controller")
    print("=" * 35)
    
    # Optional: Display camera info
    print("\nChecking camera...")
    check_camera_info()
    print()
    
    # Start main program
    main()