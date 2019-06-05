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


def reward_close_to_ball():
    m = yield {'wait-for': true}
    m = yield {'wait-for': getCompass}
    while True:
        if goal():
            sug_reward = 5
            m = yield {'block': Not(rewardReal != sug_reward)}
        else:
            distance = distance_from_ball()
            sug_reward = -distance/100
            m = yield {'block': Not(rewardReal != sug_reward)}


def get_state():
    while True:
        m = yield {'request': stop, 'block': Not(stop)}
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


def reward_real_bounds():
    m = yield {'wait-for': true}
    m = yield {'wait-for': getCompass}
    while True:
        yield {'block': Or(rewardReal > 100, rewardReal < -100)}


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


def angle_to_ball():
    return abs(math.degrees(math.atan2(mrv.ballGPSRealy-mrv.GPSRealy, mrv.ballGPSRealx-mrv.GPSRealx)))


def distance_from_ball():
    return math.sqrt((mrv.ballGPSRealx - mrv.GPSRealx)**2 + (mrv.ballGPSRealy - mrv.GPSRealy)**2)


def goal():
    return mrv.ballGPSRealx > 45.99 and -9 <= mrv.ballGPSRealy <= 9


def holding_ball():
    return distance_from_ball() < 2.5 and mrv.getSuctionReal < 0


def sign(x):
    if x < 0:
        return -1
    else:
        return 1


import gym
import itertools
import sys
import datetime
import os
import numpy as np
import tensorflow as tf
import tensorflow.contrib.layers as layers

import baselines.common.tf_util as U

from baselines import logger
from baselines import deepq
from baselines.deepq.replay_buffer import ReplayBuffer
from baselines.deepq.utils import ObservationInput
from baselines.common.schedules import LinearSchedule

from mde.bp_env import BPEnv
from mde.action_space import action_space
from mde.observation_space import observation_space


def model(inpt, num_actions, scope, reuse=False):
    """This model takes as input an observation and returns values of all actions."""
    with tf.variable_scope(scope, reuse=reuse):
        out = inpt
        out = layers.fully_connected(out, num_outputs=64, activation_fn=tf.nn.tanh)
        out = layers.fully_connected(out, num_outputs=num_actions, activation_fn=None)
        return out


if __name__ == '__main__':
    DIR = os.path.join(os.getcwd(), datetime.datetime.now().strftime("mde-%Y-%m-%d-%H-%M-%S-%f"))
    gpu_options = tf.GPUOptions(visible_device_list=sys.argv[1])
    config = tf.ConfigProto(gpu_options=gpu_options)
    config.gpu_options.allow_growth = True
    with U.make_session(config=config):
        logger.configure(dir=DIR)
        # Create the environment
        listener = MDEBProgramRunnerListener(TCP_IP='127.0.0.1', TCP_PORT=9001, BUFFER_SIZE=1024, player_name="player1",
                                             testing=False)
        b_program = BProgram(bthreads=[get_state(),
                                       reward_close_to_ball(),
                                       move_forward_real_bounds(),
                                       move_right_real_bounds(),
                                       spin_real_bounds(),
                                       set_suction_real_bounds(),
                                       # reward_real_bounds(),
                                       exclusion()],
                             event_selection_strategy=SMTEventSelectionStrategy(),
                             listener=listener)

        env = BPEnv()
        env.set_bprogram(b_program)
        env.set_listener(listener)
        # Create all the functions necessary to train the model
        act, train, update_target, debug = deepq.build_train(
            make_obs_ph=lambda name: ObservationInput(observation_space, name=name),
            q_func=model,
            num_actions=action_space.__len__(),
            optimizer=tf.train.AdamOptimizer(learning_rate=5e-4),
        )
        # Create the replay buffer
        replay_buffer = ReplayBuffer(50000)
        # Create the schedule for exploration starting from 1 (every action is random) down to
        # 0.02 (98% of actions are selected according to values predicted by the model).
        exploration = LinearSchedule(schedule_timesteps=10000, initial_p=1.0, final_p=0.02)

        # Initialize the parameters and copy them to the target network.
        U.initialize()
        update_target()

        episode_rewards = [0.0]
        obs = env.reset()
        for t in itertools.count():
            print(t)
            # Take action and update exploration to the newest value
            action = act(obs[None], update_eps=exploration.value(t))[0]
            new_obs, rew, done, _ = env.step(action_space[action])
            # Store transition in the replay buffer.
            print((obs, action, rew, new_obs, float(done)))
            replay_buffer.add(obs, action, rew, new_obs, float(done))
            obs = new_obs

            episode_rewards[-1] += rew
            if done:
                obs = env.reset()
                episode_rewards.append(0)

            #is_solved = t > 1000 and np.mean(episode_rewards[-101:-1]) >= 200
            is_solved = t > 1000 or np.mean(episode_rewards[-101:-1]) >= 1
            if is_solved:
                U.save_variables(save_path=DIR)
            else:
                # Minimize the error in Bellman's equation on a batch sampled from replay buffer.
                if t > 1000:
                #if t > 100:
                    obses_t, actions, rewards, obses_tp1, dones = replay_buffer.sample(32)
                    train(obses_t, actions, rewards, obses_tp1, dones, np.ones_like(rewards))
                # Update target network periodically.
                if t % 1000 == 0:
                #if t % 100 == 0:
                    update_target()

            if done and len(episode_rewards) % 10 == 0:
                logger.record_tabular("steps", t)
                logger.record_tabular("episodes", len(episode_rewards))
                logger.record_tabular("mean episode reward", round(np.mean(episode_rewards[-101:-1]), 1))
                logger.record_tabular("% time spent exploring", int(100 * exploration.value(t)))
                logger.dump_tabular()

