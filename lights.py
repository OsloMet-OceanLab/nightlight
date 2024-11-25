#!/usr/bin/env python3 

import gpiod as gpio
from numpy import around
from datetime import datetime, timedelta
from time import sleep
from pytz import timezone
from suntime import Sun
from apscheduler.schedulers.background import BackgroundScheduler
import signal
import sys


# Setup PWM pin
led_pin = 12
chip = gpio.Chip('gpiochip4')
led_line = chip.get_line(led_pin)

# Timing constants
time_format = "%H:%M"
minutes = 1 * 60

class ServiceKiller:
    kill = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.kill_service)
        signal.signal(signal.SIGTERM, self.kill_service)

    def kill_service(self, signum, frame):
        self.kill = True
        off()
        sys.exit(0)
        print("Kill signal caught")

def roundHalfHour(dt: datetime):
    # Get the current minute
    minute = dt.minute

    # Calculate how many minutes to the closest half-hour (either 0 or 30)
    if minute < 15:
        new_minute = 0
    elif minute < 45:
        new_minute = 30
    else:
        new_minute = 0
        dt += timedelta(hours=1)  # Round up to the next hour if it's closer

    # Create a new datetime with the rounded minute
    return dt.replace(minute=new_minute, second=0, microsecond=0)


def sunset_sunrise() -> tuple[datetime, datetime]:
    """
    Returns a tuple of sunset and sunrise of Vilanova la Geltrú in CET
    """

    # Fetch suntime in Vilanova i la Geltrú
    sun = Sun(41.2152, 1.7274)
    cet = timezone("CET")

    # The night goes from sunset to sunrise
    sunset = roundHalfHour(sun.get_sunset_time(time_zone=cet))
    sunrise = roundHalfHour(sun.get_sunrise_time(time_zone=cet))

    # TODO: Remove this
    # sunset = datetime(2024, 11, 25, 15, 19)
    # sunrise = datetime(2024, 11, 25, 15, 0)

    return sunset, sunrise


def on():
    try:
        # Request gpio service to give access
        led_line.request(consumer="LED", type=gpio.LINE_REQ_DIR_OUT)
        led_line.set_value(1)
    finally:
        # Always release after setting pin value
        led_line.release()


def off():
    try:
        # Request gpio service to give access
        led_line.request(consumer="LED", type=gpio.LINE_REQ_DIR_OUT)
        led_line.set_value(0)
    except OSError as e:
        print(f"Met error {e}, trying again")
        off()
    finally:
        # Always release after setting pin value
        led_line.release()


def night(scheduler: BackgroundScheduler, service_killer: ServiceKiller):
    """
    Runs lights at night
    """

    # Get new sunset and sunrise times
    sunset, sunrise = sunset_sunrise()
    # Express start hour and minute as strings
    start_hour, start_min = sunset.strftime(time_format).split(":")

    print(f"sunset: {sunset}")
    print(f"sunrise: {sunrise}")
    temp = sunrise - sunset
    night_duration = temp.total_seconds()

    NIGHT_PERIOD = 3600 * 1/2 # Half an hour night scheduling period
    on_time = 60 # One minute on
    off_time = NIGHT_PERIOD - on_time

    def run_night():
        repeat = around(night_duration / NIGHT_PERIOD, 0)

        while repeat > 0 and not service_killer.kill:
            on()
            print("Video lights on")
            sleep(on_time)
            off()
            print("Video lights off")
            
            # Allow for stopping early
            if not service_killer.kill:
                sleep(off_time)

            repeat -= 1

    # NOTE: The night schedule has consists of two jobs: 
    # 1) Called "night" running the actual schedule
    # 2) Called "schedule_night" used to reschedule the night schedule every day at 12:00
    scheduler.add_job(run_night, trigger='cron', hour=start_hour, minute=start_min, id="night", replace_existing=True, max_instances=1)
    scheduler.add_job(night, trigger='cron', hour=12, minute=0, args=[scheduler, service_killer], id="schedule_night", replace_existing=True)


def main():
    try:
        cet = timezone("CET")
        scheduler = BackgroundScheduler()
        scheduler.configure(timezone=cet)
        scheduler.start()

        service_killer = ServiceKiller()
        night(scheduler, service_killer)

        while not service_killer.kill:
            sleep(minutes)
            print("Tick! still alive")

    finally:
        print("Terminating...")
        scheduler.remove_all_jobs()
        print("Scheduled jobs cleared")
        scheduler.shutdown(wait=False)
        print("Scheduler terminated")
        off()
        print("Video lights off")
        print("nightlight.service terminated")


if __name__ == "__main__":
    main()