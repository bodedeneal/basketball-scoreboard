import RPi.GPIO as GPIO
import time

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
start_time = time.time()

print(score)  # Initial score output

# Function to measure distance
def measure_distance():
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
    return round(distance, 2)

try:
    while True:
        # Check if the game time has expired
        elapsed_time = time.time() - start_time
        if elapsed_time >= game_time:
            break

        # Measure distance
        distance = measure_distance()

        # Detect new movement within the threshold
        if distance < distance_threshold:
            current_time = time.time()
            if current_time - last_score_time >= score_interval:  # Enforce scoring interval
                score += 1
                last_score_time = current_time
                print(score)  # Output updated score

        time.sleep(0.1)  # Small delay to avoid rapid polling

except KeyboardInterrupt:
    print("\nGame interrupted!")

finally:
    GPIO.cleanup()
