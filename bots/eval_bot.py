"""
Script for evaluating Stock Trading Bot.

Usage:
  eval_bot.py [--agent-type=<agent_type>] [--model-name=<model-name>] [--debug]

Options:
  --agent-type=<agent_type>     Specify the type of agent (e.g., short-term).
  --model-name=<model-name>     Name of the pretrained model to use (will eval all models in `models/` if unspecified).
  --debug                       Specifies whether to use verbose logs during eval operation.
"""

import os
import coloredlogs

from docopt import docopt

from short_term.agent import ShortTermAgent
from long_term.agent import LongTermAgent

from short_term.methods import evaluate_model
from short_term.utils import (
    get_stock_data,
    format_currency,
    format_position,
    show_eval_result,
    switch_k_backend_device
)


def main(_agent_type, model_name, debug):

    #TODO: DELETE AFTER GETTING DATA
    data = get_stock_data('./data/GOOG_2019.csv')
    initial_offset = data[1] - data[0]

    # Single Model Evaluation
    if model_name is not None:
        agent = None
        if _agent_type == "short_term":
            #TODO: GET HIGH FREQUENCY DATA HERE!
            agent = ShortTermAgent(model_name=model_name, pretrained=True)
            print(f"### Short Term agent initialized for evaluation with state size = {agent.state_size}.")
        elif _agent_type == "long_term":
            #TODO: GET LOW FREQUENCY DATA HERE!
            agent = LongTermAgent(model_name=model_name, pretrained=True)
            print(f"### Long Term agent initialized for evaluation with state size = {agent.state_size}.")
        else:
            print("### Invalid agent type! Exiting...")
            sys.exit()
        profit, _ = evaluate_model(agent, data, agent.state_size, debug)
        show_eval_result(model_name, profit, initial_offset)


if __name__ == "__main__":
    args = docopt(__doc__)

    agent_type = args["--agent-type"]
    model_name = args["--model-name"]
    debug = True

    coloredlogs.install(level="DEBUG")
    switch_k_backend_device()

    try:
        main(agent_type, model_name, debug)
    except KeyboardInterrupt:
        print("Aborted")