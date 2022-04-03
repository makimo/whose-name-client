"""
Whose name client.

Usage:
    whosename [options] USERNAME SERVICE ASKED_SERVICE

Options:
    -n          Non-interactive mode.
    -t, --token TOKEN  Use authorization token.
    --version   Show version information.
    -h, --help  Show this message.
"""

VERSION = '1.0'

from docopt import docopt

from typing import Optional

import requests

import subprocess

import os, sys

from .defs import DOMAIN

def find_file_upwards(name, path=None, fail_silently=False):
        """Find file in the path directory or in directories above."""

        last_directory = None
        current_directory = path or os.getcwd()

        while current_directory != last_directory:
            file_path = os.path.join(current_directory, name)
            if os.path.exists(file_path):
                return file_path

            last_directory = current_directory
            current_directory = os.path.dirname(last_directory)

        if fail_silently:
            return None

        raise RuntimeError("File not found in this directory (or any of the parent directories): %s" % name)


def read_token_from_file(file):
    with open(file) as f:
        return f.read().strip()


def discover_token(interactive: bool = False) -> str:
    if 'WHOSENAME_TOKEN' in os.environ:
        return os.environ['WHOSENAME_TOKEN']

    try_files = [
        os.environ.get('WHOSENAME_TOKEN_FILE'),
        find_file_upwards('.whosename.token', fail_silently=True),
        os.path.expanduser('~/.whosename/token'),
        '/etc/whosename/token'
    ]

    for file in filter(None, try_files):
        if os.path.exists(file):
            return read_token_from_file(file)

    if not interactive:
        raise ValueError("Token not set")
    
    subprocess.check_call(['whosename-login'])

    return discover_token(interactive=False)


def name_of(
        username: str, 
        service: str, 
        askedService: str, 
        authToken: Optional[str] = None,
        interactive: bool = False
    ) -> Optional[str]:

    if not authToken:
        authToken = discover_token(interactive)
    
    if not authToken:
        raise ValueError("Auth Token is unknown")

    url = '{}/api/whose-name/query'.format(DOMAIN)

    headers = {
        'Authorization': 'Bearer ' + authToken,
        'Accept': 'application/json',
    }

    r = requests.get(url, params={
        'u': username,
        's': service,
        'q': askedService,
    }, headers=headers)

    j = r.json()

    if r.status_code != 200:
        raise RuntimeError(j)

    return j['username']


def main():
    arguments = docopt(__doc__, version=VERSION)

    name = name_of(
        arguments['USERNAME'],
        arguments['SERVICE'],
        arguments['ASKED_SERVICE'],
        arguments['--token'],
        sys.stdout.isatty() and not arguments['-n']
    )

    print(name)