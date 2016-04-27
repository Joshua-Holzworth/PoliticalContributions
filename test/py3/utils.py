import src.py3.utils as utils

def __contains_count(command, string_to_check, check_stderr):
    exit_code, stdout, stderr = utils.capture_command_output(command);
    output = stderr if check_stderr else stdout

    contains_count = len(output.split(string_to_check)) - 1  
    return exit_code, output, contains_count
    
def output_contains_at_least(command, string_to_check, contains_count_min, check_stderr=False):
    exit_code, output, contains_count = __contains_count(command, string_to_check, check_stderr)
    test_passed = contains_count >= contains_count_min

    return test_passed, exit_code, output, contains_count

def output_contains_exactly(command, string_to_check, contains_count_min, check_stderr=False):
    exit_code, output, contains_count = __contains_count(command, string_to_check, check_stderr)
    test_passed = contains_count == contains_count_min

    return test_passed, exit_code, output, contains_count

def output_contains_less_than_or_equal_to(command, string_to_check, contains_count_max, check_stderr=False):
    exit_code, output, contains_count = __contains_count(command, string_to_check, check_stderr)
    test_passed = contains_count <= contains_count_max

    return test_passed, exit_code, output, contains_count

def output_contains_less_than(command, string_to_check, contains_count_ceil, check_stderr=False):
    exit_code, output, contains_count = __contains_count(command, string_to_check, check_stderr)
    test_passed = contains_count < contains_count_ceil

    return test_passed, exit_code, output, contains_count

def output_contains_more_than(command, string_to_check, contains_count_floor, check_stderr=False):
    exit_code, output, contains_count = __contains_count(command, string_to_check, check_stderr)
    test_passed = contains_count > contains_count_floor

    return test_passed, exit_code, output, contains_count

def predicate_on_output(command, predicate, check_stderr=False):
    exit_code, stdout, stderr = utils.capture_command_output(command);
    output = stderr if check_stderr else stdout
    test_passed = predicate(output)

    return test_passed, exit_code, output
