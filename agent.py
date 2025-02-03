import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__) # Set up app
CORS(app, origins=["https://maatthw.github.io/PA1/"])

def find_pattern(bit_str):
    state = 0 # The initial state is S0, where the agent is simply waiting
    output = ['0'] * len(bit_str) # The output will be another string of the same length as input_string

    # Loop through the entire string. 'i' represents the index which will be used in the output, and bit refers to the specific char
    for i, bit in enumerate(bit_str):
        if state == 0: # Initial state
            if bit == '1': # This means we can move on to the next state, since we've identified the starting bit
                state = 1
        elif state == 1: # S1
            if bit == '0': # A 0 after a 1 indicates that we can move to state 2
                state = 2
            else:
                state = 1 # If it isn't a 0, then it's going to be a 1, and that means we just return to state 1.
        elif state == 2: # S2
            if bit == '0': # A 0 after 1 0 indicates that we can move to state 3
                state = 3
            else:
                state = 1 # If it isn't a 0, then it's going to be a 1, and that means we just return to state 1.
        elif state == 3: # S3
            if bit == '1': # A 1 after 1 0 0 indicates that the pattern has been located, and we can move to state 4 to check for overlaps
                state = 4
                output[i] = '1' # The final position of the '1001' pattern is used to mark where the pattern was found.
            else:
                state = 0 # If it isn't a 0, then it's going to be a 1, and that means we just return to state 1.
        elif state == 4: # S4
            state = 2 if bit == '0' else 1 # If there is a 0 after 1 0 0 1, then that indicates to move to state 2 since it is a 0 after a 1

    return ''.join(output) # Convert the list into a string

def generate_test_strings(n):
    # Function for generating test binary strings of length 12
    zero_prob = 0.65 # Probability of picking 0
    one_prob = 0.35 # Probability of picking 1
    bit_strs = []
    for i in range(n):
        bit_str = np.random.choice(['1', '0'], 12, p=[one_prob, zero_prob])
        bit_strs.append("".join(bit_str))
    return bit_strs

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    input_str = data.get("bit_str", "")

    output_str = find_pattern(input_str)

    print(f"Input: {input_str}\nOutput: {output_str}")
    return jsonify({"input": input_str, "output": output_str})

test_strings = generate_test_strings(10) # Generates 10 test strings to use
outputs = [find_pattern(bit_str) for bit_str in test_strings]

for i in range(len(outputs)):
    input_str = test_strings[i]
    output_str = outputs[i]
    print(f"Input String: {input_str}")
    print(f"Output String: {output_str}")
    print()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
