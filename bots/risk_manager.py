"""Usage:
  risk_manager.py [--investment=<investment>] [--risk-factor=<risk_factor>]

Options:
  --investment=<investment>     Specify the amount of investment to be made (i.e total money).
  --risk-factor=<risk_factor>   Specify the risk factor in between 1-10 (1: lowest risk, 10: highest risk)
  -h --help                     Show this help message and exit.
"""
import numpy as np
from docopt import docopt
import coloredlogs
import logging
import requests
import subprocess
import sys
from short_term.agent import ShortTermAgent
from long_term.agent import LongTermAgent
from short_term.utils import (
    get_stock_data,
    format_currency,
    format_position,
    show_eval_result,
    switch_k_backend_device
)
from short_term.utils import (
    format_currency,
    format_position
)
from short_term.ops import (
    get_state
)

def evaluate_agents(agent1, agent2, investment, risk_factor, data):
    total_profit = 0
    data_length = len(data) - 1
    rf = risk_factor / 10
    history = []
    inventory = []
    balance = investment
    rm_inventory = 0
    state1 = get_state(data, 0, agent1.state_size + 1)
    state2 = get_state(data, 0, agent2.state_size + 1)

    url = "http://localhost:8111/log_action"
    for t in range(data_length):
        reward = 0
        next_state1 = get_state(data, t + 1, agent1.state_size + 1)
        next_state2 = get_state(data, t + 1, agent2.state_size + 1)

        # select an action
        action1 = agent1.act(state1, is_eval=True) # Short term agent
        action2 = agent2.act(state2, is_eval=True) # Long term agent
        act1prob = agent1.act_prob(state1, is_eval=True)[0].tolist()
        act2prob = agent2.act_prob(state2, is_eval=True)[0].tolist()
        # Normalize act1prob
        sum_act1prob = sum(act1prob)
        normalized_act1prob = [a / sum_act1prob for a in act1prob]

        # Normalize act2prob
        sum_act2prob = sum(act2prob)
        normalized_act2prob = [a / sum_act2prob for a in act2prob]

        # Now you can calculate actprob with the normalized values
        actprob = [(rf * a1 + (1 - rf) * a2) for a1, a2 in zip(normalized_act1prob, normalized_act2prob)]

        if action1 != 1 and action1 != 2:
            action1 = "hold"

        if action1 == 1:
            action1 = "buy"

        if action1 == 2:
            action1 = "sell"

        if action2 != 1 and action2 != 2:
            action2 = "hold"

        if action2 == 1:
            action2 = "buy"

        if action2 == 2:
            action2 = "sell"


        current_price = data[t]
        action = np.argmax(actprob)
        print ("action : ", action)

        normalizer = 0
        for i in actprob:
            normalizer = normalizer + i
        normalizedMax = np.max(actprob) / normalizer
        print("normalized max: ", normalizedMax)

        # TODO: Basic risk manager algorithm, change if needed!!!!



        # BUY
        if action == 1:
            inventory.append(data[t])
            history.append((data[t], "BUY"))
            logging.debug("RISK MANAGER BUY AT: {}".format(format_currency(data[t])))
            amount = balance * normalizedMax / data[t]
            balance = balance - amount * data[t]
            rm_inventory = rm_inventory + amount
            data2 = {
                'time': t,
                'rm_request': 'buy',
                'lft_agent_request': action2,
                'hft_agent_request': action1,
                'amount': amount,
                'total_balance': balance,
                'currency_rate': data[t],
                'rm_inventory': rm_inventory,
            }
            response = requests.post(url, json=data2)
            print(response.text)  # Hata gelirse gorelim diye


        # SELL
        elif action == 2 and len(inventory) > 0:
            bought_price = inventory.pop(0)
            delta = data[t] - bought_price
            reward = delta  # max(delta, 0)
            total_profit += delta
            history.append((data[t], "SELL"))
            logging.debug("RISK MANAGER SELL AT: {} | Position: {}".format(
                    format_currency(data[t]), format_position(data[t] - bought_price)))
            amount = rm_inventory * normalizedMax
            balance = balance + amount * data[t]
            rm_inventory = rm_inventory - amount
            data2 = {
                'time': t,
                'rm_request': 'sell',
                'lft_agent_request': action2,
                'hft_agent_request': action1,
                'amount': amount,
                'total_balance': balance,
                'currency_rate': data[t],
                'rm_inventory': rm_inventory,
            }
            response = requests.post(url, json=data2)
            print(response.text)  # Hata gelirse gorelim diye
        # HOLD
        else:
            history.append((data[t], "HOLD"))

            data2 = {
                'time': t,
                'rm_request': 'hold',
                'lft_agent_request': action2,
                'hft_agent_request': action1,
                'amount': 0,
                'total_balance': balance,
                'currency_rate': data[t],
                'rm_inventory': rm_inventory,
            }
            response = requests.post(url, json=data2)
            print(response.text)  # Hata gelirse gorelim diye

        done = (t == data_length - 1)
        agent1.memory.append((state1, action1, reward, next_state1, done))
        agent2.memory.append((state2, action2, reward, next_state2, done))

        state1 = next_state1
        state2 = next_state2
        if done:
            balance = balance + (data[data_length - 1] * rm_inventory)
            data2 = {
                'time': data_length,
                'normalized_max': 0,
                'rm_request': 'sell',
                'lft_agent_request': "hold",
                'hft_agent_request': "hold",
                'amount': rm_inventory,
                'total_balance': balance,
                'currency_rate': format_currency(data[t]),
                'rm_inventory': 0,
            }
            response = requests.post(url, json=data2)
            return total_profit, history

def main():
    args = docopt(__doc__)
    investment = int(args["--investment"])
    risk_factor = int(args["--risk-factor"])
    url = "http://localhost:8111/set_initial_balance"
    data2 = {'initial_balance': investment}  # Burasi csv file profit hesaplama icin gonderiliyor
    response = requests.post(url, json=data2)
    if risk_factor < 1 or risk_factor > 10:
        print("### Invalid risk factor, risk factor should be an int between 1 and 10!")
        sys.exit()

    coloredlogs.install(level="DEBUG")

    short_term_model_name = "short_term_test_ep0_wd3_bs50"
    long_term_model_name = "long_term_test_ep0_wd10_bs50"

    data = get_stock_data('./data/GOOG_2019.csv')
    initial_offset = data[1] - data[0]

    agent1 = ShortTermAgent(model_name=short_term_model_name, pretrained=True)
    print(f"### Short Term agent initialized for evaluation with state size = {agent1.state_size}.")

    agent2 = LongTermAgent(model_name=long_term_model_name, pretrained=True)
    print(f"### Long Term agent initialized for evaluation with state size = {agent2.state_size}.")

    profit, _ = evaluate_agents(agent1, agent2, investment, risk_factor, data)
    show_eval_result("RISK MANAGER", profit, initial_offset)


if __name__ == "__main__":
    main()