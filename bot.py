import time
from helpers import focus_target_window, smart_sleep

# 1. Import all the different strategies you wrote
from strategies import farm_slime_routine, navigate_menu_routine, auto_heal_routine

# ==========================================
# THE MASTER LOOP ENGINE
# ==========================================
def run_bot(bot_logic, max_loops=None, max_minutes=None):
    """
    Runs the master bot engine.
    bot_logic: The specific function (from strategies.py) you want to run.
    """
    print("\n🚀 BOT ENGINE STARTED!")
    print(f"🧠 Loaded Strategy: {bot_logic.__name__}")
    print("⚠️ PRESS 'ESC' AT ANY TIME TO INSTANTLY STOP.\n")
    
    start_time = time.time()
    loops_completed = 0
    
    while True:
        # Check Time Limit
        if max_minutes is not None:
            elapsed_minutes = (time.time() - start_time) / 60
            if elapsed_minutes >= max_minutes:
                print(f"\n⏱️ Time limit of {max_minutes} minutes reached. Stopping bot.")
                break
                
        # Check Loop Limit
        if max_loops is not None:
            if loops_completed >= max_loops:
                print(f"\n🔄 Loop limit of {max_loops} runs reached. Stopping bot.")
                break
                
        print(f"--- Starting Run #{loops_completed + 1} ---")
        
        # ==========================================
        # PLUG-AND-PLAY LOGIC EXECUTES HERE
        # ==========================================
        bot_logic() 
        
        # Add a short delay at the end of the loop
        smart_sleep(1) 
        
        loops_completed += 1

    print("🤖 Bot has completely shut down.")

# ==========================================
# START THE SCRIPT
# ==========================================
if __name__ == "__main__":
    app_name = "Granblue Fantasy - Google Chrome" 
    
    if focus_target_window(app_name):
        
        # THIS IS WHERE YOU PLUG AND PLAY!
        # Just pass the name of the strategy you want to use into run_bot.
        # Notice there are no parentheses () after the strategy name here!
        
        run_bot(farm_slime_routine, max_minutes=15)
        
        # To run a different bot, you would just change it to:
        # run_bot(navigate_menu_routine, max_loops=2)
        # run_bot(auto_heal_routine, max_minutes=60)
        focus_target_window('Visual Studio Code')