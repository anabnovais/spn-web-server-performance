import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuração visual padrão IEEE
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial'],
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.titleweight': 'bold',
    'axes.labelsize': 10,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

def load_jupiter_csv(path):
    df = pd.read_csv(path, sep=';')
    df['Metric'] = df['Metric'].str.strip()
    return df.set_index('Metric')

def extract_exp(mapping):
    rows = []
    for label, path in mapping:
        df = load_jupiter_csv(path)
        rows.append({
            'Label': label,
            'TP': df.loc['TP', 'Value'], 'TP_hw': df.loc['TP', 'Half-Width'],
            'U': df.loc['U', 'Value'], 'U_hw': df.loc['U', 'Half-Width'],
            'DP': df.loc['DP', 'Value'], 'DP_hw': df.loc['DP', 'Half-Width'],
            'MRT': df.loc['MRT', 'Value'] * 1000, 'MRT_hw': df.loc['MRT', 'Half-Width'] * 1000,
            'MQT': df.loc['MQT', 'Value'] * 1000, 'MQT_hw': df.loc['MQT', 'Half-Width'] * 1000,
            'MPT': df.loc['MPT', 'Value'] * 1000, 'MPT_hw': df.loc['MPT', 'Half-Width'] * 1000,
        })
    return pd.DataFrame(rows)

# Experimento E1: Variação de LAMBDA (30, 50, 70, 90, 110 req/s)
e1_data = pd.DataFrame({
    'LAMBDA': [30, 50, 70, 90, 110],
    'TP':     [29.9949, 49.6179, 65.3754, 72.6040, 74.7656],
    'U':      [39.7456, 65.7417, 86.6414, 96.1816, 99.0339],
    'DP':     [0.0053,  0.6770,  6.6891,  19.3044, 32.0772],
    'MRT':    [56.2,    74.4,    114.1,   152.2,   175.5],
    'MQT':    [3.2,     21.4,    61.1,    99.2,    122.5],
    'MPT':    [53.0,    53.0,    53.0,    53.0,    53.0],
})

# Experimentos E2, E3 e E4 (lidos diretamente dos CSVs exportados do Jupiter)
e2_df = extract_exp([
    ('2', 'E2/N_SERVER2.csv'),
    ('4 (Ref)', 'E2/N_SERVER4.csv'),
    ('8', 'E2/N_SERVER8.csv'),
])

e3_df = extract_exp([
    ('8', 'E3/K_SIS8.csv'),
    ('16 (Ref)', 'E3/K_SIS16.csv'),
    ('32', 'E3/K_SIS32.csv'),
])

e4_df = extract_exp([
    ('C1\n(35, 2, 8)', 'E4/C1.csv'),
    ('C2 (Ref)\n(70, 4, 16)', 'E4/C2.csv'),
    ('C3\n(140, 8, 32)', 'E4/C3.csv'),
])

os.makedirs('graficos', exist_ok=True)

# Plot E1 (Linhas)
fig, axs = plt.subplots(2, 2, figsize=(9.5, 6.8))
x = e1_data['LAMBDA']

axs[0, 0].plot(x, e1_data['TP'], 'o-', color='#1f77b4', lw=2, markersize=6, label='Vazão (TP)')
axs[0, 0].axhline(75.47, color='#d62728', ls=':', lw=1.3, label='Capacidade Máx. (~75,5 req/s)')
axs[0, 0].set_title('(a) Throughput (TP)')
axs[0, 0].set_xlabel('Taxa de Chegada $\\lambda$ (req/s)')
axs[0, 0].set_ylabel('Vazão (req/s)')
axs[0, 0].set_xticks(x)
axs[0, 0].legend(loc='lower right', fontsize=8.5)

axs[0, 1].plot(x, e1_data['U'], 's-', color='#2ca02c', lw=2, markersize=6, label='Utilização (U)')
axs[0, 1].set_title('(b) Utilização dos Workers (U)')
axs[0, 1].set_xlabel('Taxa de Chegada $\\lambda$ (req/s)')
axs[0, 1].set_ylabel('Utilização (%)')
axs[0, 1].set_ylim(0, 108)
axs[0, 1].set_xticks(x)
axs[0, 1].legend(loc='lower right', fontsize=8.5)

axs[1, 0].plot(x, e1_data['DP'], '^-', color='#d62728', lw=2, markersize=6, label='Descarte (DP)')
axs[1, 0].set_title('(c) Probabilidade de Descarte (DP)')
axs[1, 0].set_xlabel('Taxa de Chegada $\\lambda$ (req/s)')
axs[1, 0].set_ylabel('Descarte (%)')
axs[1, 0].set_ylim(-2, 38)
axs[1, 0].set_xticks(x)
axs[1, 0].legend(loc='upper left', fontsize=8.5)

axs[1, 1].plot(x, e1_data['MRT'], 'D-', color='#9467bd', lw=2, markersize=5.5, label='Resposta Total (MRT)')
axs[1, 1].plot(x, e1_data['MQT'], 'v--', color='#ff7f0e', lw=1.8, markersize=5.5, label='Espera em Fila (MQT)')
axs[1, 1].plot(x, e1_data['MPT'], 'o:', color='#7f7f7f', lw=1.5, markersize=4.5, label='Processamento (MPT)')
axs[1, 1].set_title('(d) Tempos Médios (MRT, MQT e MPT)')
axs[1, 1].set_xlabel('Taxa de Chegada $\\lambda$ (req/s)')
axs[1, 1].set_ylabel('Tempo (ms)')
axs[1, 1].set_xticks(x)
axs[1, 1].legend(loc='upper left', fontsize=8.5)

fig.suptitle('Experimento E1 — Impacto da Taxa de Chegada ($\\lambda$) ($N_{SERV}=4, K_{SIS}=16$)', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('graficos/fig1_E1_demanda.png')
plt.close()

def plot_bar_exp(df, xlabel, suptitle, filename):
    fig, axs = plt.subplots(2, 2, figsize=(9.5, 6.8))
    idx = np.arange(len(df))
    w = 0.48

    bars = axs[0, 0].bar(idx, df['TP'], width=w, yerr=df['TP_hw'], capsize=4, color='#1f77b4', edgecolor='black', linewidth=0.7)
    axs[0, 0].set_title('(a) Throughput (TP)')
    axs[0, 0].set_xlabel(xlabel)
    axs[0, 0].set_ylabel('Vazão (req/s)')
    axs[0, 0].set_xticks(idx)
    axs[0, 0].set_xticklabels(df['Label'])
    axs[0, 0].set_ylim(0, max(df['TP'])*1.2)
    for b in bars:
        axs[0, 0].text(b.get_x()+b.get_width()/2, b.get_height()+max(df['TP'])*0.03, f"{b.get_height():.2f}", ha='center', va='bottom', fontsize=8.5)

    bars = axs[0, 1].bar(idx, df['U'], width=w, yerr=df['U_hw'], capsize=4, color='#2ca02c', edgecolor='black', linewidth=0.7)
    axs[0, 1].set_title('(b) Utilização dos Workers (U)')
    axs[0, 1].set_xlabel(xlabel)
    axs[0, 1].set_ylabel('Utilização (%)')
    axs[0, 1].set_xticks(idx)
    axs[0, 1].set_xticklabels(df['Label'])
    axs[0, 1].set_ylim(0, 115)
    for b in bars:
        axs[0, 1].text(b.get_x()+b.get_width()/2, b.get_height()+2.5, f"{b.get_height():.1f}%", ha='center', va='bottom', fontsize=8.5)

    bars = axs[1, 0].bar(idx, df['DP'], width=w, yerr=df['DP_hw'], capsize=4, color='#d62728', edgecolor='black', linewidth=0.7)
    axs[1, 0].set_title('(c) Probabilidade de Descarte (DP)')
    axs[1, 0].set_xlabel(xlabel)
    axs[1, 0].set_ylabel('Descarte (%)')
    axs[1, 0].set_xticks(idx)
    axs[1, 0].set_xticklabels(df['Label'])
    axs[1, 0].set_ylim(0, max(df['DP'])*1.22 if max(df['DP'])>0 else 10)
    for b in bars:
        axs[1, 0].text(b.get_x()+b.get_width()/2, b.get_height()+max(df['DP'])*0.03, f"{b.get_height():.2f}%", ha='center', va='bottom', fontsize=8.5)

    w2 = 0.26
    b1 = axs[1, 1].bar(idx - w2, df['MRT'], width=w2, yerr=df['MRT_hw'], capsize=3, color='#9467bd', edgecolor='black', linewidth=0.6, label='MRT (Total)')
    b2 = axs[1, 1].bar(idx,      df['MQT'], width=w2, yerr=df['MQT_hw'], capsize=3, color='#ff7f0e', edgecolor='black', linewidth=0.6, label='MQT (Fila)')
    b3 = axs[1, 1].bar(idx + w2, df['MPT'], width=w2, yerr=df['MPT_hw'], capsize=3, color='#7f7f7f', edgecolor='black', linewidth=0.6, label='MPT (Proc.)')
    axs[1, 1].set_title('(d) Tempos Médios (MRT, MQT e MPT)')
    axs[1, 1].set_xlabel(xlabel)
    axs[1, 1].set_ylabel('Tempo (ms)')
    axs[1, 1].set_xticks(idx)
    axs[1, 1].set_xticklabels(df['Label'])
    axs[1, 1].set_ylim(0, max(df['MRT'])*1.22)
    axs[1, 1].legend(loc='upper right', fontsize=8)
    for b in b1:
        axs[1, 1].text(b.get_x()+b.get_width()/2, b.get_height()+max(df['MRT'])*0.02, f"{b.get_height():.1f}", ha='center', va='bottom', fontsize=7.5)

    fig.suptitle(suptitle, fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

plot_bar_exp(e2_df, 'Número de Workers ($N_{SERV}$)', 'Experimento E2 — Variação de Recursos ($\\lambda=70$ req/s, $K_{SIS}=16$)', 'graficos/fig2_E2_recursos.png')
plot_bar_exp(e3_df, 'Capacidade do Sistema ($K_{SIS}$ requisições)', 'Experimento E3 — Variação da Capacidade ($\\lambda=70$ req/s, $N_{SERV}=4$)', 'graficos/fig3_E3_capacidade.png')
plot_bar_exp(e4_df, 'Configuração ($\\lambda$, $N_{SERV}$, $K_{SIS}$)', 'Experimento E4 — Escalonamento Proporcional Combinado', 'graficos/fig4_E4_combinado.png')
print("Gráficos gerados com sucesso na pasta graficos/!")
