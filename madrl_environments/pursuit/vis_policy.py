from centralized_pursuit_evade import CentralizedPursuitEvade
import gym
from os.path import join
import matplotlib.pyplot as plt

from utils import *

import tensorflow as tf

from rltools.algs import TRPOSolver
from rltools.utils import simulate
from rltools.models import softmax_mlp


xs = 10
ys = 10
n_evaders = 1
n_pursuers = 2

map_mat = TwoDMaps.rectangle_map(xs, ys) 

# obs_range should be odd 3, 5, 7, etc
#env = CentralizedPursuitEvade(map_mat, n_evaders=n_evaders, n_pursuers=n_pursuers, obs_range=9, n_catch=2)


config = {}
config["train_iterations"] = 1000 # number of trpo iterations
config["max_pathlength"] = 250 # maximum length of an env trajecotry
config["timesteps_per_batch"] = 1000
config["eval_trajectories"] = 50
config["eval_every"] = 50
config["gamma"] = 0.95 # discount factor

ran = 5

env = CentralizedPursuitEvade(map_mat, n_evaders=n_evaders, n_pursuers=n_pursuers, obs_range=ran, n_catch=2)

input_obs = tf.placeholder(tf.float32, shape=(None,) + env.observation_space.shape, name="obs" + str(ran))
net = softmax_mlp(input_obs, env.action_space.n, layers=[128,128], activation=tf.nn.tanh)

solver = TRPOSolver(env, config=config, policy_net=net, input_layer=input_obs)

model_path = "data/obs_range_sweep_2layer/obs_range_5/run4/"

solver.load(model_path+"final_model.ckpt")
d = solver.load_stats(model_path+"final_stats.txt")

#simulate(env, solver, 100, render=True)
