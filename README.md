# whose-name API client

This is a client for the [whose-name](https://github.com/makimo/whose-name) API.

It answers questions of the following form:

> For one that calls themselves `test@example.org` on `jira`, what is their username on Slack? (Answer: `U123456`).

# Installation

To install the code globally, use:

```
sudo pip3 install .
```

To add this to pip `requirements.txt` file, use:

```
-e git+ssh://git@github.com:makimo/whose-name-client.git#egg=whosename-main
```

To add this to `setup.py`, try [this answer](https://stackoverflow.com/questions/32688688/how-to-write-setup-py-to-include-a-git-repository-as-a-dependency):

```python
install_requires = [
  'whosename @ git+ssh://git@github.com/makimo/whose-name-client@v1.1#egg=whosename-main',
]
```



# Console usage

There are two commands that can be used in shell: `whosename` and `whosename-login`. When used on your own machine, you can simply issue the following command:

```
whosename user service askedService
```

First time, you'll be asked interactively for email and password to the whose-name API in order to get a token. Subsequent calls will make use of the saved token.

If you would only want to issue a token, you can do that with the `whosename-login` command. This comes in useful on servers that need access to the API.

## whosename (1.0)

```
Whose name client.

Usage:
    whosename [options] USERNAME SERVICE ASKED_SERVICE

Options:
    -n          Non-interactive mode.
    -t, --token TOKEN  Use authorization token.
    --version   Show version information.
    -h, --help  Show this message.
```

## whosename-login (1.0)

```
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
```

# Python usage

This package defines the following function:

```python
def name_of(
    username: str, 
    service: str, 
    askedService: str, 
    authToken: Optional[str] = None,
    interactive: bool = False
) -> Optional[str]:
```

where:

- `username` and `service` match one's username on a known service
- `askedService` is the service on which we want to know one's username
- `authToken` can be given explicitely (for example if you want to get the value from a database or another specific place)
- `interactive` will ask for whosename API login and password to request a token if not found

The result is one's username on `askedService` or None if not found.

# Tokens

`whosename` will try to find the token in the following places:

1. `--token` console option or `authToken` argument
2. `WHOSENAME_TOKEN` in the environment
3. `WHOSENAME_TOKEN_FILE` in the environment
4. `.whosename.token` in current directory and upwards
5. `~/.whosename/token` in user's home directory
6. `/etc/whosename/token`

If token cannot be found in any of these places, the application will ask for it interactively.