# 📊 Avaliação de Desempenho de Servidor Web com Cache e Pool de Workers via Redes de Petri Estocásticas

![Modelagem](https://img.shields.io/badge/Modelagem-GSPN%20%7C%20Jupiter%20Analytics-blue)
![Linguagem](https://img.shields.io/badge/An%C3%A1lise-Python%203%20%7C%20Matplotlib%20%7C%20Pandas-green)
![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen)

Repositório oficial contendo o modelo em Redes de Petri Estocásticas Generalizadas (GSPN), os conjuntos de dados brutos exportados das simulações, os scripts de visualização e os gráficos gerados para o artigo:

> **"Modelagem e Avaliação de Desempenho de um Servidor Web com Cache e Pool de Workers Utilizando Redes de Petri Estocásticas"**  
> *Ana Beatriz Novais de Castro — Universidade Federal do Piauí (UFPI), Picos, PI, Brasil*

---

## 🎯 Visão Geral do Projeto

Servidores web modernos lidam com cargas heterogêneas que combinam requisições leves atendidas diretamente em cache (*cache hit*) e requisições dinâmicas que exigem processamento intensivo e consultas a bancos de dados (*cache miss*). 

Neste projeto, propõe-se e avalia-se um modelo **GSPN** no simulador **Jupiter Analytics** para investigar como a taxa de chegada de requisições ($\lambda$), o número de threads trabalhadoras ($N_{\text{SERV}}$) e a capacidade máxima de admissão ($K_{\text{SIS}}$) impactam a vazão, a utilização, a taxa de descarte (HTTP 503) e os tempos médios de fila e resposta.

### 🏗️ Arquitetura e Parâmetros de Referência

| Parâmetro | Símbolo | Valor Base | Descrição |
| :--- | :---: | :---: | :--- |
| **Taxa de chegada** | $\lambda$ | `70 req/s` | Processo de chegada exponencial ($\text{IAT} = 1/\lambda$) |
| **Serviço estático (*hit*)** | $\text{ST\_EST}$ | `0,02 s` (20 ms) | Atendimento rápido via cache em memória (peso 70%) |
| **Serviço dinâmico (*miss*)** | $\text{ST\_DIN}$ | `0,13 s` (130 ms) | Processamento de aplicação/banco de dados (peso 30%) |
| **Pool de workers** | $N_{\text{SERV}}$ | `4 workers` | Número máximo de requisições atendidas em paralelo |
| **Capacidade total** | $K_{\text{SIS}}$ | `16 req` | Limite total do sistema (4 em serviço + 12 em fila) |

---

## 📁 Estrutura do Repositório

```text
spn-web-server-performance/
├── model/                  # Modelo GSPN implementado no Jupiter Analytics (.json)
├── data/                   # Dados brutos exportados das simulações estacionárias (.csv)
├── scripts/                # Scripts Python para processamento e geração dos gráficos
│   └── gerar_graficos.py
├── results/                # Figura do modelo SPN e gráficos consolidados (.png)
│   ├── modelo_spn.png
│   ├── fig1_E1_demanda.png
│   ├── fig2_E2_recursos.png
│   ├── fig3_E3_capacidade.png
│   └── fig4_E4_combinado.png
└── README.md
```

---

## 🧪 Planejamento Experimental

As simulações foram conduzidas em **regime estacionário** com nível de confiança de **95%** (32 amostras por ponto experimental), organizadas em quatro cenários:

* **E1 — Variação da Demanda:** $\lambda \in \{30, 50, 70, 90, 110\}\text{ req/s}$
* **E2 — Variação de Recursos:** $N_{\text{SERV}} \in \{2, 4, 8\}\text{ workers}$
* **E3 — Variação da Capacidade:** $K_{\text{SIS}} \in \{8, 16, 32\}\text{ requisições}$
* **E4 — Escalonamento Proporcional:** $C_1=(35,2,8)$, $C_2=(70,4,16)$ e $C_3=(140,8,32)$

### 📌 Principais Conclusões

1. **Gargalo Primário:** O estágio de processamento (`P_Servidores`) satura próximo a **75,5 req/s** com 4 *workers*, limitando a vazão efetiva sob alta demanda.
2. **Fila vs. Latência (*Bufferbloat*):** Aumentar isoladamente a capacidade da fila ($K_{\text{SIS}} = 32$) reduz os descartes para `2,51%`, mas eleva o tempo médio de resposta em **+152,8%** (`183,3 ms`) sem aumentar a capacidade real de vazão.
3. **Ganho de Escala Estatística (*Pooling*):** O escalonamento proporcional ($C_1 \rightarrow C_3$) reduz a probabilidade de descarte em **79,6%** (`13,34%` para `2,72%`) e melhora simultaneamente a latência e a eficiência de utilização (`90,33%`).

---

## 🚀 Como Reproduzir os Gráficos

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU-USUARIO/spn-web-server-performance.git
   cd spn-web-server-performance
   ```

2. **Instale as dependências Python:**
   ```bash
   pip install pandas matplotlib numpy
   ```

3. **Execute o script de visualização:**
   ```bash
   python scripts/gerar_graficos.py
   ```
   Os gráficos atualizados serão salvos no diretório `results/`.

---

## 📄 Como Citar

Caso utilize este modelo ou os dados disponibilizados em sua pesquisa, cite o trabalho como:

```bibtex
@inproceedings{castro2026spnwebserver,
  author    = {Castro, Ana Beatriz Novais de},
  title     = {Modelagem e Avalia{\c{c}}{\~a}o de Desempenho de um Servidor Web com Cache e Pool de Workers Utilizando Redes de Petri Estoc{\'a}sticas},
  year      = {2026},
  address   = {Picos, PI, Brasil},
  note      = {Universidade Federal do Piau{\'i} (UFPI)}
}
```