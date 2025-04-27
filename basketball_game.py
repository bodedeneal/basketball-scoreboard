import RPi.GPIO as GPIO
import time
import threading
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
game_running = True
game_time = 120  # 2 minutes in seconds

# Function to detect motion using HC-SR04
def detect_motion():
    global score, game_running

    while game_running:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)  # Send a 10μs pulse
        GPIO.output(TRIG, False)

        # Measure the time of signal return
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Calculate distance in cm
        distance = round(distance, 2)

        if distance < 30:  # Detect motion if distance is less than 30 cm
            score += 5
            time.sleep(0.5)  # Debounce to avoid multiple detections

# Function to handle game timer
def game_timer(stdscr):
    global game_running
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = game_time - int(elapsed_time)

        # Update the timer on the screen
        stdscr.addstr(1, 0, f"Time Left: {remaining_time}s   ")
        stdscr.refresh()

        if remaining_time <= 0:
            game_running = False
            break
        time.sleep(1)

# Function to run the game
def main(stdscr):
    global score, game_running

    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Start motion detection in a separate thread
    motion_thread = threading.Thread(target=detect_motion)
    motion_thread.start()

    # Start the timer
    timer_thread = threading.Thread(target=game_timer, args=(stdscr,))
    timer_thread.start()

    # Main game loop
    while game_running:
        # Display score
        stdscr.addstr(0, 0, f"Score: {score}   ")
        stdscr.refresh()

        # Check for user input
        key = stdscr.getch()
        if key == ord('r'):  # Reset score if 'R' is pressed
            score = 0

    # End of game
    stdscr.addstr(2, 0, "Game Over! Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

# Run the game
try:
    curses.wrapper(main)
finally:
    GPIO.cleanup()
