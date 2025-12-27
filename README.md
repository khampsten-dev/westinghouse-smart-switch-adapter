# Westinghouse Smart Switch Adapter

This project provides firmware for an ESP32-based adapter that automates the start/stop and maintenance cycle of a generator using relay outputs and status LEDs. The logic is implemented in `main.py` and is designed for use with Westinghouse (or similar) generators that can be remotely started and stopped via relay contacts.

## Features
- **Automated generator start/stop** based on external run request input
- **Cool-down cycle** after generator run
- **Scheduled maintenance runs** (e.g., once every 7 days)
- **Status LEDs** for run request, running, cool-down, and maintenance
- **Relay outputs** for start and kill generator functions
- **Debounced, non-blocking logic** using MicroPython's `asyncio`

## Pin Assignments
| Function                | ESP32 Pin |
|-------------------------|-----------|
| Run Sense Input         | 12        |
| Run Request Input       | 13        |
| Run Request LED         | 16        |
| Running LED             | 17        |
| Cool Down LED           | 18        |
| Maintenance LED         | 19        |
| Start Generator Relay   | 32        |
| Kill Generator Relay    | 33        |

## How It Works
- **Run Request:** When the run request input is active, the system starts the generator (if not already running) and resets the maintenance timer.
- **Cool Down:** When the run request is removed but the generator is running, a cool-down timer is started. After the cool-down period, the generator is stopped.
- **Maintenance:** If the generator has not run for a set number of days, a maintenance run is triggered for a fixed duration.
- **LEDs:** Indicate the current state (run request, running, cool-down, maintenance).
- **Relays:** Control the generator's start and stop (kill) circuits.

## Bill of Materials

| Item                               | Description                                                                                                                                                                                                                                      | Link                                                                 |
|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| Enclosure                          | HoHaing Junction Box Waterproof Plastic Project Box IP65 Plastic Project Box Electrical Box Enclosure Gray White 7.87"x4.72"x2.95"(200x120x75mm) - Amazon.com                                                                                   | [Amazon](https://www.amazon.com/dp/B0BZ871TH3)                      |
| ESP32 Development Board with Relays | AC/DC Power Supply ESP32 Development Board Programmable Development Board Wireless WiFi 4 Way Channel 5V Relay Module ESP32-WROOM-32E for Arduino AC 90-250V / DC 7-30V : Electronics                                                           | [Amazon](https://www.amazon.com/dp/B0DCZ549VQ)                      |
| Serial Adapter to Deploy Code      | HiLetgo CP2102 USB to TTL UART 232 485 Port Multi-Functional USB Serial Debug Tool for Windows Wince Linux Mac 32 64 : Electronics                                                                         | [Amazon](https://www.amazon.com/dp/B00LZVEQEY?th=1)                 |
| Optoisolators                      | Alinan 4pcs 4CH Optocoupler PC817 4 Channel Isolation Board Voltage Converter Adapter Module 3.6-30V Driver Photoelectric Isolated Module : Industrial & Scientific                                       | [Amazon](https://www.amazon.com/dp/B09ZH6D7CQ)                      |
| Fuse Holders                       | Joinfworld Panel Mount Fuse Holder 5x20mm 12V DC 250V AC Screw Cap Fuse Holders with Pre-Soldered Wires and Fast-Blow Glass Tube Fuses - 5Pack: Tools & Home Improvement                                  | [Amazon](https://www.amazon.com/dp/B0BF9LDW1P)                      |
| Fuses                              | BOJACK 5x20mm 1A 1amp 250V 0.2 x 0.78 Inch F1AL250V Fast-Blow Glass Fuses (Pack of 20): Tools & Home Improvement                                                                                        | [Amazon](https://www.amazon.com/dp/B07S96VTJR)                      |
| Panel-mount LEDs                   | Ltvystore 60Pcs 5MM 3Volt Prewired LED Diode 6 Colors LED Lamp Light Bulb Emitting Diodes + 60Pcs 5MM LED Clip Holder Panel Mount Black - Amazon.com                                                     | [Amazon](https://www.amazon.com/dp/B0B2L9FP4R?th=1)                 |
| Rectifier                          | MRELC Rectifier 4 Wires Voltage Regulator Compatible with Motorcycle Boat Motor Pump ATV GY6 50 150cc Scooter Moped JCL NST TAOTAO : Automotive                                                          | [Amazon](https://www.amazon.com/dp/B091MMPPZY)                      |
| GX20-7 Connectors                  | MECCANIXITY Aviation Connector Set 20mm 7 Terminals 5A 150V, GX20 Waterproof Male Female Connector Fittings with Plug Cover Pack of 5 Sets : Electronics                                                 | [Amazon](https://www.amazon.com/dp/B09BMYB9Y4)                      |
| Barrel Connector for Battery Tender| ThePoEstore 20 Pair DC 12V 5A Adapter Barrel Plug, 5.5mm X 2.1mm 20 x Male & 20 x Female DC Power Connector Jack, for CCTV Security Camera LED Light Strip : Electronics                                 | [Amazon](https://www.amazon.com/dp/B09Y1BBTZ2)                      |


## Wiring Diagram

Below is the wiring schematic for the Westinghouse Smart Switch Adapter:

![Wiring Schematic](./schematic.png)

## Usage
1. Connect the ESP32 pins as described above and in the diagram to your generator's remote start/stop interface and status LEDs.
2. Flash the ESP32 with MicroPython and upload `main.py`.
3. The script will automatically manage generator operation based on run requests and maintenance schedule.

## References

Similar project in C++ for rPI-pico [Westinghouse-12KW-transfer-switch](https://github.com/csvanholm/Westinghouse-12KW-transfer-switch/tree/main)

[Reddit thread](https://www.reddit.com/r/OffGrid/comments/mxygik/westinghouse_generator_automatic_transfer_switch/?rdt=50485) about another custom controller build with some details

Using OTS starter device $$$ [Westinghouse WH9500 / GSCM-mini Start Circuit](https://imgur.com/a/westinghouse-wh9500-gscm-mini-start-circuit-HQHf2BI)
![Westinghouse WH9500 / GSCM-mini Start Circuit](./w78Ivfb.jpeg)
