"""Usage:
  train_bot.py [--agent-type=<agent_type>] [--batch-size=<batch-size>] [--episode-count=<episode-count>]
  [--pretrained]

Options:
  --agent-type=<type>     Specify the type of agent (e.g., short-term).
  -h --help               Show this help message and exit.
"""

import sys

from short_term.agent import ShortTermAgent
from long_term.agent import LongTermAgent

from short_term.methods import train_model, evaluate_model
from short_term.utils import (
    get_stock_data as short_get_stock_data,
    format_currency,
    format_position,
    show_train_result as short_show_train_result
)

from long_term.utils import (
    get_stock_data as long_get_stock_data,
    format_currency,
    format_position,
    show_train_result as long_show_train_result
)
from docopt import docopt


def main(_agent_type, _batch_size, _episode_count, _pretrained=False):
    model_name = 'test'
    print(f"### Training agent {model_name} with the arguments:", _agent_type, _batch_size, _episode_count, _pretrained)
    train_data = None
    val_data = None
    agent = None
    if _agent_type == "short_term":
        # SET HIGH FREQUENCY DATA
        agent = ShortTermAgent(model_name, pretrained)
        train_data = short_get_stock_data('./data/HFTData30min08.csv')
        val_data = short_get_stock_data('./data/HFTData30min08.csv')
        print(f"### Short Term agent initialized for training with state size = {agent.state_size}.")
    elif _agent_type == "long_term":
        # SET LOW FREQUENCY DATA
        agent = LongTermAgent(model_name, pretrained)
        train_data = long_get_stock_data('./data/LFTData02.csv')
        val_data = long_get_stock_data('./data/LFTData02.csv')
        print(f"### Long Term agent initialized for training with state size = {agent.state_size}.")
    else:
        print("### Invalid agent type! Exiting...")
        sys.exit()

    initial_offset = val_data[1][0] - val_data[0][0]

    for step in range(0, _episode_count + 1):
        # train the model
        train_result = train_model(agent, step, train_data, ep_count=_episode_count, batch_size=_batch_size,
                                   window_size=agent.state_size)
        print(f"### Training completed for episode {step}.")
        # evaluate the model
        #validation_result, _ = evaluate_model(agent, val_data, agent.state_size)
        print(f"### Evaluation completed for episode {step}.")
        #short_show_train_result(train_result, validation_result, initial_offset)




if __name__ == "__main__":
    args = docopt(__doc__)

    agent_type = args["--agent-type"]
    batch_size = int(args["--batch-size"])
    episode_count = int(args["--episode-count"])
    pretrained = args["--pretrained"]

    try:
        main(agent_type, batch_size, episode_count, pretrained)
    except KeyboardInterrupt:
        print("### Keyboard Interrupt: Exiting.")
