from execution.listeners.b_program_runner_listener import BProgramRunnerListener
import socket
from mde.SocketCommunicator import SocketCommunicator
from z3helper import *
from mde.smt_variables import *
from mde import mde_return_variables as mrv
import subprocess
import time


class MDEBProgramRunnerListener(BProgramRunnerListener):

    def __init__(self, TCP_IP, TCP_PORT, BUFFER_SIZE, player_name, testing=False):
        super().__init__()
        self.player_name = player_name
        self.testing = testing
        if not self.testing:
            self.socket = SocketCommunicator(TCP_IP, TCP_PORT, BUFFER_SIZE)

    def starting(self, b_program):
        file = "/Users/tomyaacov/Desktop/university/thesis/ChallengeProblem/mac/mac.app"  # TODO: change
        subprocess.call(["open", file])
        time.sleep(4)
        if not self.testing:
            self.socket.connect()
        print("CONNECTED")

    def ended(self, b_program):
        if not self.testing:
            self.socket.close()
        print("ENDED")

    def event_selected(self, b_program, event):
        reply = False
        entity = self.player_name
        if event[moveForward] == true:
            message = self.event_to_message("moveForward", str(event[moveForwardReal]))
        elif event[moveRight] == true:
            message = self.event_to_message("moveRight", str(event[moveRightReal]))
        elif event[spin] == true:
            message = self.event_to_message("spin", str(event[spinReal]))
        elif event[stop] == true:
            message = self.event_to_message("stop")
        elif event[setSuction] == true:
            message = self.event_to_message("setSuction", str(event[setSuctionReal]))
        elif event[getSuction] == true:
            message = self.event_to_message("getSuction")
            reply = True
        elif event[GPS] == true:
            message = self.event_to_message("GPS")
            reply = True
        elif event[ballGPS] == true:
            entity = "ball"
            message = self.event_to_message("ball,GPS")
            reply = True
        elif event[getCompass] == true:
            message = self.event_to_message("getCompass")
            reply = True
        if not self.testing:
            if reply:
                answer = self.socket.send(message)
                answer = answer.decode().strip(";\n").strip(entity+",")
                if event[getSuction] == true:
                    mrv.getSuctionReal = float(answer)
                elif event[GPS] == true:
                    mrv.GPSRealx, mrv.GPSRealy = tuple([float(x) for x in answer.split(",")])
                elif event[ballGPS] == true:
                    mrv.ballGPSRealx, mrv.ballGPSRealy = tuple([float(x) for x in answer.split(",")])
                elif event[getCompass] == true:
                    mrv.getCompassReal = float(answer)
            else:
                self.socket.no_reply(message)
        print(message)

    def event_to_message(self, event_string, parameter=""):
        if event_string == "ball,GPS":
            return event_string + "(" + parameter + ")"
        return self.player_name + "," + event_string + "(" + parameter + ")"

    def started(self, b_program):
        pass

    def super_step_done(self, b_program):
        pass

    def assertion_failed(self, b_program):
        pass

    def b_thread_added(self, b_program):
        pass

    def b_thread_removed(self, b_program):
        pass

    def b_thread_done(self, b_program):
        pass

    def halted(self, b_program):
        pass
