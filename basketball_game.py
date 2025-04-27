import RPi.GPIO as GPIO
import time
import curses

# Pin configuration for HC-SR04 sensor
TRIG = 23  # GPIO pin for Trigger
ECHO = 24  # GPIO pin for Echo

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Initialize game variables
score = 0
last_score_time = 0  # Track the last time a basket was scored
distance_threshold = 10  # Threshold for detecting proximity (in cm)
score_interval = 1  # Minimum time between scores (in seconds)
game_time = 120  # 2 minutes in seconds

# Function to measure distance using HC-SR04
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # Send a 10μs pulse
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    # Wait for the echo to start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for the echo to end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Convert to centimeters
    return round(distance, 2)

# Main game function
def main(stdscr):
    global score, last_score_time

    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    start_time = time.time()

    # Main game loop
    while True:
        # Check if game time is over
        elapsed_time = time.time() - start_time
        if elapsed_time >= game_time:
            break

        # Measure distance
        distance = measure_distance()

        # Detect new movement close to the sensor
        if distance < distance_threshold:
            current_time = time.time()
            if current_time - last_score_time >= score_interval:  # Enforce scoring interval
                score += 5
                last_score_time = current_time

        # Display score and time left
        remaining_time = game_time - int(elapsed_time)
        stdscr.clear()
        stdscr.addstr(0, 0, f"Score: {score}")
        stdscr.addstr(1, 0, f"Time Left: {remaining_time}s")
        stdscr.addstr(2, 0, "Press 'R' to reset the score.")
        stdscr.refresh()

        # Handle user input
        key = stdscr.getch()
        if key == ord('r'):  # Reset score if 'R' is pressed
            score = 0

# Run the game
try:
    curses.wrapper(main)
finally:
    GPIO.cleanup()
