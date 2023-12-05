"""Usage:
  train_bot.py [--agent-type=<agent_type>] [--window-size=<window-size>]
  [--batch-size=<batch-size>] [--episode-count=<episode-count>]
  [--pretrained]

Options:
  --agent-type=<type>     Specify the type of agent (e.g., short-term).
  -h --help               Show this help message and exit.
"""

from short_term.agent import Agent
from short_term.methods import train_model, evaluate_model
from short_term.utils import (
    get_stock_data,
    format_currency,
    format_position,
    show_train_result,
    switch_k_backend_device
)
from docopt import docopt

def main(_agent_type, _window_size, _batch_size, _episode_count, _pretrained=False):
    model_name = 'test'
    print(f"### Training agent {model_name} with the arguments:", _agent_type, _window_size, _batch_size, _episode_count, _pretrained)
    agent = Agent(_window_size, model_name, pretrained)

    train_data = get_stock_data('./data/GOOG_2019.csv')
    val_data = get_stock_data('./data/GOOG_2019.csv')

    initial_offset = val_data[1] - val_data[0]

    for step in range(0, _episode_count + 1):
        # train the model
        train_result = train_model(agent, step, train_data, ep_count=_episode_count, batch_size=_batch_size, window_size=_window_size)
        print(f"### Training completed for episode {step}.")
        # evaluate the model
        validation_result, _ = evaluate_model(agent, val_data, window_size)
        print(f"### Evaluation completed for episode {step}.")
        show_train_result(train_result, validation_result, initial_offset)


if __name__ == "__main__":
    args = docopt(__doc__)

    agent_type = args["--agent-type"]
    window_size = int(args["--window-size"])
    batch_size = int(args["--batch-size"])
    episode_count = int(args["--episode-count"])
    pretrained = args["--pretrained"]

    try:
        main(agent_type, window_size, batch_size, episode_count, pretrained)
    except KeyboardInterrupt:
        print("### Keyboard Interrupt: Exiting.")
