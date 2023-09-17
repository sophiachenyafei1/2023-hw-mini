import machine
import time
import urandom
import ujson

# Define the button and built-in LED pins
button = machine.Pin(2, machine.Pin.IN)
led = machine.Pin(25, machine.Pin.OUT)

# Read the parameters from the JSON file
with open('experiment_params.json', 'r') as f:
    params = ujson.loads(f.read())
    num_flashes = params.get("num_flashes", 10)

response_times = []
misses = 0

for i in range(num_flashes):
    # Wait for a random period of time between 1 to 5 seconds
    wait_time = urandom.randint(1, 5)
    time.sleep(wait_time)

    # Flash the built-in LED
    led.on()
    start_time = time.ticks_us()

    # Wait for the button to be pressed, but add a timeout for "misses"
    timeout = time.ticks_add(start_time, 2000000)  # e.g., 2 seconds timeout
    while not button.value():
        if time.ticks_diff(time.ticks_us(), timeout) > 0:
            misses += 1
            response_times.append(-1)  # -1 denotes a miss
            break
    else:
        end_time = time.ticks_us()
        response_time = end_time - start_time
        response_times.append(response_time)
        print("Trial", i+1, ": Response time:", response_time, "microseconds")

    led.off()
    time.sleep(2)

# Compute min, max, and average of the valid response times
valid_responses = [t for t in response_times if t != -1]
min_response = min(valid_responses) if valid_responses else None
max_response = max(valid_responses) if valid_responses else None
avg_response = sum(valid_responses) / len(valid_responses) if valid_responses else None

results = {
    'response_times': response_times,
    'min_response': min_response,
    'max_response': max_response,
    'avg_response': avg_response,
    'misses': misses
}

# Write the results to a JSON file
with open('response_results.json', 'w') as f:
    f.write(ujson.dumps(results))

print("Test completed! Results saved to response_results.json.")

