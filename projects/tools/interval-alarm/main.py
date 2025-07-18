#!/usr/bin/env python3

import argparse
import time
import os
import subprocess
import sys


def play_alarm(sound_file=None, say_message=None):
    if sound_file and os.path.exists(sound_file):
        if sys.platform == "darwin":
            subprocess.run(["afplay", sound_file])
        elif sys.platform.startswith("linux"):
            subprocess.run(["aplay", sound_file])
        return

    if say_message:
        if sys.platform == "darwin":
            subprocess.run(["say", "-v", "Alex", say_message])
        else:
            print(f"[SAY]: {say_message}")
        return

    if sys.platform == "darwin":
        default_sound = "/System/Library/Sounds/Glass.aiff"
        subprocess.run(["afplay", default_sound])
    else:
        print("\a")  # terminal bell


def main():
    parser = argparse.ArgumentParser(description="⏰ Interval Alarm Clock")
    parser.add_argument(
        "--interval",
        type=float,
        required=True,
        help="Interval between alarms (number)"
    )
    parser.add_argument(
        "--unit",
        choices=["sec", "min", "hour"],
        default="min",
        help="Unit of interval: sec (seconds), min (minutes), hour (hours). Default is min"
    )
    parser.add_argument(
        "--sound",
        type=str,
        default=None,
        help="Path to sound file to play"
    )
    parser.add_argument(
        "--say",
        type=str,
        default=None,
        help="Message to speak if no sound file is provided"
    )
    parser.add_argument(
        "--stop-after",
        type=int,
        default=None,
        help="Stop after this many alarms (default: runs forever)"
    )
    parser.add_argument(
        "--notification-only",
        action="store_true",
        help="Send notifications instead of playing audio (requires --say)"
    )

    args = parser.parse_args()

    if args.notification_only and not args.say:
        print("Error: --notification-only requires --say to be specified.")
        return

    # convert interval to seconds
    unit_multipliers = {
        "sec": 1,
        "min": 60,
        "hour": 3600
    }
    interval_seconds = args.interval * unit_multipliers[args.unit]

    print(f"✅ Starting interval alarm every {args.interval} {args.unit}.")
    print(f"🕒 Starting timer from {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}.")
    if args.stop_after:
        print(f"⏳ Will stop after {args.stop_after} alarms.")
    print("🚪 Press Ctrl+C to stop early.\n")

    count = 0
    next_alarm_time = time.time() + interval_seconds
    try:
        while True:
            now = time.time()
            sleep_duration = max(0, next_alarm_time - now)
            print(f"⏳ Next alarm should be at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(next_alarm_time))}.")
            time.sleep(sleep_duration)

            count += 1
            print(f"\n⏰ Alarm #{count} at {time.strftime('%H:%M:%S')}!")

            if args.notification_only:
                # Send a notification instead of playing audio
                if sys.platform == "darwin":
                    subprocess.run(["osascript", "-e", f'display notification "{args.say}" with title "Alarm #{count}"'])
                elif sys.platform.startswith("linux"):
                    subprocess.run(["notify-send", f"Alarm #{count}", args.say])
                else:
                    print(f"[NOTIFICATION]: Alarm #{count} - {args.say}")
            else:
                play_alarm(args.sound, args.say)

            if args.stop_after and count >= args.stop_after:
                print(f"\n🎉 Completed {count} alarms. Goodbye!")
                break

            next_alarm_time += interval_seconds

    except KeyboardInterrupt:
        print("\n👋 Stopped early. Goodbye!")


if __name__ == "__main__":
    main()
