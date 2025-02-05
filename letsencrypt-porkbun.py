#!/usr/bin/env python3

import logging
import os
import sys

import requests

# https://porkbun.com/api/json/v3/documentation
DEFAULT_API_URL = "https://api.porkbun.com/api/json/v3"
DEFAULT_CERTIFICATE_PATH = "/ssl/fullchain.pem"
DEFAULT_PRIVATE_KEY_PATH = "/ssl/privkey.pem"

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"


def main() -> None:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

    domain = getenv_or_exit("DOMAIN")
    api_key = getenv_or_exit("API_KEY")
    secret_key = getenv_or_exit("SECRET_KEY")

    logging.info(f"Downloading SSL bundle for {domain}")
    url = os.getenv("API_URL", DEFAULT_API_URL) + "/ssl/retrieve/" + domain
    r = requests.post(url, json={"apikey": api_key, "secretapikey": secret_key})

    os.umask(0o066)

    data = r.json()
    if data["status"] == "ERROR":
        logging.error(data["message"])
        sys.exit(1)

    certificate_path = os.getenv("CERTIFICATE_PATH", DEFAULT_CERTIFICATE_PATH)
    logging.info(f"Saving certificate chain to {certificate_path}")
    with open(certificate_path, "w") as f:
        f.write(data["certificatechain"])

    private_key_path = os.getenv("PRIVATE_KEY_PATH", DEFAULT_PRIVATE_KEY_PATH)
    logging.info(f"Saving private key to {private_key_path}")
    with open(private_key_path, "w") as f:
        f.write(data["privatekey"])

    logging.info("SSL certificate has been successfully downloaded")


def getenv_or_exit(key: str) -> str:
    value = os.getenv(key)
    if value is not None:
        return value

    logging.error(f"{key} is required but not set")
    sys.exit(1)


if __name__ == "__main__":
    main()
