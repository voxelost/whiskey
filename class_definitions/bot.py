import discord
from class_definitions.command import DiscordCommand


class Bot(discord.Client):
    def __init__(self, config: dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.token = config['discord_token']
        self.prefix = config.get('prefix', './')
        self.owner_id = config['owner_id']
        self.default_auth_func = kwargs.get(
            'default_auth_func', lambda: None),
        self.default_error_handler = kwargs.get(
            'default_error_handler', lambda: None)

        # self.commands = []
        self.command_dict = {}

    async def on_message(self, message: discord.Message):
        self.log(message)

        if message.author == self.user or message.author.bot:
            return

        await self.try_command(message)

    def log(self, message: discord.Message) -> None:
        print(message)

    def command(self, triggers=None, auth_func=None, error_handler=None, required_arguments=0):
        triggers = [] if not triggers else triggers

        def inner(func):
            for x, _ in enumerate(triggers):
                triggers[x] = triggers[x].lower()

            new_command = DiscordCommand(
                triggers=triggers,
                func=func,
                auth_func=self.default_auth_func if auth_func is None else auth_func,
                error_handler=self.default_error_handler if error_handler is None else error_handler
            )

            for t in triggers:
                """newer triggers will overwrite older ones"""
                self.command_dict[t] = new_command

            # self.commands.append(new_command)

            return func
        return inner

    def get_commands_list(self) -> list:
        return list(set([self.command_dict[k] for k in self.command_dict]))

    def parse_command(self, raw_command: str) -> dict:
        command_split = raw_command.split()
        command = command_split[0].lstrip(
            self.prefix) if len(command_split) > 0 else ""

        command_arguments = command_split[1:] if len(command_split) > 1 else []

        if ' ' in raw_command:
            first_space_idx = raw_command.index(' ')
            arguments_raw = raw_command[first_space_idx +
                                        1:] if len(raw_command) > first_space_idx else ''
        else:
            arguments_raw = ''

        return {
            'prefix': self.prefix,
            'command': command,
            'arguments': command_arguments,
            'raw': raw_command,
            'arguments_raw': arguments_raw
        }

    def identify_command(self, command_parsed: tuple):
        command_str = command_parsed['command']
        if command_str not in self.command_dict:
            return None

        cmd = self.command_dict[command_str]
        if cmd.should_trigger(command_str, command_parsed['arguments']):
            return cmd

        return None

    async def try_command(self, message: discord.Message) -> None:
        if not message.content.startswith(self.prefix):
            return

        command_parsed = self.parse_command(message.content)
        cmd = self.identify_command(command_parsed=command_parsed)

        if cmd:
            await self.invoke_command(message=message, command=cmd, command_parsed=command_parsed)

    async def invoke_command(self, message: discord.Message, command: DiscordCommand, command_parsed: dict):
        await command.trigger(message=message, command_parsed=command_parsed, command=command, bot=self)
