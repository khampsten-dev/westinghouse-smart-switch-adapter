import machine
import time

# State constants (MicroPython-safe)
STATE_IDLE = 0
STATE_STARTING = 1
STATE_RUNNING = 2
STATE_COOLDOWN = 3
STATE_MAINTENANCE = 4
STATE_KILLING = 5

DEBUG = True

in_run_sense = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
in_run_request = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
led_run_request = machine.Pin(16, machine.Pin.OUT) # level sensitive
led_running = machine.Pin(17, machine.Pin.OUT)
led_cool_down = machine.Pin(18, machine.Pin.OUT)
led_maintenance = machine.Pin(19, machine.Pin.OUT)
relay_start_gen = machine.Pin(32, machine.Pin.OUT) # Edge sensitive
relay_kill_gen = machine.Pin(33, machine.Pin.OUT)

state = STATE_IDLE

TIME_SCALE = 0.001  # 1/1000 speed-up

cool_down_active = False
cool_down_duration = int(15 * 60 * 1000 * TIME_SCALE) # 15 minutes
cool_down_end = 0

us_per_day = int(24 * 60 * 60 * 1000 * TIME_SCALE) # one day
maintenance_active = False
maintenance_interval = 7 # maintenance days
days_until_maintenance = maintenance_interval
maintenance_duration = int(10 * 60 * 1000 * TIME_SCALE) # 10 minutes
maintenance_end = 0

kill_gen = False
last_manage_tick = 0
last_led_tick = 0
last_day_tick = 0
last_state = {
    "cool_down_active": cool_down_active,
    "maintenance_active": maintenance_active,
    "kill_gen": kill_gen,
    "running": False,
    "request_run": False,
    "days_until_maintenance": days_until_maintenance,
}

def debug_print(message):
    if DEBUG:
        print("[debug]", message)

def is_running():
    if DEBUG:
        return state == STATE_STARTING or state == STATE_RUNNING
    else :
        return not in_run_sense.value()

def is_request_run():
    return not in_run_request.value()

def is_cool_down_starting(): # krh rewrote - the cool_down_active dassertion was constantly putting this into a cooldown loop, instead use as an enable
    if not (cool_down_active or maintenance_active):
        return is_running() and (not is_request_run())
    else:
        return False
    
def is_cool_down_finished():
    return cool_down_active and time.ticks_diff(cool_down_end, time.ticks_ms()) < 0

def is_maintenance_starting():
    return days_until_maintenance == 0

def is_maintenance_finished():
    return maintenance_active and time.ticks_diff(maintenance_end, time.ticks_ms()) < 0


def manage_start_stop_tick():
    global state
    global cool_down_active
    global cool_down_end
    global maintenance_active
    global maintenance_end
  
    relay_start_gen.value(0)
    relay_kill_gen.value(0)
    
    if state == STATE_IDLE:
        debug_print("IDLE")    
        if is_request_run() or is_maintenance_starting():
            state = STATE_STARTING
            debug_print("run starting")
            if is_maintenance_starting():
                maintenance_active = True
                maintenance_end = time.ticks_add(time.ticks_ms(), maintenance_duration)
            
    
    elif state == STATE_STARTING:
        relay_start_gen.value(1)
        if is_running():
            debug_print("gen running")
            state = STATE_RUNNING  
        elif not is_request_run() and not maintenance_active:
            debug_print("run request gone - not running")
            # never started
            state = STATE_IDLE
  
        
    elif state == STATE_RUNNING:
 
            if not is_request_run() or is_maintenance_finished():
                debug_print("run cooldown started")
                maintenance_active = False
                cool_down_active = True
                state = STATE_COOLDOWN
                cool_down_end = time.ticks_add(time.ticks_ms(), cool_down_duration)

    elif state == STATE_COOLDOWN:
            if is_cool_down_finished():
                cool_down_active = False
                debug_print("kill request")
                state = STATE_KILLING
 
    elif state == STATE_KILLING:
            relay_kill_gen.value(1)
            if not is_running():
                debug_print("kill complete")
                state = STATE_IDLE           


def update_leds_tick():
    led_running.value(is_running())
    led_run_request.value(is_request_run())
    led_cool_down.value(cool_down_active)
    led_maintenance.value(maintenance_active)

def wait_days_tick():
    global days_until_maintenance
    
    if  state == STATE_IDLE: 
        days_until_maintenance -= 1
    else:
        days_until_maintenance = maintenance_interval
        
    debug_print("day tick -> days_until_maintenance={}".format(days_until_maintenance))


def main():
    global last_manage_tick, last_led_tick, last_day_tick
    last_manage_tick = time.ticks_ms()
    last_led_tick = time.ticks_ms()
    last_day_tick = time.ticks_us()
    debug_print("main loop start")

    while True:
        now_ms = time.ticks_ms()
        now_us = time.ticks_us()

        if time.ticks_diff(now_ms, last_manage_tick) >= 50:
            last_manage_tick = now_ms
            manage_start_stop_tick()
            #debug_print("manage_start_stop tick")

        if time.ticks_diff(now_ms, last_led_tick) >= 100:
            last_led_tick = now_ms
            update_leds_tick()
            #debug_print("led update tick")

        if time.ticks_diff(now_us, last_day_tick) >= us_per_day:
            last_day_tick = now_us
            wait_days_tick()

        time.sleep_ms(1)

main()



