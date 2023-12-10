from collections import deque
import gym
import random
import numpy as np
import time
import pickle

from collections import defaultdict


EPISODES =   20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999



def default_Q_value():
    return 0


if __name__ == "__main__":




    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v0")
    env.seed(1)
    env.action_space.np_random.seed(1)


    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.

    episode_reward_record = deque(maxlen=100)
    
    Q_sp_ap = 0
    Q_s_p = 0
    #print("test")

    for i in range(EPISODES):
        episode_reward = 0
        initial = env.reset()
        done = False
        reward = 0
        episode_reward =0 
        #Take original first step
        if random.uniform(0,1) < EPSILON:   # Take a random step
        	action = env.action_space.sample() # Random move 0-3     
        else: # Non-random move
        	prediction = np.array([Q_table[(initial,i)] for i in range(env.action_space.n)]) # Plots all predictions
        	action =  np.argmax(prediction) # Picks the highest rated action from the list

        info_tuple = (initial, action, 0, None, 0, False) # In order (s, a, r, s', a', done)
        
        #TODO perform SARSA learning
        while done is False:
            sp, reward, done, info = env.step(info_tuple[1])
            # get s', and now a' following, also have r', and done' info.
            if random.uniform(0,1) < EPSILON:   # Take a random step
                    action = env.action_space.sample() # Random move 0-3      
            else: # Non-random move
                   prediction = np.array([Q_table[(sp,i)] for i in range(env.action_space.n)]) # Plots all predictions
                   action =  np.argmax(prediction) # Picks the highest rated action from the list
            # Now that a' is calculated, we need to store info appropriately.
           
            info_tuple = (info_tuple[0], info_tuple[1], reward, sp, action, done) # Add the move to info tuple
            # Now, the updating of Q(s, a) can be done.
            
            Q_s_a = Q_table[(info_tuple[0], info_tuple[1])] # Finding Q(s, a)
            Q_sp_ap = Q_table[(info_tuple[3], info_tuple[4])] # Finding Q(s', a')
            #print("Q_s_a: ", Q_s_a, "Q_sp_ap: ", Q_sp_ap, "Done: ", done) # TEMP
            #time.sleep(.01) # TEMP
            if done is True: # New state is at terminal.
            	Q_table[(info_tuple[0], info_tuple[1])] = Q_s_a + LEARNING_RATE*(reward - Q_s_a) # Q(s, a) updates under done condition, with r'
            	if(reward ==1):
            		pass
            		#print('won')
            	
            	episode_reward = reward
            else:
                Q_table[(info_tuple[0], info_tuple[1])] = Q_s_a + LEARNING_RATE*(info_tuple[2] + DISCOUNT_FACTOR*Q_sp_ap-Q_s_a)
           
            info_tuple = (info_tuple[3], info_tuple[4], reward, None, None, done)	

            """## Always Update Q(s, a)
            Q_table[(info_tuple[0], info_tuple[1])] = Q_s_a+LEARNING_RATE*(info_tuple[2]+DISCOUNT_FACTOR*Q_sp_ap-Q_s_a) # Setting Q(s, a)
                   if done is True: # Update Q(s', a') if done is True
                       fake_state, reward_prime, fake_done, fake_info = env.step(info_tuple[4]) # Step to get reward prime
                       Q_table[(info_tuple[3], info_tuple[4])] = Q_sp_ap + LEARNING_RATE*(reward_prime - Q_sp_ap) #?
                       episode_reward = reward_prime
                       print(episode_reward)
                   else: # If done is false, get next info and update s, a, s', a', r done appropriately.
                       new_state, reward, done, info = env.step(info_tuple[4]) # Step s, a to get s', r, done
                       info_tuple = (info_tuple[3], info_tuple[4], reward, new_state, 0, done)
             """   
        episode_reward_record.append(episode_reward)     
        EPSILON*=EPSILON_DECAY 
        if i%100 ==0 and i>0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    ####DO NOT MODIFY######
    model_file = open('SARSA_Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    #######################




