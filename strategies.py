import pyautogui
from helpers import find_and_click_image, is_image_on_screen, get_chrome_url, navigate_chrome_to, smart_sleep

has_checked_buffs = False

# --- STRATEGY 1: The standard farming loop ---
def farm_slime_routine():
    """Logic for standard slime farming."""
    current_link = get_chrome_url()
    check_buff()
    if current_link is None:
        return
    if(current_link) == "https://game.granbluefantasy.jp/#quest/supporter/400181/4":
        possible_buttons = ['images/ok1.png', 'images/ok2.png']
        find_and_click_image(possible_buttons, timeout=3)
    elif "https://game.granbluefantasy.jp/#raid/" in current_link:
        print("⚔️ Currently in a battle or result screen. Waiting...")
        if is_image_on_screen('images/semi_auto_on.png', timeout=2):
            smart_sleep(3)
        else:
            possible_buttons = ['images/attack.png', 'images/next.png']
            find_and_click_image(possible_buttons, timeout=3)
            find_and_click_image('images/semi_auto.png', timeout=10)
    elif "https://game.granbluefantasy.jp/#result/" in current_link:
        possible_buttons = ['images/ok1.png', 'images/ok2.png', 'images/close.png', 'images/emp.png']
        find_and_click_image(possible_buttons, timeout=3)
        find_and_click_image('images/play_again.png', timeout=3)
    else:
        print("🧭 We are off course. Redirecting to quest...")
        navigate_chrome_to("https://game.granbluefantasy.jp/#quest/supporter/400181/4")

# --- STRATEGY 2: A totally different bot logic ---
def navigate_menu_routine():
    """Logic for moving through the game menus."""
    print("Navigating menus...")
    find_and_click_image('images/menu.png', timeout=5)
    find_and_click_image('images/inventory.png', timeout=5)

# --- STRATEGY 3: Add as many as you want in the future! ---
def auto_heal_routine():
    """Checks health and clicks potion if needed."""
    if is_image_on_screen('images/low_health.png'):
        print("Health is low! Using potion...")
        find_and_click_image('images/potion.png')

# --- Local bot logic---
def check_buff():
    """Checks shop journey drop buff ONLY ONCE!"""
    
    # 2. Tell Python we want to use the global sticky note
    global has_checked_buffs 
    
    # 3. Check the note! If it's True, we immediately exit the function.
    if has_checked_buffs == True:
        print("⏭️ Buffs were already checked this session. Skipping...")
        return  # This kicks the bot out of the function without running the code below!

    print("🛡️ Checking buffs for the first time...")
    navigate_chrome_to("https://game.granbluefantasy.jp/#shop/exchange/trajectory")
    
    if is_image_on_screen('images/no_buff.png', timeout=3):
        # 1st buff
        window_area = (294,571,450,160)
        find_and_click_image('images/activate_journey.png', timeout=3, region=window_area)
        find_and_click_image('images/lvl4_exp_50.png', timeout=3)
        window_area = (300,563,550,550)
        possible_buttons = ['images/ok1.png', 'images/ok2.png']
        for i in range(2):
            print(f"--- Attempting OK button click {i + 1} of 2 ---")
            find_and_click_image(possible_buttons, timeout=3, region=window_area)
            smart_sleep(1) # Added sleep to let menus load!
            
        # 2nd buff
        window_area = (288,747,450,160)
        find_and_click_image('images/activate_journey.png', timeout=3, region=window_area)
        find_and_click_image('images/lvl4_rp_50.png', timeout=3)
        window_area = (300,563,550,550)
        for i in range(2):
            print(f"--- Attempting OK button click {i + 1} of 2 ---")
            find_and_click_image(possible_buttons, timeout=10, region=window_area)
            smart_sleep(1)
            
    else:
        print("✅ Buffs are already active!")
        navigate_chrome_to("https://game.granbluefantasy.jp/#mypage")

    # 4. MARK THE TASK AS DONE!
    # The next time the loop calls check_buff(), the bot will see this is True and skip it.
    has_checked_buffs = True 
    print("📝 Marked buff check as complete.")