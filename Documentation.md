# Slack Weather Snippet
## Code Documentation
<a id="main">

<a id="main.check_slack_secret"></a>
#### check\_slack\_secret

```python
def check_slack_secret(timestamp, request_body_raw, signature)
```

This function is used to validate the Slack token. It uses the new signing secret instead of the legacy verification token.

**Arguments**:

- `timestamp` _int_ - The timestamp of the request (X-Slack-Request-Timestamp header).
- `request_body_raw` _str_ - The received request body.
- `signature` _str_ - The X-Slack-Signature header.
  

**Returns**:

- `bool` - True if secret is valid / the expected one. False otherwise.

<a id="main.get_weather"></a>

#### get\_weather

```python
def get_weather(city)
```

This function retrieves a the current weather from a specified city using the OpenWeatherAPI.

**Arguments**:

- `city` _str_ - Name of the city to get the current weather from
  

**Returns**:

- `dict` - Response in JSON format.

<a id="main.weather"></a>

#### weather

```python
@app.route("/jumo_weather", methods=["POST"])
def weather()
```

This function processes the received POST request and returns the weather result.

**Returns**:

- `dict` - response from the API in JSON format.

<br>
