# Utility logging file
# Imports
import os
import constants
from datetime import datetime

class JLogger:
	
	# Levels
	DEBUG = 0
	INFO = 1
	WARNING = 2
	ERROR = 3
	CRITICAL = 4
	LEVEL_HEADERS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
	
	# Current vars
	current_log_level = constants.DEFAULT_LEVEL
	log_to_console = constants.LOG_TO_CONSOLE
	log_to_file = constants.LOG_TO_FILE
	do_level_headers = constants.DO_LEVEL_HEADERS
	do_timestamps = constants.DO_TIMESTAMPS
	
	def change_log_level(self, level):
		pass

	# Basic wrappers for log() function
	def debug(self, msg): self.log(msg, self.DEBUG)
	def info(self, msg): self.log(msg, self.INFO)
	def warning(self, msg): self.log(msg, self.WARNING)
	def error(self, msg): self.log(msg, self.ERROR)
	def critical(self, msg): self.log(msg, self.CRITICAL)

	def log(self, msg, level):
		"""Does the log, to file and/or console, with fitting prefix"""
		# Immediately returns if the log level is below what is required to do a log
		if level < self.current_log_level: 
			return
			
		# Get the string version of msg, then list version
		msg = str(msg).split('\n')
		
		# Gets current datetime if we're going to a file or we've got timestamps
		if self.do_timestamps or self.log_to_file:
			today = datetime.today()
			
		# Creates message prefix
		msg_prefix = ''
		today = datetime.today()
		if self.do_timestamps:
			temptime = today.strftime('%H:%M:%S')
			msg_prefix+= f'[{temptime}] '
		if self.do_level_headers:
			msg_prefix+= self.LEVEL_HEADERS[level] + ': '
		
		# Logs to console
		if self.log_to_console:
			for m in msg:
				if m:
					print(msg_prefix + m)
				else:
					print('\n')
		
		# Logs to file
		if self.log_to_file:
			if not os.path.isdir(constants.LOGS_DIR):
				os.mkdir(constants.LOGS_DIR)
			log_file = open(os.path.join(constants.LOGS_DIR, today.strftime('%Y-%m-%d') + '.txt'), 'a')
			for m in msg:
				if m:
					log_file.write(msg_prefix + m + '\n')			
				else:
					log_file.write('\n')
			log_file.close()
		
