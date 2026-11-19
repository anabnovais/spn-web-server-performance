# 📊 Avaliação de Desempenho de Servidor Web com Cache e Pool de Workers via Redes de Petri Estocásticas

## 🎯 Visão Geral do Projeto

Servidores web modernos lidam com cargas heterogêneas que combinam requisições leves atendidas diretamente em cache (_cache hit_) e requisições dinâmicas que exigem processamento intensivo e consultas a bancos de dados (_cache miss_).

Neste projeto, propõe-se e avalia-se um modelo **GSPN** no simulador **Jupiter Analytics** para investigar como a taxa de chegada de requisições ($\lambda$), o número de threads trabalhadoras ($N_{\text{SERV}}$) e a capacidade máxima de admissão ($K_{\text{SIS}}$) impactam a vazão, a utilização, a taxa de descarte (HTTP 503) e os tempos médios de fila e resposta.

### 🏗️ Arquitetura e Parâmetros de Referência

| Parâmetro                     |      Símbolo      |    Valor Base     | Descrição                                                  |
| :---------------------------- | :---------------: | :---------------: | :--------------------------------------------------------- |
| **Taxa de chegada**           |     $\lambda$     |    `70 req/s`     | Processo de chegada exponencial ($\text{IAT} = 1/\lambda$) |
| **Serviço estático (_hit_)**  | $\text{ST\_EST}$  | `0,02 s` (20 ms)  | Atendimento rápido via cache em memória (peso 70%)         |
| **Serviço dinâmico (_miss_)** | $\text{ST\_DIN}$  | `0,13 s` (130 ms) | Processamento de aplicação/banco de dados (peso 30%)       |
| **Pool de workers**           | $N_{\text{SERV}}$ |    `4 workers`    | Número máximo de requisições atendidas em paralelo         |
| **Capacidade total**          | $K_{\text{SIS}}$  |     `16 req`      | Limite total do sistema (4 em serviço + 12 em fila)        |

---
