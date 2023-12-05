## Driver Code
* train_bot.py: Driver code to start training of the agent with the provided parameters.
Saves the trained model in /models directory in the format <model_name>_ep<episode_count>\_wd<window_size>_bs<batch_size>
  * Example Usage:
```python .\train_bot.py --agent-type short-term --window-size 10 --batch-size 50 --episode-count 0```
  * Data: train_data, val_data variables inside main function.
* eval_bot.py: Driver code to evaluate the trained model with the provided parameters.
  * Example Usage:
```python .\eval_bot.py ./data/GOOG_2019.csv --window-size 10 --model-name test_ep0_wd10_bs50```

## Agent & Models
* agent.py:
  * Huber Loss:
    The code defines a custom Huber loss function (huber_loss) to be used during the training of the DQN.
  * Agent Class: The Agent class represents the DQN-based trading agent. 
    * The constructor (__init__) initializes the agent's parameters, 
     model configuration, and optionally loads a pre-trained model. 
    
    * The remember method stores a tuple of ```(state, action, reward, next_state, done)``` in the replay buffer.
    
    * The ```act``` method selects an action, exploring with probability epsilon.
      
    * The ```train_experience_replay``` method trains the agent's neural network using experience replay, a technique that samples random batches from the replay buffer.
      
    * The save and load methods handle saving and loading trained models.

* methods.py:
    * train_model:
      * agent.inventory: A list to keep track of the stocks the agent currently holds 
      * avg_loss: A list to store the average loss during training 
      * state: The initial state of the agent, obtained by calling the get_state function on the first ```window_size + 1``` data points 
      * Main loop: 
              Computes the next_state based on the current time step
              The tuple ```(state, action, reward, next_state, done)``` 
              is stored in the agent's memory for experience replay buffer 
      * If the agent's memory has accumulated enough experiences (larger than batch_size), it calls experience replay by calling agent.train_experience_replay with a mini-batch of size batch_size
      * Every 10 episodes, the model is saved by calling agent.save.
  
    * evaluate_model: 
      * history: A list to record the actions taken by the agent during the evaluation.
      * agent.inventory: A list to keep track of the agent's holdings (stocks, for example).
      * state: The initial state for the agent, obtained using the get_state function.
      * done: A boolean variable indicating whether the evaluation is done.
      * The state, action, reward, next state, and done flag are appended to the agent's memory.

## Ops & Utils
* ops.py
  * sigmoid: Sigmoid function
  * get_state: Gets a sample of window-size units (days in this case)
* utils.py: Utility functions