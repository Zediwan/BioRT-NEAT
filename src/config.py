# from enum import Enum

# class ControlType(Enum):
#     none = 0
#     Velocity = 1
#     Acceleration = 2

class conf:
    class win:
        window_width = 2560
        window_height = 1440
        bit_depth = 24

    class net:
        input_count = 2
        output_count = 1

    class sim:
        segment_size = 100.0
        slider_length = 500.0
        max_gravity = 1000.0
        segments_count = 2
        world_size = [slider_length + 2.2 * segments_count * segment_size, segments_count * segment_size * 2.25]

    class sel:
        population_size = 1000
        max_iteration_time = 60.0
        elite_ratio = 0.35

    class mut:
        # Structure
        new_node_proba = 0.05
        new_conn_proba = 0.8
        # Node
        new_bias_proba = 0.2
        new_response_proba = 0.2
        new_af_proba = 0.2
        new_agg_proba = 0.2
        bias_sigma = 1
        response_sigma = 1

        # Connection
        new_weight_proba = 0.2
        weight_sigma = 1

        weight_range = 1.0
        weight_small_range = 0.01
        mut_count = 4
        max_hidden_nodes = 30

    class exp:
        seed_offset = 101
        best_save_period = 10
        exploration_period = 1000