# Slack Weather Snippet
This magic piece of code allows you to retrieve the weather of a specified city using a Slack slash command.

For this you need:
* A Slack bot + a Slack slash command configured
* An OpenWeatherAPI account
* Ngrok for testing locally

## Installation
To use this script, just follow the steps below:
```bash 
git clone git@github.com:luis-at/slack-weather-app.git
pip3 install -r requirements.txt
```

## Running the script
First, you need to create a vault.py file on the code directory, following the structure below:
```python
SLACK_TOKEN = "YOUR_SLACK_TOKEN"
SLACK_SIGNING_SECRET = "YOUR_SIGNING_SECRET"
OPENWEATHERMAP_API_KEY = "YOUR_API_KEY"
```
Secondly, you need to run:
```bash
python3 main.py
```
Then, you should setup ngrok to listen and forward all the requests to configured Flask port (9002 in this case):
```bash
ngrok http --domain=YOUR_NGROK_DOMAIN 9002
```

If you have your Slack app and slash commands properly configured, you should now be able to run:
```bash
/jumo_weather Texas
```
And you should be seeing a reply. If you don't get any reply, it means that something is broken. Double-check the communication between Slack and ngrok, namely by checking that the configured domain matches the `YOUR_NGROK_DOMAIN` you used on the command above.

## Useful links
* [Slack API - Your Apps](https://api.slack.com/app) - To manage and create your Slack Apps
* [Slack API Docs - API requests validation](https://api.slack.com/authentication/verifying-requests-from-slack) - To securely validate the API requests you get from Slack
