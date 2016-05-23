import re

import src.python.utils as utils

PARAM_REGEX = '\$(\w+)\s*'
PARAMS_OPTION = 'params'
TRIGGER_SECTION = 'TriggerEvent'
TRIGGER_SCRIPT_OPTION = 'triggerscript'
TRIGGER_DELAY_OPTION = 'triggerdelay'
TRIGGER_DELAY_DEFAULT = 5    # In seconds
EVENT_SECTION = 'Event'
EVENT_SCRIPT_OPTION = 'eventscript'
RETRY_COUNT_OPTION = 'retrycount'
RETRY_COUNT_DEFAULT = '3'
USHER_SECTION = 'Usher'
USHER_SCRIPT_OPTION = 'usherscript'
PARAMETER_VALUE_OPTION = 'val'
PARAMETER_SCRIPT_OPTION = 'script'
LOGGING_NAME = 'NotifierConfig'

class NotifierConfig():
    def __init__(self, config, parent_name, log_location):
        self._name = parent_name + ' ' + LOGGING_NAME
        self._log_location = log_location
        self.trigger, self.event, self.usher = (None, None, None)
        self.parameters = dict()

        if config.has_section(TRIGGER_SECTION):
            self.trigger = Trigger(dict(config.items(TRIGGER_SECTION)))
        if config.has_section(EVENT_SECTION):
            self.event = Event(dict(config.items(EVENT_SECTION)))
        if config.has_section(USHER_SECTION):
            self.usher = Usher(dict(config.items(USHER_SECTION)))

        for section in config.sections():
            section_items = dict(config.items(section))
    
            if PARAMETER_VALUE_OPTION in section_items or PARAMETER_SCRIPT_OPTION in section_items:
                self.parameters[section] = Parameter(section_items)

    def get_trigger_command(self):
        script = None

        if self.trigger and self.trigger.script:
             params = self.__substitute_variable_params(self.trigger.param_literal)
             script = self.trigger.script + ' ' + params + self.__logging_params()

        return script

    def get_event_command(self, extra_params=None):
        script = None

        if self.event and self.event.script:
             params = self.__substitute_variable_params(self.event.param_literal,
                                                        extra_params=extra_params)
             script = self.event.script + ' ' + params + self.__logging_params()

        return script

    def get_usher_command(self, extra_params=None):
        script = None

        if self.usher and self.usher.script:
             params = self.__substitute_variable_params(self.usher.param_literal,
                                                        extra_params=extra_params)
             script = self.usher.script + ' ' + params + self.__logging_params()

        return script

    # Gets a parameter from the NotifierConfig's interal parameter dictionary
    # If that parameter has a script associated with it, it will first run that
    # script and set the parameter's value to the result of that script
    def get_param(self, parameter_name):
        parameter_obj = self.parameters.get(parameter_name)
        param_val = None

        if parameter_obj:
            if parameter_obj.script:
                parameter_obj.val = self.__generate_val(self, parameter_name)

            param_val = parameter_obj.val

        return param_val

    def __logging_params(self):
        return ' -pn "' + self._name + '" -log ' + self._log_location

    # Given a param string literal, it will find all of the variables denoted
    # by a '$' and will substitute them with their associated values if they
    # exist. It will first try to get the matched parameter value from
    # the internal param dictionary (parameters defined in .cfg file)
    # and if it does not have it there, it will try to find in extra_params,
    # which is most likely the json response from the step's previous script
    def __substitute_variable_params(self, param_literal, extra_params=None):
        utils.log('Finding params inside: ' + param_literal, self._name,
                  utils.DEBUG, self._log_location)
        param_matches = re.findall(PARAM_REGEX, param_literal, re.M|re.I)
    
        for param_match in param_matches:
            substitute_param = self.get_param(param_match)

            if extra_params:
                substitute_param = extra_params.get(param_match) or substitute_param

            if not substitute_param:
                raise KeyError('Value for parameter "' + param_match + '"' +
                               ' not found in internal config or in extra_params')

            param_literal = re.sub('\$' + param_match, substitute_param, param_literal)
    
        utils.log('Final param literal : ' + param_literal, self._name,
                  utils.DEBUG, self._log_location)
    
        return param_literal

    # Gets a value for a parameter by running its script
    def __generate_val(self, param_name):
        command = self.parameters[param_name].get_command()

        utils.log('Getting value of ' + param_name + ' with command ' + command,
                  self._name, utils.INFO, self._log_location)

        exit_code, stdout, stderr = utils.capture_command_output(command)

        if exit_code == 0:
            utils.log('Param ' + param_name + ' will now be set to ' + stdout,
                      self._name, utils.INFO, self._log_location)
        else:
            # TODO this should throw an exception or something so notifier.py can handle the failure of the script
            exit(666)

        self.val = stdout.strip()
        return self.val

class Trigger():
    def __init__(self, items):
        self.script = items.get(TRIGGER_SCRIPT_OPTION)
        self.delay = float(items.get(TRIGGER_DELAY_OPTION) or TRIGGER_DELAY_DEFAULT)
        self.param_literal = items.get(PARAMS_OPTION)

class Event():
    def __init__(self, items):
        self.script = items.get(EVENT_SCRIPT_OPTION)
        self.retry_count = int(items.get(RETRY_COUNT_OPTION) or RETRY_COUNT_DEFAULT)
        self.param_literal = items.get(PARAMS_OPTION)

class Usher():
    def __init__(self, items):
        self.script = items.get(USHER_SCRIPT_OPTION)
        self.param_literal = items.get(PARAMS_OPTION)

class Parameter():
    def __init__(self, items):
        self.val = items.get(PARAMETER_VALUE_OPTION)
        self.script = items.get(PARAMETER_SCRIPT_OPTION)
        self.script_params = items.get(PARAMS_OPTION)

    def get_command(self):
        return self.script + ' ' + (self.script_params or '')
