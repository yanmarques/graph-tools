"""
    This module provides some helper functions for reading specified formats
    from user input. But also for pretty output.
"""


class RateLimitExceeded(Exception): pass


class ValidationException(Exception): pass


def read_text(message,
              max_attempts=2,
              default=None,
              validation=None,
              throlling_message=None):
    text = None
    attempts = 0
    formatted_msg = f'{message}> '
    
    try:
        while text is None or text == '':
            text = input(formatted_msg)
            attempts += 1
            if len(text):
                text = validation(text) if validation is not None else text
            elif attempts >= max_attempts:
                raise RateLimitExceeded(throlling_message)
    except Exception as exc:
        print(f'[*] {str(exc)}')
        if isinstance(exc, ValidationException):
            remaining_attempts = max_attempts - attempts
            text = None
            if remaining_attempts >= 0:
                return read_text(message,
                                 max_attempts=remaining_attempts,
                                 default=default,
                                 validation=validation,
                                 throlling_message=throlling_message)
    if text is None or text == '':
        return default
    return text


def read_int(message, **kwargs):
    return read_by_function(message, int, 'Value must be an integer.', **kwargs)


def read_float(message, **kwargs):
    return read_by_function(message, float, 'Value must be a number.', **kwargs)


def read_by_function(message, convert_function, validation_msg, **kwargs):
    def validator(text):
        try:
            return convert_function(text)
        except ValueError:
            raise ValidationException(validation_msg)

    return read_text(message, validation=validator, **kwargs)


def read_choices(message, choices, default=0, **kwargs):
    choice_msg = '|'.join(choices)
    choices = enumerate(choices)

    def chooser(text):
        for index, choice in choices:
            if choice.lower().startswith(text.lower()):
                return index
        raise ValidationException(f'Value must be one of [{choice_msg}].')

    return read_text(f'{message} [{choice_msg}]',
                     validation=chooser,
                     default=default,
                     **kwargs)


def prompt_forever(message, return_value):
    binary_choices = ['yes', 'no']
    can_continue = False
    while not can_continue:
        value = return_value()
        print(value)
        choice = read_choices(message, binary_choices,
                        throlling_message='Assuming everything is ok...')
        can_continue = choice == 0
    return value


def show_banner(text, separator='#'):
    line_size = len(text) * 2
    fmt = format_sized(':^', line_size)
    line_size += 2
    print(separator * line_size)
    display(fmt.format(text), separator=separator)
    print(separator * line_size)


def display(text, separator='#'):
    print(f'{separator}{text}{separator}')


def format_sized(string_fmt, size):
    return '{' + string_fmt + str(size) + '}'


def display_table(section, keys, table, lines=None, end="\n"):
    header_sep = ' | '
    header_sep_size = len(header_sep)

    headers = header_sep.join(keys)

    # pad left and right with space
    headers = f' {headers}'
    headers = f'{headers} '

    header_size = len(headers)

    if lines is not None:
        # take a copy for changing
        keys, lines = keys.copy(), lines.copy()

        largest_line = len(max(lines)) + 2

        line_separator = '|'
        empty_header = f"{' ' * (largest_line)}" + line_separator

        headers = empty_header + headers
        header_size = len(headers)
        line_fmt = format_sized(':^', largest_line - len(line_separator))

    def fill_line(separator='#'):
        display(f'{separator * header_size}')

    def display_padded(string_fmt, text):
        fmt = format_sized(string_fmt, header_size)
        display(fmt.format(text))

    fill_line()
    display_padded(':^', section)

    fill_line(separator='-')
    display(headers)
    fill_line(separator='-')


    for table_index, items in enumerate(table):
        line = ''
        last_index = len(items) - 1

        for key_index, value in enumerate(items):
            key_size = len(keys[key_index])

            if key_index != last_index: # decrements one time
                 key_size += header_sep_size
            else:
                key_size += 2

            formatted_line = format_sized(':^', key_size).format(value)

            if key_index == 0 and lines is not None:
                new_line = line_fmt.format(lines[table_index])
                formatted_line = ' ' + new_line + line_separator + formatted_line

            line += formatted_line
        display(line)
    fill_line()
    print(end=end)
