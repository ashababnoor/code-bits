#!/usr/bin/env python3

import argparse
import time
import os
import subprocess
import sys


def play_alarm(sound_file=None, say_message=None):
    if sound_file and os.path.exists(sound_file):
        # play sound file
        if sys.platform == "darwin":
            subprocess.run(["afplay", sound_file])
        elif sys.platform.startswith("linux"):
            subprocess.run(["aplay", sound_file])
        return

    if say_message:
        # speak message
        if sys.platform == "darwin":
            subprocess.run(["say", "-v", "Alex", say_message])
        else:
            print(f"[SAY]: {say_message}")
        return

    # fallback default
    if sys.platform == "darwin":
        default_sound = "/System/Library/Sounds/Glass.aiff"
        subprocess.run(["afplay", default_sound])
    else:
        print("\a")  # terminal bell


def main():
    parser = argparse.ArgumentParser(description="⏰ Interval Alarm Clock")
    parser.add_argument(
        "--interval",
        type=int,
        required=True,
        help="Interval between alarms in minutes",
    )
    parser.add_argument(
        "--sound",
        type=str,
        default=None,
        help="Path to sound file to play",
    )
    parser.add_argument(
        "--say",
        type=str,
        default=None,
        help="Message to speak if no sound file is provided",
    )
    parser.add_argument(
        "--stop-after",
        type=int,
        default=None,
        help="Stop after this many alarms (default: runs forever)",
    )

    args = parser.parse_args()

    interval_seconds = args.interval * 60
    print(f"✅ Starting interval alarm every {args.interval} minutes.")
    if args.stop_after:
        print(f"⏳ Will stop after {args.stop_after} alarms.")
    print("🚪 Press Ctrl+C to stop early.\n")

    count = 0
    try:
        while True:
            time.sleep(interval_seconds)
            count += 1
            print(f"\n⏰ Alarm #{count} at {time.strftime('%H:%M:%S')}!")
            play_alarm(args.sound, args.say)

            if args.stop_after and count >= args.stop_after:
                print(f"\n🎉 Completed {count} alarms. Goodbye!")
                break

    except KeyboardInterrupt:
        print("\n👋 Stopped early. Goodbye!")


if __name__ == "__main__":
    main()
