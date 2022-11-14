"""Etruria Guerra Bot

Grotte di Castro merda.
"""


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import emoji

def get_confinanti(etruria_matrix, attacker, comuni):
    loc = np.zeros(len(etruria_matrix[0]))
    loc[attacker] = 1
    confinanti = etruria_matrix @ loc
    comuni_confinanti = []
    idx_cc = []
    for i in range(len(confinanti)):
        if confinanti[i] == 1:
            idx_cc.append(i)
            comuni_confinanti.append(comuni[i])
    return confinanti, comuni_confinanti, idx_cc

def guerra(verbose=False):
    t = 1

    etruria = pd.read_excel('Etruria.xlsx')
    etruria.set_index("indice", inplace=True)

    etruria_matrix = etruria.to_numpy()

    comuni = list(etruria.columns)
    owners = np.arange(0, len(comuni))

    while len(np.unique(owners)) > 1:
        attacker = np.random.randint(0, high=len(etruria_matrix[0]))

        confinanti, comuni_confinanti, idx_cc = get_confinanti(etruria_matrix, attacker, comuni)
        
        if len(np.unique(np.append(owners[idx_cc], owners[attacker]))) == 1:
            continue

        defender = np.random.randint(0, high=sum(confinanti))
        while owners[attacker] == owners[idx_cc[defender]]:
            defender = np.random.randint(0, high=sum(confinanti))
        if verbose:
            print('#EtrurianWar')

            print(emoji.emojize(f'Un saluto etrusco! :sunrise:. Siamo alla battaglia numero #{t}  \nCe so ancora {len(np.unique(owners))} regni :castle:.'))
            print("================================================")
            print(f"'l regno de {comuni[owners[attacker]]} attacca:")
            print("================================================")
            print(emoji.emojize(":slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine: :slot_machine:"))
            print("================================================")
            print(f"Viene preso de mira 'l territorio de {comuni_confinanti[defender]}, del regno di {comuni[owners[idx_cc[defender]]]}.")
            print("================================================")
            print(emoji.emojize("Ai posti di combattimento Etruschi! :dagger:"))
        rolldice = np.random.rand()

        attack_boost = np.count_nonzero(owners == owners[attacker])
        defender_boost = np.count_nonzero(owners == owners[idx_cc[defender]])
        rolldice = rolldice*attack_boost/defender_boost

        if comuni[idx_cc[defender]] == '?':
            rolldice = rolldice/1.5
        if comuni[owners[attacker]] == '?':
            rolldice = 2.5*rolldice
        if comuni[owners[attacker]] == '?':
            rolldice *= 0.75*rolldice
        if comuni[attacker] == '?':
            rolldice = 2.5*rolldice
        if comuni[owners[attacker]] == '?':
            rolldice = 1.1*rolldice
        if comuni[owners[attacker]] == '?' and comuni[idx_cc[defender]] == '?':
            rolldice = 5*rolldice
        if comuni[owners[attacker]] == '?' and comuni[idx_cc[defender]] == '?':
            rolldice = 0.2*rolldice
        if comuni[attacker] == '?' and (comuni[idx_cc[defender]] == '?' or comuni[idx_cc[defender]] == '?' or comuni[idx_cc[defender]] == '?'):
            rolldice = 3
        if comuni[idx_cc[defender]] == '?' or comuni[idx_cc[defender]] == '?':
            rolldice = 0.5*rolldice
        if comuni[idx_cc[defender]] == '?':
            rolldice = 0.75*rolldice
        if comuni[attacker] == '?':
            rolldice = 0.25*rolldice
        if comuni[attacker] == '?':
            rolldice = 0.25*rolldice
        if owners['?'] == attacker:
            rolldice *= 2

        if rolldice > 0.25:  
            if verbose:
                print(f'Vince {comuni[owners[attacker]]}.')
            oldowner_id = owners[idx_cc[defender]]
            owners[idx_cc[defender]] = owners[attacker]
            if verbose:
                if oldowner_id not in owners:
                    print(emoji.emojize(f"Il regno di {comuni[oldowner_id]} si estingue :skull:."))
                print(f'Ora il territorio di {comuni[idx_cc[defender]]} appartiene a {comuni[owners[attacker]]}.')

                print("================================================")
                print("================================================")
            t += 1
        else:
            if verbose:
                print(emoji.emojize(f'Il regno di {comuni[owners[idx_cc[defender]]]} riesce a difendersi a {comuni_confinanti[defender]} :shield:, nulla di fatto.'))
                print("================================================")
                print("================================================")
            t += 1
    return t #owners[attacker]

mc = []
variance_history = []
samples = 1
for i in range(samples):
    # print(i/samples)
    winner = guerra(verbose=True)
    mc.append(winner)
    # variance_history.append(np.var(mc))

# plt.hist(mc, bins=60, density=True)
# plt.grid(True)
# plt.savefig('durata.png')

# plt.figure()
# plt.plot(variance_history)
# plt.grid(True)
# plt.savefig('var_h.png')
