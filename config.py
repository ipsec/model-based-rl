import argparse
from utils import Game

class Config(object):

  def __init__(self, args, visit_softmax_temperature_fn):
    self.__dict__.update(args)
    self.visit_softmax_temperature_fn = visit_softmax_temperature_fn

  def new_game(self, environment):
    return Game(environment, self.discount)


def make_atari_config():
  parser = argparse.ArgumentParser()

  parser.add_argument('--architecture', type=str, default='MuZeroNet')

  ### Environment
  parser.add_argument('--environment', type=str, default='SpaceInvadersNoFrameskip-v4') # BreakoutNoFrameskip-v4 SpaceInvadersNoFrameskip-v4

  # Environment Modifications
  parser.add_argument('--clip_rewards', action='store_true')
  parser.add_argument('--episode_life', action='store_true')
  parser.add_argument('--stack_actions', action='store_true')
  parser.add_argument('--stack_frames', type=int, default=32)
  parser.add_argument('--frame_size', nargs='+', type=int, default=[96, 96])
  parser.add_argument('--noop_max', type=int, default=30)
  parser.add_argument('--frame_skip', type=int, default=4)

  ### Self-Play
  parser.add_argument('--num_actors', type=int, default=5)
  parser.add_argument('--max_moves', type=int, default=27000)
  parser.add_argument('--num_simulations', type=int, default=50)
  parser.add_argument('--discount', type=float, default=0.997)
  parser.add_argument('--visit_softmax_temperatures', nargs='+', type=float, default=[1.0, 0.5, 0.25])
  parser.add_argument('--visit_softmax_temperature_steps', nargs='+', type=int, default=[500e3, 750e3])

  # Root prior exploration noise.
  parser.add_argument('--root_dirichlet_alpha', type=float, default=0.25)
  parser.add_argument('--root_exploration_fraction', type=float, default=0.25)

  # UCB formula
  parser.add_argument('--pb_c_base', type=int, default=19652)
  parser.add_argument('--pb_c_init', type=float, default=1.25)

  ### Prioritized Replay Buffer
  parser.add_argument('--window_size', type=int, default=int(1e6))
  parser.add_argument('--epsilon', type=float, default=0.01)
  parser.add_argument('--alpha', type=float, default=1.)
  parser.add_argument('--beta', type=float, default=1.)
  parser.add_argument('--beta_increment_per_sampling', type=float, default=0.001)

  ### Training
  parser.add_argument('--training_steps', type=int, default=int(1000e3))
  parser.add_argument('--policy_loss', type=str, default='CrossEntropyLoss')
  parser.add_argument('--scalar_loss', type=str, default='MSELoss')
  parser.add_argument('--num_unroll_steps', type=int, default=5)
  parser.add_argument('--checkpoint_interval', type=int, default=int(1e3))
  parser.add_argument('--td_steps', type=int, default=10)
  parser.add_argument('--batch_size', type=int, default=1024)


  ## Optimizer
  parser.add_argument('--optimizer', type=str, default='SGD')
  parser.add_argument('--momentum', type=float, default=0.9)
  parser.add_argument('--weight_decay', type=float, default=1e-4)

  ## Learning rate scheduler
  parser.add_argument('--lr_scheduler', type=str, default='ExponentialLR')
  parser.add_argument('--lr_init', type=float, default=0.05)
  parser.add_argument('--lr_decay_rate', type=float, default=0.1)
  parser.add_argument('--lr_decay_steps', type=int, default=350e3)

  args = vars(parser.parse_args())

  def visit_softmax_temperature(training_steps):
    limit_1, limit_2 = args['visit_softmax_temperature_steps']
    temp_1, temp_2, temp_3 = args['visit_softmax_temperatures']
    if training_steps < limit_1:
      return temp_1
    elif training_steps < limit_2:
      return temp_2
    else:
      return temp_3

  return Config(args=args, visit_softmax_temperature_fn=visit_softmax_temperature)
