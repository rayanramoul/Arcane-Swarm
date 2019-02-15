from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features
from absl import app
from pysc2.lib import actions, features, units
import random

from q_table import *

class ArcaneSwarm(base_agent.BaseAgent):
    def __init__(self):
        super(ArcaneSwarm, self).__init__()
        self.spawningpool=False
        self.attack_coordinates = None
        self.qlearn = QLearningTable(actions=list(range(len(actions))))

    def step(self, obs):
        super(ArcaneSwarm, self).step(obs)
        if obs.first():
            player_y, player_x = (obs.observation.feature_minimap.player_relative ==
                                  features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()

            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (49, 49)

            else:
                self.attack_coordinates = (12, 16)
        larvae = self.get_units_by_type(obs, units.Zerg.Larva)
        return actions.FUNCTIONS.no_op()

    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
            obs.observation.single_select[0].unit_type == unit_type):
            return True
    
        if (len(obs.observation.multi_select) > 0 and
            obs.observation.multi_select[0].unit_type == unit_type):
            return True
    
        return False

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
            if unit.unit_type == unit_type]

    def can_do(self, obs, action):
        return action in obs.observation.available_actions

def main(unused_argv):
    agent = ArcaneSwarm()
    try:
        while True:
            with sc2_env.SC2Env(
                map_name="AbyssalReef",
                players=[sc2_env.Agent(sc2_env.Race.zerg), sc2_env.Bot(sc2_env.Race.random,
            sc2_env.Difficulty.very_easy)],
            agent_interface_format=features.AgentInterfaceFormat(
feature_dimensions=features.Dimensions(screen=84, minimap=64),use_feature_units=True), # Size of screen and minimap that the agent see

            visualize=True
            ) as env:
                agent.setup(env.observation_spec(), env.action_spec())
                timesteps = env.reset()
                agent.reset()
                
                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)


    except KeyboardInterrupt:
        pass
    
if __name__=="__main__":
    app.run(main)