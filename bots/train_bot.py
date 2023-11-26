"""Usage:
  train_bot.py [--agent-type=<agent_type>] [--window-size=<window-size>]
  [--batch-size=<batch-size>] [--episode-count=<episode-count>]
  [--pretrained]

Options:
  --agent-type=<type>     Specify the type of agent (e.g., short-term).
  -h --help               Show this help message and exit.
"""

from short_term.agent import Agent
from docopt import docopt

def main(_agent_type, _window_size, _batch_size, _episode_count, _pretrained):

    model_name = 'test'
    print(f"### Training agent {model_name} with the arguments:", _agent_type, _window_size, _batch_size, _episode_count, _pretrained)
    agent = Agent(_window_size, model_name, pretrained)

    # Get these later
    x_train = []
    x_val = []

    for step in range(0, _episode_count):
        # train the model
        # evaluate the model
        pass


if __name__ == "__main__":
    args = docopt(__doc__)

    agent_type = args["--agent-type"]
    window_size = args["--window-size"]
    batch_size = args["--batch-size"]
    episode_count = args["--episode-count"]
    pretrained = args["--pretrained"]

    try:
        main(agent_type, window_size, batch_size, episode_count, pretrained)
    except KeyboardInterrupt:
        print("### Keyboard Interrupt: Exiting.")
