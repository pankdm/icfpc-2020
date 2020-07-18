import requests

_API_KEY="6e1336a2ffa94971b5f74715a85708b9"
_URL="https://icfpc2020-api.testkontur.ru"

def do_send(body, server_url=_URL, api_key=_API_KEY):
  send_url = f"{server_url}/aliens/send"
  if api_key:
    send_url += f"?apiKey={api_key}"
  res = requests.post(send_url, body)
  if res.status_code != 200:
    print('Unexpected server response:')
    print('HTTP code:', res.status_code)
    print('Response body:', res.text)
    raise RuntimeError("send request failed")
  print('Server response:', res.text)
  return res.text
