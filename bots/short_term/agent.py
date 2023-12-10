import random
from collections import deque
import numpy as np
import tensorflow as tf
import keras.backend as K
from keras.models import Sequential
from keras.models import load_model, clone_model
from keras.layers import Dense
from keras.optimizers import Adam

import logging

def huber_loss(actual, predicted, delta=1.0):
    """
    error^2/2, if |error| <= delta (ie, if it is a small error); delta * ( |error| - delta/2), otherwise
    """
    error = actual - predicted
    cond = K.abs(error) <= delta
    squared_loss = 0.5 * K.square(error)
    quadratic_loss = delta * (K.abs(error) - (delta/2))

    # Return the result as a tensor
    return K.mean(tf.where(cond, squared_loss, quadratic_loss))

class ShortTermAgent:
    def __init__(self, model_name, pretrained):


        # agent config
        self.state_size = 27             # CONSTANT FOR SHORT TERM
        self.action_size = 3            # [hold, buy, sell]
        self.model_name = model_name
        self.inventory = []
        self.memory = deque(maxlen=10000) # replay buffer
        self.first_iter = True

        # model configuration
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.loss = huber_loss
        self.custom_objects = {"huber_loss": huber_loss}
        self.optimizer = Adam(lr=self.learning_rate)

        if pretrained and self.model_name is not None:
            self.model = self.load()
        else:
            self.model = self._model()

    def _model(self):
        """
        A Sequential model used as a base model.
        5 dense layers with relu activation function are added to the sequential model.
        Input layer accepts state_size dimensioned inputs.
        Output layer outputs an action.
        """
        model = Sequential()
        model.add(Dense(units=128, activation="relu", input_dim=self.state_size))
        model.add(Dense(units=256, activation="relu"))
        model.add(Dense(units=256, activation="relu"))
        model.add(Dense(units=128, activation="relu"))
        model.add(Dense(units=self.action_size))

        model.compile(loss=self.loss, optimizer=self.optimizer)
        return model

    def remember(self, state, action, reward, next_state, done):
        """
        Saves the current sample into replay buffer.
        """
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, is_eval=False):
        """
        Take action from given possible set of actions
        """
        # take random action in order to diversify experience at the beginning
        if not is_eval and random.random() <= self.epsilon:
            return random.randrange(self.action_size)

        if self.first_iter:
            self.first_iter = False
            return 1 # make a definite buy on the first iter

        # Take the maximum probability action given state
        action_probs = self.model.predict(state)
        return np.argmax(action_probs[0])

    def train_experience_replay(self, batch_size):
        """
        Train on previous experiences in memory
        """
        # Get a random batch from the memory
        mini_batch = random.sample(self.memory, batch_size)
        X_train, y_train = [], []

        # Deep Q-Learning
        for state, action, reward, next_state, done in mini_batch:
            if done:
                target = reward
            else:
                print("reward : ", reward)
                # approximate deep q-learning equation
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
                # estimate q-values based on current state
                q_values = self.model.predict(state)
                # update the target for current action based on discounted reward
                q_values[0][action] = target

                X_train.append(state[0])
                y_train.append(q_values[0])

        # update q-function parameters based on huber loss gradient
        loss = self.model.fit(
            np.array(X_train), np.array(y_train),
            epochs=1, verbose=0
        ).history["loss"][0]

        # as the training goes on we want the agent to
        # make less random and more optimal decisions
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        return loss

    def save(self, episode, window_size, batch_size):
        self.model.save("models/short_term_{}_ep{}_wd{}_bs{}".format(self.model_name, episode, window_size, batch_size))

    def load(self):
        return load_model("models/" + self.model_name, custom_objects=self.custom_objects)