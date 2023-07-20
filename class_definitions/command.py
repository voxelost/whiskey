import discord


class DiscordCommand():
    def __init__(self,
                 triggers: list,
                 func=lambda: None,
                 required_arguments=0,
                 auth_func=lambda: None,
                 error_handler=lambda: None) -> None:

        self._triggers = triggers
        self._required_arguments = required_arguments
        self._auth_func = auth_func
        self._func = func
        self._error_handler = error_handler

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            triggers=d.get('triggers', []),
            func=d.get('func', lambda: None),
            required_arguments=d.get('required_arguments', 0),
            auth_func=d.get('auth_func', lambda: None),
            error_handler=d.get('error_handler', lambda: None),
        )

    def should_trigger(self, cmd: str, cmd_args: list) -> bool:
        return cmd in self._triggers and \
            (len(cmd_args) >= self._required_arguments)

    def generate_response_str(self, inp: str):
        if not inp:
            return

        MAX_MESSAGE_LEN = 2000
        for resp in [inp[i: i + MAX_MESSAGE_LEN - 8] for i in range(0, len(inp), MAX_MESSAGE_LEN - 8)]:
            yield f'```\n{resp}\n```'

    async def trigger(self, message: discord.Message, command_parsed: tuple, command, bot):
        try:
            await self._auth_func(message=message, command_parsed=command_parsed, command=command, bot=bot)

            command_generator = self._func(
                message=message, command_parsed=command_parsed, command=command, bot=bot)

            while(True):
                try:
                    command_output = await command_generator.__anext__()

                    for resp_str in self.generate_response_str(command_output):
                        await message.channel.send(resp_str)

                except StopAsyncIteration:
                    break

        except Exception as e:
            await self._error_handler(message=message, command_parsed=command_parsed, command=command, bot=bot, exception=e)
