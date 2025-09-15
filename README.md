# Caminho Mais Longo em Grafos Acíclicos Direcionados (DAGs)

Implementação em Python para resolver o problema do caminho mais longo em um Grafo Acíclico Direcionado (DAG), desenvolvido como parte da disciplina de Algoritmos Avançados.

**Autor:** Jairson Steinert  
**Professora:** Ma. Beatriz Michelson Reichert  
**Disciplina:** Algoritmos Avançados

## 📜 Descrição do Problema

Este script lê um arquivo de entrada contendo:
- O número de vértices do grafo
- Uma matriz de adjacência com pesos (valores inteiros) 
- Os vértices de origem e destino

O objetivo é calcular o **caminho simples com peso máximo** entre a origem e o destino, assumindo que o grafo é direcionado e acíclico.

### Requisitos do Problema

- ✅ O grafo deve ser **direcionado e acíclico (DAG)**
- ✅ Pesos podem ser **negativos**, mas o valor `0` indica ausência de aresta
- ✅ Os índices dos vértices começam em **0**

## 🧠 Abordagem Utilizada

1. **Ordenação Topológica**: Utiliza o algoritmo de Kahn para processar os vértices em ordem linear
2. **Programação Dinâmica**: 
   - Mantém um vetor de distâncias máximas a partir da origem
   - Inicializa `dist[origem] = 0` e `-∞` (representado por `None`) para os demais
   - Para cada vértice na ordem topológica, atualiza as distâncias dos vizinhos
   - Registra o predecessor para reconstruir o caminho final

## ✨ Funcionalidades Avançadas

- **🔍 Detecção de Ciclos**: Identifica ciclos no grafo e exibe o caminho completo que forma o ciclo
- **⚠️ Detecção de Arestas Duplicadas**: Verifica valores duplicados na mesma linha da matriz
- **📍 Localização Precisa de Erros**: Mostra linha e posição exatas no arquivo para correções
- **💡 Sugestões de Correção**: Fornece instruções detalhadas para corrigir problemas detectados
- **📝 Parsing Inteligente**: Ignora automaticamente linhas vazias e comentários (`#`)
- **🎨 Formatação Adaptativa**: Caminhos longos são quebrados em linhas para melhor legibilidade

## 📥 Instalação e Download

### Opção 1: Git Clone (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/Jairson-Steinert/N1_Algoritimos_Avancados.git

# Entre na pasta do projeto
cd N1_Algoritimos_Avancados
```

### Opção 2: Download ZIP

1. Acesse o repositório no GitHub
2. Clique em **"Code"** → **"Download ZIP"**
3. Extraia o arquivo ZIP
4. Abra o terminal na pasta extraída

## Configuração do Ambiente

### 1. Criar Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 2. Verificar Instalação

```bash
python --version  # Deve retornar Python 3.x
```

## 🛠️ Como Executar

```bash
# Executar com arquivo específico
python n1.py entrada.txt

# Ou usar arquivo padrão
python n1.py
```

> **Nota:** Se nenhum arquivo for especificado, o script usará `entrada.txt` por padrão.

## 📁 Formato do Arquivo de Entrada

O arquivo deve seguir esta estrutura:

1. **Primeira linha**: Número inteiro `N` (quantidade de vértices)
2. **Próximas `N` linhas**: Matriz de adjacência `N x N`
3. **Última linha**: Dois inteiros representando `origem` e `destino`

### Exemplo de Arquivo (`entrada.txt`)

```txt
# Número de vértices
5

# Matriz de adjacência (5x5)
0 5 3 0 0
0 0 8 12 0
0 0 0 4 7
0 0 0 0 6
0 0 0 0 0

# Origem e destino (índices começam em 0)
0 4
```

## 📊 Exemplos de Saída

### ✅ Execução Bem-sucedida

```
Matriz adjacência:

0 5 3 0 0
0 0 8 12 0
0 0 0 4 7
0 0 0 0 6
0 0 0 0 0

Origem: 0
Destino: 4

Resultado:

  • Caminho máximo: [0, 1, 3, 4]
  • Peso total: 23
```

### ❌ Erro: Ciclo Detectado

```
ERRO DE GRAFO: Ciclo detectado!
Ciclo encontrado: 8 → 9 → 10 → 8
Problema: Este arquivo contém um grafo Cíclico, mas o algoritmo/enunciado da questão exige grafos Acíclicos (DAG)

Detalhes das arestas do ciclo:
   • Vértice 8 → Vértice 9 (peso: 4)
   • Vértice 9 → Vértice 10 (peso: 6)
   • Vértice 10 → Vértice 8 (peso: 7)

SUGESTÃO DE CORREÇÃO:
   Para quebrar o ciclo, remova a aresta que o fecha:
   No arquivo 'teste.txt', linha 13 (linha 11 da matriz), posição 9
   Substitua o valor '7' por '0'
   Isso removerá a aresta 10 → 8 e tornará o grafo acíclico
```

### ⚠️ Erro: Valores Duplicados

```
ERRO: Valor '5' duplicado!
Arquivo: teste.txt
Localização: Linha 4 do arquivo (linha 1 da matriz), colunas 2 e 4
Correção: Substitua uma das posições por '0'
```

## 🏗️ Estrutura do Projeto

```
N1_Algoritimos_Avancados/
├── n1.py                         # Arquivo principal com o algoritmo
├── README.md                     # Este arquivo
├── entrada.txt                   # Arquivo de entrada padrão
├── teste.txt                     # Arquivo de teste básico
├── teste_negativo.txt            # Teste com pesos negativos e grafo grande
├── Relatório_N1_Algoritmos_Avançados.pdf  # Relatório acadêmico do projeto
```

## 📈 Complexidade

- **Tempo**: O(V + E) - Linear no número de vértices e arestas
- **Espaço**: O(V) - Para armazenar as estruturas auxiliares

## 👨‍💻 Autor

**Jairson Steinert**
- GitHub: [@Jairson-Steinert](https://github.com/Jairson-Steinert)
- Email: j.steinert@catolicasc.edu.br

---

*Trabalho desenvolvido para a disciplina de Algoritmos Avançados do Centro Universitário – Católica de Santa Catarina, sob orientação da Prof. Ma. Beatriz Michelson Reichert.*
