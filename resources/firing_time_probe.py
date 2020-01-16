##  Made by Chris Beem, dec 10th 2019
##  Function: Test for printing each neuron fiering at each timestep
import nengo
from nengo.utils.neurons import spikes2events

import numpy as np

global timestep

with nengo.Network() as model:

    input = nengo.Node(1)
    a = nengo.Ensemble(n_neurons=8, dimensions=1)
    b = nengo.Ensemble(n_neurons=8, dimensions=1)
    spikes_probe = nengo.Probe(a.neurons, synapse=None)

    w = 2 * np.random.randn(b.n_neurons, a.n_neurons) / b.n_neurons
    timestep = 0;
    def my_rule(t, input):
        global timestep
        global w
        p = sim.data[spikes_probe]
        if(timestep>0):
            print("T:{} neurons {}".format(timestep,p[timestep-1]))

        output = np.dot(w, input) * 0.001
        w += np.random.randn(*w.shape) * 0.0001  # learning rule/rate
        timestep+=1
        return output

    learner = nengo.Node(my_rule, size_in=a.n_neurons, size_out=b.n_neurons)
    nengo.Connection(a.neurons, learner, synapse=None)
    nengo.Connection(learner, b.neurons, synapse=0.05)
    nengo.Connection(input, a)

with nengo.Simulator(model) as sim:
    sim.run(5.0)

spikes = sim.data[spikes_probe]

for i,spike in enumerate(spikes):
    print(i,spike,spike[0])

# print("RANGE {}".format(spikes_probe))

spike_times = spikes2events(sim.trange(), spikes)

# print the first 10 spikes of the
#print(spike_times[0][:10])
