from flask import Flask, request, jsonify
import json
import requests
import os

app = Flask(__name__)
port = int(os.environ.get('PORT', 3000))

# port = '5000'

@app.route('/countrydata', methods=['POST'])
def countrydata():
  data = json.loads(request.get_data())

  # Get the country's name from the bot
  country_name = data['conversation']['memory']['country']['raw']

  # Get the Coronavirus data for the specified country
  r = requests.get("https://corona.lmao.ninja/countries/"+country_name+"")

  return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      'content': 'Number of people infected in %s = %.0f, and the number of deaths = %.0f' % (country_name, r.json()['cases'], r.json()['deaths'])
    }]
  )


@app.route('/globalstats', methods=['POST'])
def globalstats():
  data = json.loads(request.get_data())

  # Get the global Coronavirus stats
  r = requests.get("https://corona.lmao.ninja/all")

  return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      'content': 'Number of infections globally = %.0f, and the number of deaths = %.0f' % (r.json()['cases'], r.json()['deaths'])
    }]
  )
# Handle Errors
@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data()))
  return jsonify(status=200)

# app.run(port=port)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)