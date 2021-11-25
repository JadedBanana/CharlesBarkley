async def send_log(self, message, argument, is_in_guild):
    """
    Sends a log file through discord.
    Argument should be formatted in YYYY-MM-DD.
    """
    # If there is no argument, we simply grab today's log file.
    is_today = not argument
    if is_today:
        target_log = datetime.today().strftime('%Y-%m-%d') + '.txt'

    # Otherwise, we grab the argument and try to work it into a good target log.
    else:
        # Normalizing the string
        argument_slim = misc.normalize_string(argument)
        for i in range(len(argument_slim) - 1, -1, -1):
            if argument_slim[i] not in string.digits:
                argument_slim = argument_slim[:i] + argument_slim[i + 1:]

        # If the length of our argument isn't now 8, we tell the user that and return.
        if len(argument_slim) != 8:
            log.debug(misc.get_comm_start(message, is_in_guild) + 'Ordered log file, invalid date')
            await message.channel.send('Invalid date format. Should be YYYY-MM-DD')
            return

        # Now, we form a date.
        target_log = '{}-{}-{}.txt'.format(argument_slim[:4], argument_slim[4:6], argument_slim[6:8])
        is_today = target_log == datetime.today().strftime('%Y-%m-%d') + '.txt'

    # We see if that log file exists.
    if os.path.isfile(os.path.join(constants.LOGS_DIR, target_log)) or is_today:
        # Log then send file.
        log.info(misc.get_comm_start(message, is_in_guild) + 'Ordered log file {}, sending'.format(target_log))
        await message.channel.send(file=discord.File(os.path.join(constants.LOGS_DIR, target_log)))

    # If the log file doesn't exist, we tell the user that.
    else:
        log.debug(misc.get_comm_start(message, is_in_guild) + 'Ordered log file, file {} does not exist'.format(target_log))
        await message.channel.send('Log file {} does not exist.'.format(target_log))