def run_state_machine(states_map, starting_state_name, log, input_generator,
                      default_state_data=None):
    """
    State machine loop - uses supplied input generator to activate method on
    a state. Each method can either spawn its own state machine, modify state
    data and request transition to a new state
    :param states_map:
    :param starting_state_name:
    :param log:
    :param input_generator:
    :param default_state_data:
    :return: last state name, last state exit data
    """
    current_state = states_map[starting_state_name]
    current_state_data = default_state_data
    next_state_name = starting_state_name
    current_state_name = starting_state_name
    
    for input_data in input_generator:
        log("Input data: {}".format(input_data))
        
        if input_data in current_state:
            log("Activating action: {}".format(str(current_state[input_data])))
            next_state_name, current_state_data = \
                current_state[input_data](current_state_data, input_generator)
        elif '*' in current_state:
            log("Activating default action: {}".format(str(current_state['*'])))
            next_state_name, current_state_data = \
                current_state['*'](current_state_data, input_generator, input_data)
        
        if next_state_name != current_state_name:
            current_state = states_map[next_state_name]
            current_state_name = next_state_name
    
    return current_state_name, current_state_data
