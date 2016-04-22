import subprocess
import shlex

def run_command(command):
    process = subprocess.run(shlex.split(command), stderr=subprocess.PIPE)
    stdout = process.stdout
    stderr = process.stderr
    
    if stdout:
        stdout = stdout.decode('utf-8') 
    if stderr:
        stderr = stderr.decode('utf-8')

    return stdout, stderr

def __contains_count(command, string_to_check, check_stderr):
    stdout, stderr = run_command(command);
    output = stderr if check_stderr else stdout

    contains_count = len(output.split(string_to_check)) - 1  
    return output, contains_count
    
def output_contains_at_least(command, string_to_check, contains_count_min, check_stderr=False):
    output, contains_count = __contains_count(command, string_to_check, check_stderr)
    test_passed = contains_count >= contains_count_min

    return test_passed, output, contains_count

def output_contains_exactly(command, string_to_check, contains_count_min, check_stderr=False):
    output, contains_count = __contains_count(command, string_to_check, check_stderr)
    test_passed = contains_count == contains_count_min

    return test_passed, output, contains_count

def output_contains_less_than_or_equal_to(command, string_to_check, contains_count_max, check_stderr=False):
    output, contains_count = __contains_count(command, string_to_check, check_stderr)
    test_passed = contains_count <= contains_count_max

    return test_passed, output, contains_count

def output_contains_less_than(command, string_to_check, contains_count_ceil, check_stderr=False):
    output, contains_count = __contains_count(command, string_to_check, check_stderr)
    test_passed = contains_count < contains_count_ceil

    return test_passed, output, contains_count

def output_contains_more_than(command, string_to_check, contains_count_floor, check_stderr=False):
    output, contains_count = __contains_count(command, string_to_check, check_stderr)
    test_passed = contains_count > contains_count_floor

    return test_passed, output, contains_count

def predicate_on_output(command, predicate, check_stderr=False):
    stdout, stderr = run_command(command);
    output = stderr if check_stderr else stdout
    test_passed = predicate(output)

    return test_passed, output
