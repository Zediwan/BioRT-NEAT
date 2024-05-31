from ..genome import Genome

class FeedForwardNetwork():
    def __init__(self, inputs, outputs, node_evals):
        self.input_nodes = inputs
        self.output_nodes = outputs
        self.node_evals = node_evals
        self.values = dict((key, 0.0) for key in inputs + outputs)

    def activate(self, inputs):
        if len(self.input_nodes) != len(inputs):
            raise RuntimeError("Expected {0:n} inputs, got {1:n}".format(len(self.input_nodes), len(inputs)))

        for k, v in zip(self.input_nodes, inputs):
            self.values[k] = v

        for node, act_func, agg_func, bias, response, links in self.node_evals:
            node_inputs = []
            for i, w in links:
                node_inputs.append(self.values[i] * w)
            s = agg_func(node_inputs)
            self.values[node] = act_func(bias + response * s)

        return [self.values[i] for i in self.output_nodes]

    @staticmethod
    def create(genome: Genome):
        """ Receives a genome and returns its phenotype (a FeedForwardNetwork). """

        # Gather expressed connections.
        connections = [cg.key for cg in genome.connections.values() if cg.enabled]

        layers = FeedForwardNetwork._feed_forward_layers(Genome.INPUT_KEYS, Genome.OUTPUT_KEYS, connections)
        node_evals = []
        for layer in layers:
            for node in layer:
                inputs = []
                for conn_key in connections:
                    inode, onode = conn_key
                    if onode == node:
                        cg = genome.connections[conn_key]
                        inputs.append((inode, cg.weight))

                ng = genome.nodes[node]
                aggregation_function = ng.aggregation
                activation_function = ng.activation
                node_evals.append((node, activation_function, aggregation_function, ng.bias, ng.response, inputs))

        return FeedForwardNetwork(Genome.INPUT_KEYS, Genome.OUTPUT_KEYS, node_evals)

    @staticmethod
    def _feed_forward_layers(inputs, outputs, connections) -> list[set[str]]:
        """
        Collect the layers whose members can be evaluated in parallel in a feed-forward network.
        :param inputs: list of the network input nodes
        :param outputs: list of the output node identifiers
        :param connections: list of (input, output) connections in the network.

        Returns a list of layers, with each layer consisting of a set of node identifiers.
        Note that the returned layers do not contain nodes whose output is ultimately
        never used to compute the final network output.
        """

        required = FeedForwardNetwork._required_for_output(inputs, outputs, connections)

        layers = []
        s = set(inputs)
        while 1:
            # Find candidate nodes c for the next layer.  These nodes should connect
            # a node in s to a node not in s.
            c = set(b for (a, b) in connections if a in s and b not in s)
            # Keep only the used nodes whose entire input set is contained in s.
            t = set()
            for n in c:
                if n in required and all(a in s for (a, b) in connections if b == n):
                    t.add(n)

            if not t:
                break

            layers.append(t)
            s = s.union(t)

        return layers

    @staticmethod
    def _required_for_output(inputs, outputs, connections):
        """
        Collect the nodes whose state is required to compute the final network output(s).
        :param inputs: list of the input identifiers
        :param outputs: list of the output node identifiers
        :param connections: list of (input, output) connections in the network.
        NOTE: It is assumed that the input identifier set and the node identifier set are disjoint.
        By convention, the output node ids are always the same as the output index.

        Returns a set of identifiers of required nodes.
        """
        assert not set(inputs).intersection(outputs)

        required = set(outputs)
        s = set(outputs)
        while 1:
            # Find nodes not in s whose output is consumed by a node in s.
            t = set(a for (a, b) in connections if b in s and a not in s)

            if not t:
                break

            layer_nodes = set(x for x in t if x not in inputs)
            if not layer_nodes:
                break

            required = required.union(layer_nodes)
            s = s.union(t)

        return required
