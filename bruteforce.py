#!/usr/bin/env python3.8
# -*- coding: UTF-8 -*-

import os
import sys
import json
import base64
import subprocess


def do_param_check(config) -> None:
    """
    Does the configuration check
    :param config: configuration file parsed from base64
    :return: none. Raises exception in case of error
    """
    if "login" not in config or not config["login"]:
        raise Exception("Login dictionary file is not loaded. Please load login.txt")
    if "password" not in config or not config["password"]:
        raise Exception("Password dictionary file is not loaded. Please load password.txt")
    if "ip" not in config or "port" not in config or "service" not in config \
            or "tool" not in config or "bruteforce_threads" not in config:
        raise Exception("Wrong config file provided! " + str(config))


def hydra(config) -> None:
    """
    Runs hydra on a victim specified in the config
    Gives all output to the console
    """
    # Form command-line command for hydra
    command_line = "hydra"
    # Login file is always fixed
    if config["service"].lower() != "vnc":
        command_line += " -L %s" % (os.path.join(config["upload_folder"], "login.txt"))
    # Passwords file is always fixed
    command_line += " -P %s" % (os.path.join(config["upload_folder"], "password.txt"))
    # Add number of threads
    command_line += " -t %s" % config["bruteforce_threads"]
    # Add address
    command_line += " %s://%s:%s" % (config["service"].lower(), config["ip"], config["port"])

    # Run hydra
    print("Command-line command: %s" % command_line)
    process = subprocess.run(command_line, shell=True)


def medusa(config) -> None:
    """
    Runs medusa on a victim specified in the config
    Gives all output to the console
    """
    # Form command-line command for hydra
    command_line = "medusa"
    # Login file is always fixed
    command_line += " -U %s" % (os.path.join(config["upload_folder"], "login.txt"))
    # Passwords file is always fixed
    command_line += " -P %s" % (os.path.join(config["upload_folder"], "password.txt"))
    # Add number of threads
    command_line += " -t %s" % config["bruteforce_threads"]
    # Add address variables
    command_line += " -M %s -h %s -n %s" % (config["service"].lower(), config["ip"], config["port"])

    # Run medusa
    print("Command-line command: %s" % command_line)
    process = subprocess.run(command_line, shell=True)


def ncrack(config) -> None:
    """
    Runs ncrack on a victim specified in the config
    Gives all output to the console
    """
    # Form command-line command for hydra
    command_line = "ncrack -v"
    # Login file is always fixed
    command_line += " -U %s" % (os.path.join(config["upload_folder"], "login.txt"))
    # Passwords file is always fixed
    command_line += " -P %s" % (os.path.join(config["upload_folder"], "password.txt"))
    # Add number of threads
    command_line += " --connection-limit %s" % config["bruteforce_threads"]
    # Add address variables
    command_line += " %s://%s:%s" % (config["service"].lower(), config["ip"], config["port"])

    # Run ncrack
    print("Command-line command: %s" % command_line)
    process = subprocess.run(command_line, shell=True)


def patator(config) -> None:
    """
    Runs patator on a victim specified in the config
    Has specific syntax for every service
    Gives all output to the console
    """
    # Form command-line
    if config["service"].lower() in ["ssh", "ftp", "vnc", "rdp"]:
        command_line = "patator %s_login" % config["service"].lower()
        command_line += " password=FILE0 0=%s" % (os.path.join(config["upload_folder"], "password.txt"))
        if config["service"].lower() != "vnc":
            command_line += " user=FILE1 1=%s" % (os.path.join(config["upload_folder"], "login.txt"))
        command_line += " -t %s" % config["bruteforce_threads"]
        command_line += " host=%s port=%s" % (config["ip"], config["port"])
    elif config["service"].lower() == "telnet":
        command_line = "patator telnet_login inputs='FILE0\nFILE1' prompt_re='Username:|Password:'"
        command_line += " 0=%s" % (os.path.join(config["upload_folder"], "login.txt"))
        command_line += " 1=%s" % (os.path.join(config["upload_folder"], "password.txt"))
        command_line += " -t %s" % config["bruteforce_threads"]
        command_line += " host=%s port=%s" % (config["ip"], config["port"])
    else:
        raise Exception("patator: wrong service name")

    # Run patator
    print("Command-line command: %s" % command_line)
    process = subprocess.run(command_line, shell=True)


def command_line_runner():
    if len(sys.argv) != 3:
        raise Exception("Wrong number of arguments! Usage: python bruteforce.py php_answer path_to_upload")

    # Read config from argv
    config = json.loads(base64.b64decode(sys.argv[1]))
    config["upload_folder"] = sys.argv[2]
    do_param_check(config)

    # Run the program
    print("Running %s..." % config["tool"])
    if config["tool"].lower() == "hydra":
        hydra(config)
    if config["tool"].lower() == "medusa":
        medusa(config)
    if config["tool"].lower() == "ncrack":
        ncrack(config)
    if config["tool"].lower() == "patator":
        patator(config)


if __name__ == "__main__":
    command_line_runner()
