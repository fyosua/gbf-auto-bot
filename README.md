# 🗡️ GBF Auto Bot 

A highly modular, computer-vision-based automation framework built for Granblue Fantasy (GBF) using Python and PyAutoGUI. 

Instead of a single messy script, this bot is built using a **Strategy Pattern**. The core engine handles the loop and safety checks, while individual bot behaviors (farming, navigating, healing) are built as separate plug-and-play modules.

## ✨ Core Features
* 🧠 **Modular Architecture:** Build endless custom routines in `strategies.py` without ever modifying the core bot engine.
* 🛑 **Hardware-Level Kill Switch:** Pressing `Esc` triggers a `sys.exit()` command that instantly terminates the process, even during sleep cycles.
* ⚡ **Smart Sleep Engine:** Replaces standard `time.sleep()`. It chunks waiting periods into 0.05s intervals so the bot is constantly listening for the kill switch with zero lag.
* 🔗 **Chrome URL Awareness:** The bot actively reads the browser's address bar via clipboard injection to verify its location, and can auto-redirect itself if it gets lost.
* 🎯 **Region-Based Scanning:** Image recognition is restricted to specific screen coordinates to drastically reduce CPU load and prevent false-positive clicks.
