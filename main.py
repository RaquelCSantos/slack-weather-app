from flask import Flask, request, jsonify
import requests, urllib
import hmac, hashlib
import vault

__author__ = 'Luís Teles'
__copyright__ = 'N/A'
__credits__ = ['N/A']
__license__ = ''
__version__ = '1.0.0'
__maintainer__ = 'Luís Teles'
__status__ = 'prod'

# Initialize the Flask app with the class name (main in this case)
app = Flask(__name__)

def check_slack_secret(timestamp, request_body_raw,signature):
    """This function is used to validate the Slack token. It uses the new signing secret instead of the legacy verification token.

    Args:
        timestamp (int): The timestamp of the request (X-Slack-Request-Timestamp header).
        request_body_raw (str): The received request body.
        signature (str): The X-Slack-Signature header.

    Returns:
        bool: True if secret is valid / the expected one. False otherwise.
    """
    # hint from https://stackoverflow.com/questions/64341222/how-to-validate-slack-api-request
    # Slack's docs: https://api.slack.com/authentication/verifying-requests-from-slack
    # convert the token to Slack's expected format
    version_number = "v0:"
    token_parts = []
    for key, val in request_body_raw.to_dict().items():
        encoded_val = urllib.parse.quote(val, safe='')
        key_val_pair = '='.join([key, encoded_val])
        token_parts.append(key_val_pair)
    request_body = "&".join(token_parts)
    
    # Create the base secret format as per Slack's documentation
    sig_basestring = version_number + timestamp + ':' + request_body
    
    # Convert slack_signing_secret and sig_basestring to bytes
    secret_bytes = bytes(vault.SLACK_SIGNING_SECRET, 'utf-8')
    message_bytes = bytes(sig_basestring, 'utf-8')

    # Compute the HMAC-SHA256 hash
    hmac_hash = hmac.new(secret_bytes, message_bytes, hashlib.sha256)

    # Get the hexadecimal representation of the hash digest
    hex_digest = hmac_hash.hexdigest()
    
    my_signature = 'v0=' + hex_digest

    # Compare the expected signature with the received one
    if my_signature == signature:
        return True
    else:
        return False
    
def get_weather(city):
    """This function retrieves a the current weather from a specified city using the OpenWeatherAPI.

    Args:
        city (str): Name of the city to get the current weather from

    Returns:
        dict: Response in JSON format. 
    """
    try:
        # Try to contact the API
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={vault.OPENWEATHERMAP_API_KEY}")
        
        # If the response is sucessful
        if response.status_code == 200:
            data = response.json()
            return {
                "description": data.get("weather",[])[0].get("description","").capitalize(),
                "temperature": data.get("main",[]).get("temp",""),
                "city" : data.get("name")
            }
        # If response is not sucessful
        else:
            return {}
    # If there is an error with the request itself
    except:
        return {}

@app.route("/jumo_weather", methods=["POST"])
def weather():
    """This function processes the received POST request and returns the weather result.

    Returns:
        dict: response from the API in JSON format. 
    """
    # Check if the request is coming from Slack and verify the token
    #if request.form.get("token") != SLACK_TOKEN: #Legacy verification method
    if not check_slack_secret(request.headers.get("X-Slack-Request-Timestamp"), request.form, request.headers.get("X-Slack-Signature")):
        return jsonify({"text": "Invalid Slack token"}), 401

    # Extract the location from the command
    city = request.form.get("text")
    if not city:
        return jsonify({"text": "Please specify a location"}), 200

    # Call OpenWeatherMap API to get weather data
    weather = get_weather(city)
    if len(weather)>0:
        # Parse weather data and format the response
        return jsonify({"text": f"The weather in {weather['city']} is {weather['description']} with a temperature of {weather['temperature']}°C"}), 200
      
    else:
        return jsonify({"text": "Error retrieving weather info, sorry."}), 200

if __name__ == "__main__":
    app.run(port=9002,debug=True) #Don't use the default port 5000 on Mac! Used by ControlCenter
