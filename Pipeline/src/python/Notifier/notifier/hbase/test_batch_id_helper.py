#!/usr/bin/python -B
import pprint

from connector import Connector
from data_access_layer import DataAccessLayer

def main():
    pp = pprint.PrettyPrinter(indent=2, width=1)

    helper = DataAccessLayer(Connector('localhost'), 'contributions_pipeline')

    current_lz_batch_id = int(helper.get_latest_batch_id('lz'))
    latest_lz_batch = helper.get_step_batch('lz', current_lz_batch_id)
    previous_lz_batch = helper.get_step_batch('lz', current_lz_batch_id + 1)

    print('Latest lz batch: ')
    pp.pprint(latest_lz_batch)
    print('Previous lz batch: ')
    pp.pprint(previous_lz_batch)

    raw_input('Press Enter')
    print('\nPZ batch: ')
    pp.pprint(helper.get_latest_step_batch('pz'))
    raw_input('Press Enter')
    print('Starting PZ step')
    helper.set_step_to_running('pz', 'test run')
    print('\nPZ batch: ')
    pp.pprint(helper.get_latest_step_batch('pz'))

    raw_input('Press Enter')
    print('\nStopping PZ step')
    helper.set_step_to_stopped('pz', 'manually stopped')
    print('\nPZ batch: ')
    pp.pprint(helper.get_latest_step_batch('pz'))

    raw_input('Press Enter')
    print('\nRestarting pz step')
    helper.set_step_to_running('pz', 'restart test run')
    print('\nPZ batch: ')
    pp.pprint(helper.get_latest_step_batch('pz'))

if __name__ == '__main__':
    main()
