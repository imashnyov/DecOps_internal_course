import argparse
import string
import random
import re
import logging
from functools import wraps
from typing import List

logging.basicConfig(level=logging.CRITICAL)

small_lateral = string.ascii_lowercase  # set of little literal
big_lateral = string.ascii_uppercase  # set of big literal
digits = string.digits  # set of big digits
punctuation = string.punctuation  # set of big symbols

# mapping for generation random token-password
mapping = {
    'A': big_lateral,
    'a': small_lateral,
    'd': digits,
    'p': punctuation,
    '-': '-',
    '@': '@'
}

# mapping for log levels
log_levels = {
    0: logging.ERROR,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG,
}

# decorating a function for logging (debug level, -vvv)
def function_logging(func):
    """Decorator that add logging for function
    """
    @wraps(func)
    def wraper(*args, **kwargs):
        logging.debug(
            f'Called {func.__name__}.\n With args:{args} kwargs:{kwargs}')
        return func(*args, **kwargs)
    return wraper


# generation random password for flag "-l"
@function_logging
def generate_random_password(lenght: int) -> str:
    """Generate random password

    Args:
        lenght (int): password length

    Returns:
        str: random password 
    """
    available_symbvol = small_lateral+big_lateral+digits
    result = ''.join(random.choices(available_symbvol, k=lenght))
    logging.info(f"Generated random password with length={lenght}.")
    return result

# generation random password by template "-t"
@function_logging
def generate_from_template(template: str) -> str:
    """Generate a password for provided template

    Args:
        template (str): template

    Returns:
        str: generated password
    """
    try:
        result = re.finditer(
            r'((?P<token_type>[a-zA-Z@-]|\[.*\])(?P<count>\d+)?)', template)  # parser  module re
        res_string = ''
        for match in result:
            token_type = match.groupdict().get('token_type')
            count = match.groupdict().get('count')
            count = 1 if count is None else int(count)
            sequence = get_token_sequence(token_type)
            res_string += ''.join(random.choices(sequence, k=count))
        logging.info(f"Generated password for template '{template}'.")
        return res_string
    except TypeError:
        logging.error(f"Wrong template '{template}' !")

# get random symbols corresponding to the token in the mapping
@function_logging
def get_token_sequence(token: str) -> str:
    """Return sequence ok symbols for provided token

    Args:
        token (str): token

    Returns:
        str: sequence of symbols for token
    """
    if token.startswith('['):
        token = token.strip('[]').replace('%', '')
    return ''.join([mapping.get(t) for t in token])


@function_logging
def generate_from_file(file_path: str) -> List[str]:
    """Generate passwords for templates provided in file

    Args:
        file_path (str): file path

    Returns:
        List[str]: list of generated passwords
    """
    try:
        with open(file_path, 'r') as file:  # context manager
            # list comprehension
            return [generate_from_template(line) for line in file]
    except FileNotFoundError:
        logging.error(f"File '{file_path}' doesn\'t exist")


def main():
    parser = argparse.ArgumentParser(description='Utility for generating passwords according to a given template that supports the \
                                                  CLI interface and logging', epilog="The developer: Mashnov Illia (2021)")
    parser.add_argument('-l', dest='length', type=int,
                        help='use -l for point on length of password')
    parser.add_argument('-t', dest='template', type=str,
                        help='use -t for point on template for generate passwords. Tokens must consist of two part <type_token> and <count>. \
                            Type of token: "a"-small lateral, "A"-big lateral, "d"-digit, "p"-punctuations, "-"-same symbol, \
                                "@"-same symbol, "[]"-set type of token.')
    parser.add_argument('-c', dest='number', type=int,
                        help='the number of passwords you want to generate')
    parser.add_argument('-f', dest='file', type=str,
                        help='path to a file containing templates for generating passwords')
    parser.add_argument('-v', action='count', dest='log_level', default=0)

    args = parser.parse_args()  # parsed the passed argument and send to the variable

    level = log_levels.get(args.log_level, logging.ERROR)
    logging.getLogger().setLevel(level=level)

# part for flag "-f"
    if args.file is not None:
        print(*generate_from_file(args.file), sep='\n')
    else:
        # part for flag "-с"
        for _ in range(args.number if args.number else 1):  # ternary operator
            # part for flag "-l"
            if args.length is not None:
                print(generate_random_password(args.length))
# part for flag "-t"
            elif args.template is not None:
                print(generate_from_template(args.template))


if __name__ == "__main__":
    main()
