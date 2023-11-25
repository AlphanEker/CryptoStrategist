"""Usage:
  train_bot.py [--agent-type=<agent_type>] [--window-size=<window-size>]
  [--batch-size=<batch-size>] [--episode-count=<episode-count>]

Options:
  --agent-type=<type>     Specify the type of agent (e.g., short-term).
  -h --help               Show this help message and exit.
"""

from short_term.agent import Agent
from docopt import docopt

def main(agent_type, window_size, batch_size, episode_count):
    print("Arguments:", agent_type, window_size, batch_size, episode_count)


if __name__ == "__main__":
    args = docopt(__doc__)

    agent_type = args["--agent-type"]
    window_size = args["--window-size"]
    batch_size = args["--batch-size"]
    episode_count = args["--episode-count"]

    main(agent_type, window_size, batch_size, episode_count)