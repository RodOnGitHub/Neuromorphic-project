import pickle

spike_times = pickle.load(open("iris_spikes", 'rb'))

from brian2 import *

N = 8
taum = 10*ms
taupre = 20*ms
taupost = taupre
Ee = 0*mV
vt = 1*mV
vr = -5*mV
El = -74*mV
taue = 5*ms
F = 1*Hz
gmax = .01
dApre = .01
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax

eqs_neurons = '''
dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
dge/dt = -ge / taue : 1
'''

input = PoissonGroup(8, rates=F)
neurons = NeuronGroup(3, eqs_neurons, threshold='v>vt', reset='v = vr',
                      method='exact', refractory=3*ms)
S = Synapses(input, neurons,
             '''w : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)''',
             on_pre='''ge += w
                    Apre += dApre
                    w = clip(w + Apost, 0, gmax)''',
             on_post='''Apost += dApost
                     w = clip(w + Apre, 0, gmax)''',
             )
S.connect()
S.w = 'rand() * gmax'
mon = StateMonitor(S, 'w', record=[0, 1])
spikemon=SpikeMonitor(neurons)
s_mon = SpikeMonitor(input)

run(6*ms, report='text')


subplot(511)
plot(S.w / gmax, '.k')
ylabel('Weight / gmax')
xlabel('Synapse index')
subplot(512)
hist(S.w / gmax, 20)
xlabel('Weight / gmax')
subplot(513)
plot(mon.t/second, mon.w.T/gmax)
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(514)
plot(s_mon.t/ms, s_mon.i, '.k', ms=3)
subplot(515)
plot(spikemon.t/ms, spikemon.i, '.k', ms=3)
tight_layout()
show()

