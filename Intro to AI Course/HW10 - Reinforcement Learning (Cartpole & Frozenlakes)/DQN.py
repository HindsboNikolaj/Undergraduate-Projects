import torch.nn as nn
import torch.nn.functional as functional
from collections import deque
import gym
import random
import torch
import numpy as np
import torch.optim as optim
import time
import pickle


EARLY_STOPPING_THRESHOLD = 80 # we stop training and immediately save our model when we reach a this average score over the past 100 episodes
INPUT_DIMENSIONS = 4
OUTPUT_DIMENSIONS = 2
MAX_QUEUE_LENGTH = 1000000
EPSILON = 1
EPSILON_DECAY = .996
MIN_EPSILON = .05
EPOCHS =   2000
DISCOUNT_FACTOR = 0.995
TARGET_NETWORK_UPDATE_FREQUENCY = 5000
MINI_BATCH_SIZE = 32
PRETRAINING_LENGTH = 1000





class Network(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(INPUT_DIMENSIONS,12)
        self.fc2 = nn.Linear(12,12)
        self.fc3 = nn.Linear (12, OUTPUT_DIMENSIONS)


    def forward(self,x):
        x = functional.relu(self.fc1(x))
        x = functional.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class ExperienceReplayBuffer():
    experience_list = None
    def __init__(self):
        #TODO complete ExperienceReplayBuffer __init__
        #Depends on MAX_QUEUE_LENGTH
        #HINT: use a deque object
        self.experience_list = deque(maxlen = MAX_QUEUE_LENGTH)
        

    def sample_mini_batch(self):
        #TODO complete ExperienceReplayBuffer sample_mini_batch
        #Depends on MINI_BATCH_SIZE
        batch = random.sample(self.experience_list, MINI_BATCH_SIZE)
        return batch

    def append(self,experience):
        #TODO complete ExperienceReplayBuffer append
        self.experience_list.append(experience)


if __name__ == "__main__":




    torch.manual_seed(1)
    random.seed(1)
    np.random.seed(1)

    policy_net = Network()
    target_policy_net = Network()

    target_policy_net.load_state_dict(policy_net.state_dict()) # here we update the target policy network to match the policy network


    env = gym.envs.make("CartPole-v1")
    env.seed(1)
    env.action_space.np_random.seed(1)


    queue = ExperienceReplayBuffer()

    optimizer = optim.Adam(policy_net.parameters(), lr=.001)

    step_counter = 0

    episode_reward_record = deque(maxlen=100)


    for i in range(EPOCHS):
        episode_reward = 0
        done = False
        obs = env.reset()
        while not done:
           
           #TODO collect experience sample and add to experience replay buffer
           if random.uniform(0, 1) < EPSILON:
               action = env.action_space.sample()
           else:
               with torch.no_grad():
                   prediction = np.array(policy_net(torch.tensor(np.array(obs)).float()))
                   action = np.argmax(prediction)
           new_state, reward, done, _ = env.step(action)
           episode_reward += reward
           experience_tuple = (obs, action, reward, new_state, done)
           queue.append(experience_tuple)
           env.render()
           obs = new_state
           
           if step_counter >= PRETRAINING_LENGTH:
                experience = queue.sample_mini_batch()
               
                #TODO Fill in the missing code to perform a Q update on 'policy_net'
                #for the sampled experience minibatch 'experience'
                all_states_estimator = []
                all_states = []
                all_y_vector = []
                for j in range(MINI_BATCH_SIZE):
                    current_state = experience[j][0] # "experience state"
                    all_states.append(current_state) # add to all states
                    with torch.no_grad():
                    	current_estimate = policy_net(torch.tensor(np.array(current_state)).float()).detach()
                    current_terminal = experience[j][4] # "DONE"
                    current_reward = experience[j][2] # "REWARD"
                    current_action = experience[j][1] # " EXPERIENCE
                    # Calculatign y_vector
                    if current_terminal is True:
                        current_estimate[current_action] = current_reward
                    else:
                        state_prime = experience[j][3]
                        with torch.no_grad():
                            Q_sp_ap_prediction = np.array(target_policy_net(torch.tensor(np.array(state_prime)).float()))
                            action_sp_ap = np.argmax(Q_sp_ap_prediction)
                        current_estimate[current_action] = current_reward + DISCOUNT_FACTOR * Q_sp_ap_prediction[action_sp_ap]
                    all_y_vector.append(current_estimate)
             
                #print(len(all_y_vector))
                all_states_tensor = torch.FloatTensor(all_states)
                estimate = policy_net(all_states_tensor)
                temp_y_vector = torch.clone(estimate).detach()
                #print(temp_y_vector)
                
                for j in range(MINI_BATCH_SIZE):
                    temp_y_vector[j][0] = all_y_vector[j][0]
                    temp_y_vector[j][1] = all_y_vector[j][1]
                
                loss = functional.smooth_l1_loss(estimate,temp_y_vector)
                optimizer.zero_grad()
                loss.backward()
                
                optimizer.step()

           if step_counter % TARGET_NETWORK_UPDATE_FREQUENCY == 0:
                target_policy_net.load_state_dict(policy_net.state_dict()) # here we update the target policy network to match the policy network
           step_counter += 1

        EPSILON = EPSILON * EPSILON_DECAY
        if EPSILON < MIN_EPSILON:
            EPSILON = MIN_EPSILON
        episode_reward_record.append(episode_reward)

        if i%100 ==0 and i>0:
            last_100_avg = sum(list(episode_reward_record))/100
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(last_100_avg))
            print("EPSILON: " +  str(EPSILON))
            if last_100_avg > EARLY_STOPPING_THRESHOLD:
                break

    
    torch.save(policy_net.state_dict(), "DQN.mdl")
    pickle.dump([EPSILON], open("DQN_DATA.pkl",'wb'))







