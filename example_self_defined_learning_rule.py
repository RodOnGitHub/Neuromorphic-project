#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
implementing self defined learning rule in a node


"""

import nengo
import numpy as np

model = nengo.Network()
with model:
    input = nengo.Node(1)
    a = nengo.Ensemble(n_neurons=100, dimensions=1)
    b = nengo.Ensemble(n_neurons=50, dimensions=1)
    
    nengo.Connection(input,a)

    w = 2*np.random.randn(b.n_neurons, a.n_neurons)/b.n_neurons
    def my_rule(t, input):
        global w
        output = np.dot(w, input)*0.001
        w += np.random.randn(*w.shape)*0.01   # learning rule
        return output
    
    learner = nengo.Node(my_rule, size_in=a.n_neurons,
                     size_out=b.n_neurons)
                     
    nengo.Connection(a.neurons, learner, synapse=None)
    nengo.Connection(learner, b.neurons, synapse=0.05)