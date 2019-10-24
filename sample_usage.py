import requests

HOST = '127.0.0.1'
PORT = 5000
BASE_URL = 'http://{}:{}'.format(HOST, PORT)

# Turn on the warning light
if input("Turn on the warning light? [y/N]").strip() in 'yY':
    print('Turning on the warning light.')
    resp = requests.post(BASE_URL+'/warning_light/on')
    print('res: ', resp.content)

# Turn on the warning light
if input("Turn off the warning light? [y/N]").strip() in 'yY':
    print('Turning off the warning light.')
    resp = requests.post(BASE_URL+'/warning_light/off')
    print('res: ', resp.content)

# Fire cannon 1
if input("Fire cannon 1 [y/N]").strip() in 'yY':
    print('Firing cannon 1.')
    resp = requests.post(BASE_URL+'/cannon_1/fire')
    print('res: ', resp.content)

# Reload cannon 1
if input("Reload cannon 1 [y/N]").strip() in 'yY':
    print('Reload cannon 1.')
    resp = requests.post(BASE_URL+'/cannon_1/reload')
    print('res: ', resp.content)

# Reload cannon 1
if input("Fire cannon 1 with 10 sec warning [y/N]").strip() in 'yY':
    print('Firing cannon 1 with 10 sec warning.')
    resp = requests.post(BASE_URL+'/cannon_1/fire?delay=10')
    print('res: ', resp.content)

# Reload cannon 1
if input("Reload cannon 1 [y/N]").strip() in 'yY':
    print('Reload cannon 1.')
    resp = requests.post(BASE_URL+'/cannon_1/reload')
    print('res: ', resp.content)

# Reload cannon 1
if input("Fire cannon 1 with 0 sec warning [y/N]").strip() in 'yY':
    print('Firing cannon 1 with 0 sec warning.')
    resp = requests.post(BASE_URL+'/cannon_1/fire?delay=0')
    print('res: ', resp.content)