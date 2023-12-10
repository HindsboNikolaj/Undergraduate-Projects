import gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict


EPISODES =   20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999

"""
An argmax function for the Q-learning.
"""


def default_Q_value():
    return 0


if __name__ == "__main__":



    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v0")
    env.seed(1)
    env.action_space.np_random.seed(1)
    
    #TODO - Make use of epsilon and epsilon decay - not just random moves
    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)



    for i in range(EPISODES): # Each episode is done when state is 'done'
        episode_reward = 0
        reward = 0
        done = False
        obs = env.reset()
        #TODO PERFORM Q LEARNING
        while done is False:
            if random.uniform(0,1) < EPSILON:   # Take a random step
                action = env.action_space.sample() # Random move 0-3
                
            else: # Non-random move
                prediction = np.array([Q_table[(obs,i)] for i in range(env.action_space.n)]) # Plots all predictions
                action =  np.argmax(prediction) # Picks the highest rated action from the list
            # Get info from this new step.
            new_state, reward, done, info = env.step(action) # New state
            Q_s_a = Q_table[(obs, action)] # Current state Q value with action selected
            prediction_for_max = np.array([Q_table[(new_state,i)] for i in range(env.action_space.n)]) # Plots all predictions          	
            action_max = np.argmax(prediction_for_max)
            
            gamma_max = Q_table[(new_state, action_max)]
            # For each sample tuple (s, a, r, s', done)  
            # Update if terminal state
            # Q(s, a) = Q(s,a)+α(r−Q(s,a))
            if done is True: # Finished
                Q_table[(obs, action)] = Q_s_a + LEARNING_RATE*(reward-Q_s_a)
                episode_reward = reward
            # Not terminal state
            # Q(s, a) = Q(s,a)+α(r+γmaxa′∈AQ(s′,a′)−Q(s,a))
            else:
                Q_table[(obs, action)] = Q_s_a + LEARNING_RATE*(reward + DISCOUNT_FACTOR*gamma_max-Q_s_a)
            
            obs = new_state
            
        episode_reward_record.append(episode_reward)
        EPSILON *= EPSILON_DECAY
        if i%100 ==0 and i>0:

            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
            pass
  
    ####DO NOT MODIFY######
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    #######################








