import pyautogui
import time
import keyboard
import sys
import pyperclip

def smart_sleep(seconds):
    """Breaks waiting time into 0.05s chunks to constantly listen for ESC."""
    end_time = time.time() + seconds
    while time.time() < end_time:
        if keyboard.is_pressed('esc'):
            print("\n🛑 INSTANT KILL SWITCH ACTIVATED! Shutting down immediately.")
            sys.exit() 
        time.sleep(0.05)

def focus_target_window(window_name):
    """Finds a window by title and brings it to the front."""
    print(f"Searching for a window containing: '{window_name}'...")
    windows = pyautogui.getWindowsWithTitle(window_name)
    if windows:
        target_win = windows[0]
        try:
            if target_win.isMinimized:
                target_win.restore()
            target_win.activate()
            print(f"Success! Focused on: {target_win.title}")
            smart_sleep(1)
            return True
        except Exception as e:
            print(f"Found the window, but couldn't bring it to the front: {e}")
    else:
        print(f"Could not find any open window named '{window_name}'.")
    return False

def find_and_click_image(image_paths, timeout=15, confidence_level=0.8, region=None):
    """
    Waits for one or more images to appear and clicks the first one it finds.
    image_paths: Can be a single string ('img.png') OR a list of strings (['img1.png', 'img2.png']).
    """
    # 1. If the user provided a single string, wrap it in a list so the code below always works
    if isinstance(image_paths, str):
        image_paths = [image_paths]
        
    if region:
        print(f"Waiting up to {timeout}s for any of {len(image_paths)} image(s) in region {region}...")
    else:
        print(f"Waiting up to {timeout}s for any of {len(image_paths)} image(s) on full screen...")
        
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if keyboard.is_pressed('esc'):
            print("\n🛑 INSTANT KILL SWITCH ACTIVATED!")
            sys.exit()
            
        # 2. Loop through every image in the list
        for img in image_paths:
            try:
                location = pyautogui.locateOnScreen(img, confidence=confidence_level, region=region)
                if location:
                    pyautogui.click(location)
                    print(f"🎯 Successfully found and clicked: {img}")
                    return True  # Stop and return immediately after clicking the first match
                    
            except pyautogui.ImageNotFoundException:
                continue  # Image wasn't found, instantly try the next image in the list
                
            except Exception as e:
                print(f"⚠️ CRASH DETECTED checking {img}: {e}")
                return False

        # 3. If NONE of the images in the list were found, sleep briefly before checking them all again
        smart_sleep(0.5)

    print(f"❌ Timed out: None of the target images appeared.")
    return False

def is_image_on_screen(image_paths, timeout=0, confidence_level=0.8, region=None):
    """
    Checks if one or more images are visible.
    Returns True if ANY of the images are found.
    """
    if isinstance(image_paths, str):
        image_paths = [image_paths]
        
    if timeout > 0:
        print(f"👀 Watching for any of {len(image_paths)} image(s) for up to {timeout} seconds...")
        
    start_time = time.time()
    
    while True:
        if keyboard.is_pressed('esc'):
            print("\n🛑 INSTANT KILL SWITCH ACTIVATED!")
            sys.exit()
            
        # Check all images in the list
        for img in image_paths:
            try:
                location = pyautogui.locateOnScreen(img, confidence=confidence_level, region=region)
                if location:
                    return True # Found one! Return True instantly.
            except pyautogui.ImageNotFoundException:
                continue
            except Exception as e:
                print(f"⚠️ Error checking for {img}: {e}")
                return False
                
        # Time limit check
        if time.time() - start_time >= timeout:
            return False
            
        smart_sleep(0.5)

def get_chrome_url():
    """
    Forces Chrome to highlight the address bar, copies it, and reads the clipboard.
    Returns the URL as a string.
    """
    print("🔍 Reading Chrome address bar...")
    
    # Clear the clipboard first so we don't accidentally read old data
    pyperclip.copy("")
    
    # Ctrl + L is the universal Windows shortcut to highlight the Chrome address bar
    pyautogui.hotkey('ctrl', 'l')
    smart_sleep(0.2) # Wait a tiny bit for Chrome to react
    
    # Ctrl + C copies the highlighted text
    pyautogui.hotkey('ctrl', 'c')
    smart_sleep(0.2) 
    
    # Read what we just copied!
    current_url = pyperclip.paste()
    
    # Click somewhere safe to unfocus the address bar (optional, but a good idea)
    # pyautogui.press('esc') 
    
    if current_url:
        print(f"🔗 Found URL: {current_url}")
        return current_url
    else:
        print("⚠️ Failed to copy URL.")
        return None
    
def navigate_chrome_to(url):
    """
    Highlights the Chrome address bar, pastes a new URL, and presses Enter.
    """
    print(f"🌐 Navigating to: {url}")
    
    # 1. Focus the address bar (Ctrl + L)
    pyautogui.hotkey('ctrl', 'l')
    smart_sleep(0.3) # Give Chrome a fraction of a second to highlight the bar
    
    # 2. Copy the new URL to clipboard and paste it (Ctrl + V)
    pyperclip.copy(url)
    pyautogui.hotkey('ctrl', 'v')
    smart_sleep(0.3)
    
    # 3. Press Enter to load the page
    pyautogui.press('enter')
    
    # Wait a moment for the page to actually start loading before moving on
    smart_sleep(2) 
    return True