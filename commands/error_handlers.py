
async def default_error_handler(message, exception, **kwargs):
    await debug_error_handler(message, exception, **kwargs)


async def debug_error_handler(message, exception: Exception, **kwargs):
    await message.channel.send(f'```css\n[error: {exception}]\n```')
    print(message, exception)
