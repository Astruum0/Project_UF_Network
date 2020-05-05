import json
import sys
import ipaddress
import socket

help_msg = """
PyNetGames 1.0

Server configuration:

    USAGE: server.py [configs] [-s]

        -ip [ip/auto] : Give manual IP address to the server, type "auto" to use your device IP address (Default value)
        -p [port] : Give manual port to the server (Default is 5555)
        -s : Save this configuration to default value for next utilisation
        
Client-side configuration:

    USAGE: config.py [configs]
        -ip [ip/auto] : Set the server IP to the given ip, type "auto" to set your device IP address
        -p [port] : Set the server port to the given port (Default value is 5555)
"""


def saveValues(ip, port):
    with open("configs.json", "w") as f:
        config = {"ip": ip, "port": port}
        json.dump(config, f)


def getValues():
    with open("configs.json", "r") as f:
        config = json.load(f)
        return config["ip"], config["port"]


if __name__ == "__main__":
    if sys.argv[1] == "--help" and len(sys.argv) == 2:
        sys.exit(help_msg)

    server, port = getValues()

    for i, arg in enumerate(sys.argv[1:]):
        if arg == "-ip":
            try:
                server = sys.argv[i + 2]
                if server == "auto":
                    server = ""
                else:
                    ipaddress.ip_address(server)
            except:
                sys.exit("Error - Invalid argument for ip, --help for more info")

        elif arg == "-p":
            try:
                port = int(sys.argv[i + 2])
            except:
                sys.exit("Error - Invalid argument for host, --help for more info")

        elif not sys.argv[i] in ["-ip", "-p"]:
            sys.exit("Error - Invalid arguments, --help for more info")

        saveValues(server, port)
