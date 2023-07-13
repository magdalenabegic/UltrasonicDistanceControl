# UltrasonicDistanceControl
Raspberry Pi-based automation system that integrates ultrasonic distance sensing and light detection

Materials used for this project: Raspberry Pi 4, 6 x LEDs, 4 x buttons, 1 x photocell, 1 x 1 μF capacitor, 1 x ultrasonic sensor, 1 x 1 kΩ resistor, 1 x 2 kΩ resistor.

## Project goal & details

When the program starts, all of the LEDs turn on and off for 3 seconds to verify their proper functioning. The ON/OFF button is used to activate or deactivate the system. After the program starts, at any time, the system can be activated or deactivated.

- If the system is deactivated, the red LED lights up, and the message "System: deactivated" is displayed on the screen, waiting for the ON/OFF button to be pressed to activate the system. The following is displayed on the screen:
System: deactivated
- If the system is activated, the green LED lights up, and the message "System: activated" is displayed on the screen, followed by the measured distance, light level, and "illumination threshold."
The following is displayed on the screen:
System: activated UZ sensor: ON Distance: ## cm Light sensor: #### Illumination threshold: ###

The DIST button turns the ultrasonic sensor on and off.

- If the ultrasonic sensor is activated, the “system ON” and the “distance” are displayed on the screen, and three LEDs (red, yellow, green) indicate the measured distance in the following ranges:
distance <= 15 cm (red LED lights up), 15 cm < distance <= 30 cm (yellow LED lights up), 30 cm < distance (green LED lights up)
The following is displayed on the screen:
System: activated ultrasonic sensor: ON Distance: ## cm Light sensor: #### Illumination threshold: ###
- If the ultrasonic sensor is deactivated, the system OFF is displayed on the screen, the distance is set to 0 cm, and the three LEDs (red, yellow, green) do not light up.
The following is displayed on the screen:
System: activated ultrasonic sensor: OFF Distance: 0 cm Light sensor: #### Illumination threshold: ###

When the system is active, LED_S turns on and off depending on the light level detected by the photocell and the "illumination threshold" we set. If the room's illumination is higher than the set threshold, LED_S is turned off, and if the level is lower, LED_S is turned on. The reading from the photocell and the illumination threshold are displayed on the screen.
The following is displayed on the screen:
System: activated UZ sensor: ON Distance: ## cm Light sensor: #### Illumination threshold: ####

- The "S+" button is used to increase the illumination threshold. When we press and release the S+ button, the threshold increases by 100. If we press the S+ button, hold it, and at the same time press and release the S- button, the threshold increases by 500.
- The "S-" button is used to decrease the illumination threshold. When we press and release the S- button, the threshold decreases by 100. If we press the S- button, hold it, and at the same time press and release the S+ button, the threshold decreases by 500.
If the system is deactivated, LED_S is turned off.

## Functions description

The **`rc_time`** function measures the time taken for a capacitor connected to the **`analog_pin`** to discharge through a photoresistor. It performs the following steps:

- Initializes a variable **`count`** to 0.
- Sets the **`analog_pin`** as an output and sets it to a low state (discharging the capacitor).
- Pauses the execution for 0.1 seconds to allow the capacitor to discharge.
- Sets the **`analog_pin`** as an input.
- Enters a loop that increments **`count`** as long as the **`analog_pin`** remains in a low state.
- Returns the final value of **`count`**, which represents the time taken for the capacitor to discharge.

The **`button1_callback`** function is a callback for the rising edge detection of **`button1`**. It adjusts the **`granica`** value based on the state of **`button2`**. If **`button2`** is pressed, it sets **`dupliGumb`** to **`True`** and decreases **`granica`** by 500. Otherwise, if **`dupliGumb`** is **`False`**, it increases **`granica`** by 100. Finally, if **`dupliGumb`** is **`True`** (indicating that both buttons were pressed simultaneously), it sets **`dupliGumb`** back to **`False`**. The **`granica`** value is also checked to ensure it doesn't go below 0.

The **`button2_callback`** function is a callback for the rising edge detection of **`button2`**. It adjusts the **`granica`** value based on the state of **`button1`**. If **`button1`** is pressed, it sets **`dupliGumb`** to **`True`** and increases **`granica`** by 500. Otherwise, if **`dupliGumb`** is **`False`**, it decreases **`granica`** by 100. Finally, if **`dupliGumb`** is **`True`**, it sets **`dupliGumb`** back to **`False`**. The **`granica`** value is also checked to ensure it doesn't go below 0.

The **`GPIO.add_event_detect`** function is used to detect rising edges on **`button1`** and **`button2`** and trigger the corresponding callback functions (**`button1_callback`** and **`button2_callback`**) when a rising edge is detected. The **`bouncetime`** parameter specifies the time in milliseconds for which events are ignored after an event is detected to prevent false triggering due to mechanical noise.

The variables **`upperBorder`**, **`lowerBorder`**, **`udaljenost`** (distance), and **`granica`** are initialized to their initial values.

The code enters a **`try`** block, starting an infinite loop that continuously monitors the system state and performs the corresponding actions.

If **`ButtonState`** is 1 (indicating that the system is activated):

- The **`zelena_sustav`** LED is turned on, and the **`crvena_sustav`** LED is turned off briefly.
- The **`rc_time`** function is called to measure the light level using the **`analog_pin`**. The measured value is compared with **`upperBorder`** and **`lowerBorder`**, and if necessary, these values are updated accordingly.
- The **`plava`** LED is turned on or off based on whether the measured light level exceeds the **`granica`** threshold.
- If **`ButtonState1`** is 0 (indicating that the distance measurement is activated), the ultrasonic distance sensor is triggered to measure the distance:
    - The **`trig`** pin is set to a low state for a brief period to generate a trigger signal.
    - The program waits for the ultrasonic pulse to return by monitoring the **`echo`** pin.
    - The time of flight is calculated based on the difference in timestamps before and after the pulse is detected.
    - The distance is calculated by multiplying the time of flight by the speed of sound and dividing it by 2 (since the pulse travels to the target and back).
    - The appropriate LEDs (**`crvena`**, **`zuta`**, **`zelena`**) are turned on or off based on the measured distance.
- If **`ButtonState1`** is not 0 (distance measurement deactivated), all LEDs (**`zelena`**, **`crvena`**, **`zuta`**) are turned off, and the **`udaljenost`** (distance) value is set to 0.
- The system state, **`upperBorder`**, **`granica`**, and **`udaljenost`** are printed.
- The loop is paused for 0.5 seconds.

If **`ButtonState`** is not 1 (indicating that the system is deactivated):

- The **`zelena_sustav`** LED is turned off, and the **`crvena_sustav`** LED is turned on.
- The **`crvena`**, **`zuta`**, and **`zelena`** LEDs are turned off.
- The **`granica`** and **`upperBorder`** values are reset to 0.
- The system state, **`upperBorder`**, and **`granica`** are printed.
- The loop is paused for 1 second.
