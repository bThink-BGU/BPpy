from z3helper import *
from execution.listeners.print_b_program_runner_listener import PrintBProgramRunnerListener
from model.bprogram import BProgram
from model.event_selection.smt_event_selection_strategy import SMTEventSelectionStrategy
from mde.smt_variables import *
from mde import mde_return_variables as mrv
from mde.MDEBProgramRunnerListener import MDEBProgramRunnerListener
import subprocess
import time
import math

def orient_to_ball():
    while True:
        m = yield {'wait-for': getCompass}
        if mrv.getSuctionReal <= 0:
            angle = get_angle(mrv.GPSRealx, mrv.GPSRealy, mrv.ballGPSRealx, mrv.ballGPSRealy)
            diff = angle - mrv.getCompassReal % 360
            while abs(diff) > 4:
                m = yield {'request': And(spin, spinReal == sign(diff)*70), 'wait-for': And(spin, spinReal == sign(diff)*70)}
                m = yield {'request': stop, 'wait-for': stop}
                angle = get_angle(mrv.GPSRealx, mrv.GPSRealy, mrv.ballGPSRealx, mrv.ballGPSRealy)
                diff = angle - mrv.getCompassReal % 360


def move_to_ball():
    while True:
        m = yield {'wait-for': ballGPS}
        if mrv.getSuctionReal <= 0:
            while get_distance(mrv.GPSRealx, mrv.GPSRealy, mrv.ballGPSRealx, mrv.ballGPSRealy) > 5:
                m = yield {'request': And(moveForward, moveForwardReal == 50), 'wait-for': And(moveForward, moveForwardReal == 50)}
                m = yield {'request': stop, 'wait-for': stop}


def suck_ball():
    while True:
        m = yield {'wait-for': ballGPS}
        if mrv.getSuctionReal <= 0 and get_distance(mrv.GPSRealx, mrv.GPSRealy, mrv.ballGPSRealx, mrv.ballGPSRealy) <= 5:
            m = yield {'request': And(setSuction, setSuctionReal == -100), 'wait-for': And(setSuction, setSuctionReal == -100)}


def stuck_in_south_wall():
    while True:
        m = yield {'wait-for': getCompass}
        if mrv.GPSRealy <= -25.5 and 45 <= mrv.getCompassReal <= 135:
            m = yield {'request': And(moveForward, moveForwardReal == -100), 'block': Or(Not(moveForward), moveForwardReal > 0), 'wait-for': And(moveForward, moveForwardReal == -100)}
            m = yield {'block': moveForward, 'request': stop, 'wait-for': stop}


def stuck_in_north_wall():
    while True:
        m = yield {'wait-for': getCompass}
        if mrv.GPSRealy >= 25.5 and 225 <= mrv.getCompassReal <= 315:
            m = yield {'request': And(moveForward, moveForwardReal == -100), 'block': Not(moveForward), 'wait-for': And(moveForward, moveForwardReal == -100)}
            m = yield {'block': moveForward}
            m = yield {'block': moveForward, 'request': stop, 'wait-for': stop}


def get_state():
    while True:
        m = yield {'request': getSuction, 'block': Not(getSuction)}
        m = yield {'request': GPS, 'block': Not(GPS)}
        m = yield {'request': ballGPS, 'block': Not(ballGPS)}
        m = yield {'request': getCompass, 'block': Not(getCompass)}
        m = yield {'wait-for': true}


def move_forward_real_bounds():
    while True:
        yield {'block': Or(moveForwardReal > 100, moveForwardReal < -100)}


def move_right_real_bounds():
    while True:
        yield {'block': Or(moveRightReal > 100, moveRightReal < -100)}


def spin_real_bounds():
    while True:
        yield {'block': Or(spinReal > 100, spinReal < -100)}


def set_suction_real_bounds():
    while True:
        yield {'block': Or(setSuctionReal > 100, setSuctionReal < -100)}


def exclusion():
    while True:
        yield {'block': Or(And(moveForward, moveRight),
                           And(moveForward, spin),
                           And(moveForward, stop),
                           And(moveForward, setSuction),
                           And(moveForward, getSuction),
                           And(moveForward, GPS),
                           And(moveForward, ballGPS),
                           And(moveForward, getCompass),
                           And(moveRight, spin),
                           And(moveRight, stop),
                           And(moveRight, setSuction),
                           And(moveRight, getSuction),
                           And(moveRight, GPS),
                           And(moveRight, ballGPS),
                           And(moveRight, getCompass),
                           And(spin, stop),
                           And(spin, setSuction),
                           And(spin, getSuction),
                           And(spin, GPS),
                           And(spin, ballGPS),
                           And(spin, getCompass),
                           And(stop, setSuction),
                           And(stop, getSuction),
                           And(stop, GPS),
                           And(stop, ballGPS),
                           And(stop, getCompass),
                           And(setSuction, getSuction),
                           And(setSuction, GPS),
                           And(setSuction, ballGPS),
                           And(setSuction, getCompass),
                           And(getSuction, GPS),
                           And(getSuction, ballGPS),
                           And(getSuction, getCompass),
                           And(GPS, ballGPS),
                           And(GPS, getCompass),
                           And(ballGPS, getCompass),
                           )}

# help functions


def get_angle(x1, y1, x2, y2):
    return abs(math.degrees(math.atan2(y2-y1, x2-x1)))


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def sign(x):
    if x < 0:
        return -1
    else:
        return 1


if __name__ == "__main__":
    b_program = BProgram(bthreads=[get_state(),
                                   orient_to_ball(),
                                   move_to_ball(),
                                   suck_ball(),
                                   stuck_in_north_wall(),
                                   stuck_in_south_wall(),
                                   move_forward_real_bounds(),
                                   move_right_real_bounds(),
                                   spin_real_bounds(),
                                   set_suction_real_bounds(),
                                   exclusion()],
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=MDEBProgramRunnerListener(TCP_IP='127.0.0.1', TCP_PORT=9001, BUFFER_SIZE=1024, player_name="player1", testing=False))

    file = "/Users/tomyaacov/Desktop/university/thesis/ChallengeProblem/mac/mac.app"
    subprocess.call(["open", file])
    time.sleep(4)
    b_program.run()
