import time
from flask import Flask, jsonify, request
import threading

DUMMY = True
if not DUMMY:
    import wiringpi
    # For sequential pin numbering
    wiringpi.wiringPiSetup()


class Relay:
    def __init__(self, pin_no):
        self.pin_no = pin_no
        self._state = False
        if not DUMMY:
            wiringpi.pinMode(self.pin_no, 1)
            wiringpi.digitalWrite(self.pin_no, 0)

    @property
    def state(self) -> bool:
        return self._state

    @state.setter
    def state(self, on: bool):
        if on:
            if not DUMMY:
                wiringpi.digitalWrite(self.pin_no, 1)
            self._state = True
            print("Setting pin {} high".format(self.pin_no))
        else:
            if not DUMMY:
                wiringpi.digitalWrite(self.pin_no, 0)
            self._state = False
            print("Setting pin {} low".format(self.pin_no))


class WarningLight:
    def __init__(self, pin_no):
        self._relay = Relay(pin_no)

    @property
    def state(self) -> bool:
        return self._relay.state

    @state.setter
    def state(self, on: bool):
        self._relay.state = on


class Cannon:
    STATE_LOADED = 'loaded'
    STATE_USED = 'used'

    def __init__(self, pin_no):
        self._relay = Relay(pin_no)
        self._state = Cannon.STATE_LOADED

    @property
    def state(self) -> str:
        return self._state

    def reload(self):
        self._relay.state = False
        self._state = Cannon.STATE_LOADED

    def fire(self) -> threading.Thread:
        if self.state != Cannon.STATE_LOADED:
            raise ValueError('This cannon is already fired!')
        self._state = Cannon.STATE_USED

        def th_main():
            self._relay.state = True
            time.sleep(30)
            self._relay.state = False

        th = threading.Thread(target=th_main)
        th.start()
        return th


app = Flask(__name__)

devices = {
    'warning_light': WarningLight(0),
    'cannon_1': Cannon(1),
    'cannon_2': Cannon(2),
    'cannon_3': Cannon(3),
    'cannon_4': Cannon(4),
    'cannon_5': Cannon(5),
    'cannon_6': Cannon(6),
    'cannon_7': Cannon(7),
}


@app.route('/<device_name>/status', methods=['GET'])
def status(device_name):
    if device_name not in devices:
        return 'Device not found', 404

    device = devices[device_name]
    if isinstance(device, Cannon):
        return jsonify({
            'name': device_name,
            'state': device.state
        })
    elif isinstance(device, WarningLight):
        return jsonify({
            'name': device_name,
            'state': device.state
        })
    else:
        return 'Status reporting for this device is not implemented', 501


@app.route('/<device_name>/on', methods=['POST'])
def on(device_name):
    if device_name not in devices:
        return 'Device not found', 404

    resp = {
        'name': device_name,
        'action': 'on',
        'msg': 'N/A'
    }
    device = devices[device_name]
    if isinstance(device, WarningLight):
        resp['msg'] = 'Turning the light on!'
        device.state = True
        return jsonify(resp)
    else:
        return 'The on command is only implemented for lights', 501


@app.route('/<device_name>/off', methods=['POST'])
def off(device_name):
    if device_name not in devices:
        return 'Device not found', 404

    resp = {
        'name': device_name,
        'action': 'off',
        'msg': 'N/A'
    }
    device = devices[device_name]
    if isinstance(device, WarningLight):
        resp['msg'] = 'Turning the light off!'
        device.state = False
        return jsonify(resp)
    else:
        return 'The off command is only implemented for lights', 501


@app.route('/<device_name>/fire', methods=['POST'])
def fire(device_name):
    if device_name not in devices:
        return 'Device not found', 404

    resp = {
        'name': device_name,
        'action': 'fire',
        'msg': 'N/A'
    }
    device = devices[device_name]
    if isinstance(device, Cannon):
        if device.state != Cannon.STATE_LOADED:
            resp['msg'] = 'The cannon is not in the loaded state'
            return jsonify(resp), 409

        delay = request.args.get('delay', default=3, type=int)

        if delay != 0:
            resp['msg'] = 'Firing the cannon in {} seconds. Warning light activated'.format(delay)

            def th_main():
                light = devices['warning_light']
                light.state = True
                time.sleep(delay)
                device.fire()
                time.sleep(4)
                light.state = False

            th = threading.Thread(target=th_main)
            th.start()
        else:
            resp['msg'] = 'Firing the cannon!'
            device.fire()
        return jsonify(resp)
    else:
        return 'The fire command is only implemented for cannons', 501


@app.route('/<device_name>/reload', methods=['POST'])
def reload(device_name):
    if device_name not in devices:
        return 'Device not found', 404

    resp = {
        'name': device_name,
        'action': 'reload',
        'msg': 'N/A'
    }
    device = devices[device_name]
    if isinstance(device, Cannon):
        if device.state != Cannon.STATE_USED:
            resp['msg'] = 'The cannon is not in the used state'
            return jsonify(resp), 409
        resp['msg'] = 'Reloading the cannon!'
        device.reload()
        return jsonify(resp)
    else:
        return 'The reload command is only implemented for cannons', 501


if __name__ == '__main__':
    app.run()
