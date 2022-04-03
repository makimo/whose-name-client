"""
Get token for whosename

Usage:
    whosename-login [options] [EMAIL]

Options:
    -n          Non-interactive mode.
    -t TITLE    Set title for a token.
    -o OUTPUT   Save token to a specific file.
    --password PASS  Use specific password
    --version   Show version information.
    -h, --help  Show this message.
"""

VERSION = '1.0'


from typing import Optional

from pathlib import Path

import getpass
import platform

from docopt import docopt
import requests

from .defs import DOMAIN


def save_token(filename, token):
    path = Path(filename).expanduser()

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w') as f:
        f.write(token)


def input_until_valid(
    prompt,
    message,
    check=lambda x: x != '',
    default=None,
    default_prompt="{prompt} [{default}]: "
):
    if default:
        prompt = default_prompt.format(
            prompt=prompt.strip(': '),
            default=default,
        )

    while True:
        s = input(prompt)

        if s == '' and default:
            s = default

        if check(s):
            return s

        print(message)


def getpass_until_valid(
    prompt,
    message,
    check=lambda x: x != '',
    default=None,
    default_prompt="{prompt} [*****]: "
):
    if default:
        prompt = default_prompt.format(
            prompt=prompt.strip(': ')
        )

    while True:
        s = getpass.getpass(prompt)

        if s == '' and default:
            s = default

        if check(s):
            return s

        print(message)


def default_token_title():
    return "{}@{}".format(
        getpass.getuser(),
        platform.node()
    )


def interactively_request_token(
    email: Optional[str] = None, 
    password: Optional[str] = None,
    title: Optional[str] = None,
    abilities: Optional[list[str]] = None,
) -> str:
    
    if not email:
        email = input_until_valid(
            "E-mail: ", 
            "Please provide an email",
        )
    
    if not password:
        password = getpass_until_valid(
            "Password: ",
            "Please write your password"
        )
    
    if not title:
        title = input_until_valid(
            "Token name: ",
            "A token name should describe where token should be used",
            default=default_token_title()
        )
    
    return request_token(
        email,
        password,
        title,
        abilities
    )

def request_token(
    email: str, 
    password: str,
    title: Optional[str] = None,
    abilities: Optional[list[str]] = None,
) -> str:

    url = '{}/api/request-token'.format(DOMAIN)

    headers = {
        'Accept': 'application/json',
    }

    payload = {
        'email': email,
        'password': password,
        'title': title or default_token_title(),
        'abilities': abilities
    }

    r = requests.post(
        url,
        json=payload,
        headers=headers
    )

    if r.status_code != 201:
        raise RuntimeError(r.json())
    
    j = r.json()

    return j['token']


def main():
    arguments = docopt(__doc__, version=VERSION)

    if not arguments['-n']:
        func = interactively_request_token
    else:
        func = request_token

    token = func(
        arguments['EMAIL'],
        arguments['--password'],
        arguments['-t'],
        ['whose-name']
    )

    filename = arguments['-o'] or '~/.whosename/token'

    save_token(filename, token)

    print("Token saved to {}".format(filename))