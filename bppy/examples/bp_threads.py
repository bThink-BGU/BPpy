from time import sleep, perf_counter
import time
from threading import Thread, Condition
from bppy import *
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

NUM_OF_BTHREADS = 1
c_synced_bthreads = Condition()
threads_to_events = {}

selected_event = [-1]

threads_to_locks_and_events = {}

def everyone_synchornized(threads_to_events):
    num_of_synched_scenarios = 0
    for k, v in threads_to_events.items():
        if v != "":
            num_of_synched_scenarios = num_of_synched_scenarios + 1
    ans = num_of_synched_scenarios == NUM_OF_BTHREADS
    return ans

def select_event(selected_event) -> object:
    selected_event[0] = random.randrange(10)
    return

def selector( cv_1 , threads_to_events, threads_to_locks_and_events ):
    logging.debug('Enter selector')
    j = 0
    while j < 5:
        cv_1.acquire()
        while not everyone_synchornized(threads_to_events):
            logging.debug('Waiting for all the threads to synchronize')
            cv_1.wait()
        events = []
        for key in threads_to_events:
            events.append(threads_to_events[key])
            threads_to_events[key] = ""
        logging.debug(f'selector received events: {events}')
        cv_1.release()

        if events:
            threads_to_locks_and_events[0][0].acquire()
            logging.debug(f'Notifiying on event: {events[0]}')
            threads_to_locks_and_events[0] = ( threads_to_locks_and_events[0][0], events[0])
            threads_to_locks_and_events[0][0].notify()
            threads_to_locks_and_events[0][0].release()

        j = j + 1

def is_empty_event(id, threads_to_locks_and_events):
    ans = len(threads_to_locks_and_events[id][1]) == 0
    return ans

def add_external_events( id, cv_1, threads_to_events,threads_to_locks_and_events):
    logging.debug('Starting add_external_events')
    i = 0
    while i < 5:
        cv_1.acquire()
        requested_event = "event("+str(i)+")"
        threads_to_events[id] = requested_event
        logging.debug(f'bThread: {id} requested: {threads_to_events[id]}')
        cv_1.notify()
        cv_1.release()

        threads_to_locks_and_events[id][0].acquire()
        while is_empty_event(id, threads_to_locks_and_events):
            threads_to_locks_and_events[id][0].wait()
        selected_event = threads_to_locks_and_events[id][1]
        logging.debug(f'bThread: {id} received event: {selected_event}')
        threads_to_locks_and_events[id] = (threads_to_locks_and_events[id][0], '')
        threads_to_locks_and_events[id][0].release

        i += 1

def wait_for_external_events():
    print('Starting wait_for_external_events')
    i = 0
    while i < 100:
        print("Waiting for event(" ,i, ")")
        i += 1

if __name__ == "__main__":
    threads_to_locks_and_events = {}
    c_scenario_lock = Condition()
    threads_to_locks_and_events[0] = (c_scenario_lock, "")
    t_selector = Thread(target=selector, args=(c_synced_bthreads,
                                               threads_to_events,
                                               threads_to_locks_and_events ))
    t_scenario = Thread(target=add_external_events, args=(0, c_synced_bthreads,
                                                          threads_to_events,
                                                          threads_to_locks_and_events))

    t_selector.start()
    # time.sleep(2)
    t_scenario.start()

    t_selector.join()
    t_scenario.join()

    print("End main...")
