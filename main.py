
from io import StringIO
from contextlib import redirect_stdout
import os
import json


from class_definitions.bot import Bot
from commands.error_handlers import default_error_handler
from commands.auth_commands import anyone_anywhere, owner_only


def load_config(config_file='./config.json') -> dict:
    with open(config_file) as fptr:
        return json.loads(fptr.read())


bot = Bot(
    config=load_config(),
    default_auth_func=anyone_anywhere,
    default_error_handler=default_error_handler
)


@bot.command(triggers=['sys', 'system', 'os'], auth_func=owner_only)
async def system_command(command_parsed: dict, *args, **kwargs):
    # # system_command.__doc__ = 'testin'
    # setattr(system_command, '__doc__', f'ninja')

    with os.popen(command_parsed['arguments_raw']) as p:
        yield p.read().strip()


@bot.command(triggers=['exec', 'execute'], auth_func=owner_only)
async def execute(command_parsed: dict, *args, **kwargs):
    """execute a python command using exec()"""

    stdout_buffer = StringIO()
    with redirect_stdout(stdout_buffer):
        exec(command_parsed['arguments_raw'], globals())

    yield stdout_buffer.getvalue()


@ bot.command(triggers=['help'], auth_func=anyone_anywhere)
async def print_help(bot: Bot, *args, **kwargs):
    """prints this message"""
    out = ''

    for cmd in bot.get_commands_list():
        out += f'triggers: {cmd._triggers}\n'
        out += f'security: {cmd._auth_func.__doc__}\n'
        out += f'{cmd._func.__doc__}\n'
        out += '\n'

    yield out

if __name__ == '__main__':
    bot.log('starting...')
    bot.run(bot.token)
