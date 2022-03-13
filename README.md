# whiskey

Discord bot micro-framework allowing for easy to write asynchronous commands.

An example command will look like this:
```py
@bot.command(triggers=['hello', 'example'])
async def hello_world(*args, **kwargs):
    """an example discord command"""

    yield 'hi from within the command'
    # do some operations
    
    yield 'another response within the same command'
```

An example config file can be found [here](https://github.com/voxelost/whiskey/blob/master/example.config.json).
