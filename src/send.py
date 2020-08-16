import requests

# _API_KEY="6e1336a2ffa94971b5f74715a85708b9"
# _URL="https://icfpc2020-api.testkontur.ru"

_API_KEY=None
_URL="https://api.pegovka.space"

GLOBAL_COUNTER = 0

def do_send(body, server_url=_URL, api_key=_API_KEY):
  send_url = f"{server_url}/aliens/send"
  if api_key:
    send_url += f"?apiKey={api_key}"
  print (" >>> sending response to API")
  res = requests.post(send_url, body)
  if res.status_code != 200:
    print('Unexpected server response:')
    print('HTTP code:', res.status_code)
    print('Response body:', res.text)
    raise RuntimeError("send request failed")
  global GLOBAL_COUNTER
  GLOBAL_COUNTER += 1
  print(f'{GLOBAL_COUNTER}: Server response:', res.text)
  return res.text
