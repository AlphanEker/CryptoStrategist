import os
import logging
import requests
import numpy as np

from tqdm import tqdm

from long_term.utils import (
    format_currency,
    format_position
)
from long_term.ops import (
    get_state
)

def train_model(agent, episode, data, ep_count=100, batch_size=32, window_size=10):
    total_profit = 0
    data_length = len(data) - 1

    agent.inventory = []
    avg_loss = []

    state = get_state(data, 0, window_size + 1)

    for t in range(data_length): # tqdm(range(data_length), total=data_length, leave=True, desc='Episode {}/{}'.format(episode, ep_count))
        reward = 0
        next_state = get_state(data, t + 1, window_size + 1)

        # select an action
        action = agent.act(state)

        # BUY
        if action == 1:
            agent.inventory.append(data[t])

        # SELL
        elif action == 2 and len(agent.inventory) > 0:
            bought_price = agent.inventory.pop(0)
            delta = data[t] - bought_price
            reward = delta  # max(delta, 0)
            total_profit += delta

        # HOLD
        else:
            pass

        done = (t == data_length - 1)
        agent.remember(state, action, reward, next_state, done)

        if len(agent.memory) > batch_size:
            loss = agent.train_experience_replay(batch_size)
            print(f"### Loss at episode = {episode}, t = {t}:", loss)
            avg_loss.append(loss)

        state = next_state

    if episode % 10 == 0:
        agent.save(episode, window_size, batch_size)

    return (episode, ep_count, total_profit, np.mean(np.array(avg_loss)))


def evaluate_model(agent, data, window_size, debug=True):
    debug=True
    total_profit = 0
    data_length = len(data) - 1
    balance = 10000
    confidence = 0.5
    lft_inventory = 0
    history = []
    agent.inventory = []
    url = "http://localhost:8111/set_initial_balance"
    data2 = {'initial_balance': balance}  # Burasi csv file profit hesaplama icin gonderiliyor
    response = requests.post(url, json=data2)
    url = "http://localhost:8111/log_action"
    state = get_state(data, 0, window_size + 1)

    for t in range(data_length):
        reward = 0
        next_state = get_state(data, t + 1, window_size + 1)

        # select an action
        action = agent.act(state, is_eval=True)
        action_probs = agent.act_prob(state, is_eval=True)[0].tolist()
        normalizer = 0
        for i in action_probs:
            normalizer = normalizer + i
        normalizedMax = np.max(action_probs) / normalizer
        print("normalized max: ", normalizedMax)

        # BUY
        if action == 1:
            agent.inventory.append(data[t])

            history.append((data[t], "BUY"))
            amount = balance * normalizedMax * confidence / data[t]
            balance = balance - (amount * data[t])
            lft_inventory = lft_inventory + amount
            data2 = {
                'time': t,
                'normalized_max': normalizedMax,
                'rm_request': 'buy',
                'lft_agent_request': "buy",
                'hft_agent_request': "buy",
                'amount': amount,  # Buraya data gelcek
                'total_balance': balance,  # Global variable balance olcak onu gondercez
                'currency_rate': format_currency(data[t]),  # Dogru olmayabilir t zamandaki close price gondercez
                'hft_inventory': 0,  # buraya hft ne kadar coine sahip o gelcek
                'lft_inventory': lft_inventory  # hft gibi
            }
            response = requests.post(url, json=data2)
            if debug:
                logging.debug("Buy at: {}".format(format_currency(data[t])))

        # SELL
        elif action == 2 and len(agent.inventory) > 0:
            bought_price = agent.inventory.pop(0)
            delta = data[t] - bought_price
            reward = delta  # max(delta, 0)
            total_profit += delta
            amount = lft_inventory * normalizedMax * confidence
            balance = balance + (amount * data[t])
            lft_inventory = lft_inventory - amount
            data2 = {
                'time': t,
                'normalized_max': normalizedMax,
                'rm_request': 'sell',
                'lft_agent_request': "sell",
                'hft_agent_request': "sell",
                'amount': amount,  # Buraya data gelcek
                'total_balance': balance,  # Global variable balance olcak onu gondercez
                'currency_rate': format_currency(data[t]),  # Dogru olmayabilir t zamandaki close price gondercez
                'hft_inventory': 0,  # buraya hft ne kadar coine sahip o gelcek
                'lft_inventory': lft_inventory  # hft gibi
            }
            response = requests.post(url, json=data2)

            history.append((data[t], "SELL"))
            if debug:
                logging.debug("Sell at: {} | Position: {}".format(
                    format_currency(data[t]), format_position(data[t] - bought_price)))
        # HOLD
        else:
            data2 = {
                'time': t,
                'normalized_max': 0,
                'rm_request': 'hold',
                'lft_agent_request': "hold",
                'hft_agent_request': "hold",
                'amount': 0,  # Buraya data gelcek
                'total_balance': balance,  # Global variable balance olcak onu gondercez
                'currency_rate': format_currency(data[t]),  # Dogru olmayabilir t zamandaki close price gondercez
                'hft_inventory': 0,  # buraya hft ne kadar coine sahip o gelcek
                'lft_inventory': lft_inventory  # hft gibi
            }
            response = requests.post(url, json=data2)
            history.append((data[t], "HOLD"))

        done = (t == data_length - 1)
        agent.memory.append((state, action, reward, next_state, done))

        state = next_state
        if done:
            balance = balance + (data[data_length - 1] * lft_inventory)
            data2 = {
                'time': data_length - 1,
                'normalized_max': 0,
                'rm_request': 'hold',
                'lft_agent_request': "hold",
                'hft_agent_request': "hold",
                'amount': lft_inventory,  # Buraya data gelcek
                'total_balance': balance,  # Global variable balance olcak onu gondercez
                'currency_rate': format_currency(data[t]),  # Dogru olmayabilir t zamandaki close price gondercez
                'hft_inventory': 0,  # buraya hft ne kadar coine sahip o gelcek
                'lft_inventory': 0  # hft gibi
            }
            lft_inventory = 0
            response = requests.post(url, json=data2)
            return total_profit, history