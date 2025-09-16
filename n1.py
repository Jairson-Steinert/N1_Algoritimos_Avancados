#!/usr/bin/env python3
"""
Prof. Ma. Beatriz Michelson Reichert
Acadêmico: Jairson Steinert

Trabalho N1 - Algoritmos Avançados
Problema do caminho mais longo em grafos acíclicos direcionados (DAG).

Uso: python n1.py [arquivo_entrada.txt]
"""

from __future__ import annotations

import sys
import math
from typing import List, Optional, Tuple


def parse_input(lines: List[str], filename: str = "") -> Tuple[int, List[List[int]], int, int, List[int]]:
    """Analisa as linhas de entrada e retorna o número de vértices, matriz de
    adjacência e índices de origem/destino.

    Linhas que começam com '#' ou linhas vazias são ignoradas.

    Parâmetros
    ----------
    lines : List[str]
        Linhas brutas do arquivo de entrada.

    Retorna
    -------
    Tuple[int, List[List[int]], int, int]
        (n_vertices, adjacency_matrix, origin, destination)
    """
    # Remove comments and blank lines, keeping track of original line numbers
    cleaned = []
    original_line_numbers = []
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        # skip empty lines
        if not stripped:
            continue
        # skip comments
        if stripped.startswith('#'):
            continue
        cleaned.append(stripped)
        original_line_numbers.append(line_num)

    if not cleaned:
        raise ValueError("Arquivo de entrada vazio ou apenas comentários.")

    # Primeiro valor é o número de vértices
    try:
        n_vertices = int(cleaned[0])
    except Exception as e:
        raise ValueError(f"Esperado número de vértices na primeira linha válida: {cleaned[0]}") from e

    # Próximas n_vertices linhas: matriz de adjacência
    adjacency: List[List[int]] = []
    line_idx = 1
    for i in range(n_vertices):
        if line_idx >= len(cleaned):
            raise ValueError(f"Esperadas {n_vertices} linhas de matriz após o número de vértices.")
        parts = cleaned[line_idx].split()
        if len(parts) != n_vertices:
            raise ValueError(
                f"A linha {i+1} da matriz de adjacência deve conter {n_vertices} valores, mas tem {len(parts)}: {cleaned[line_idx]}"
            )
        
        # Detecta valores duplicados não-zero na mesma linha
        non_zero_values = {}
        for j, part in enumerate(parts):
            if part != '0':  # Ignora zeros (são normais)
                if part in non_zero_values:
                    print(f"\nERRO: Valor '{part}' duplicado!")
                    print(f"Arquivo: {filename}")
                    print(f"Localização: Linha {original_line_numbers[line_idx]} do arquivo (linha {i+1} da matriz), colunas {non_zero_values[part]+1} e {j+1}")
                    print(f"Correção: Substitua uma das posições por '0'")
                    raise ValueError(f"Valor duplicado '{part}' encontrado na linha {i+1} do vértice {i}")
                non_zero_values[part] = j
        
        try:
            row = [int(p) for p in parts]
        except ValueError as e:
            raise ValueError(f"Valores inválidos na matriz de adjacência na linha {i+1}: {cleaned[line_idx]}") from e
        adjacency.append(row)
        line_idx += 1

    # Última linha válida: origem e destino
    if line_idx >= len(cleaned):
        raise ValueError("Não foram fornecidos origem e destino.")
    last_parts = cleaned[line_idx].split()
    if len(last_parts) != 2:
        raise ValueError(f"A linha de origem e destino deve ter 2 valores: {cleaned[line_idx]}")
    try:
        origin, destination = map(int, last_parts)
    except Exception as e:
        raise ValueError(f"Valores inválidos para origem e destino: {cleaned[line_idx]}") from e

    # Validate indices
    if not (0 <= origin < n_vertices and 0 <= destination < n_vertices):
        raise ValueError(f"Origem e destino devem estar entre 0 e {n_vertices - 1}.")

    return n_vertices, adjacency, origin, destination, original_line_numbers


def detect_cycle_dfs(n: int, adjacency: List[List[int]]) -> Optional[List[int]]:
    """Detecta um ciclo específico no grafo usando DFS.
    
    Returns
    -------
    Optional[List[int]]
        Lista de vértices que formam um ciclo, ou None se não houver ciclo.
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    
    def dfs_visit(u: int, path: List[int]) -> Optional[List[int]]:
        if u in path:  # Ciclo detectado!
            cycle_start = path.index(u)
            cycle = path[cycle_start:] + [u]
            return cycle
            
        color[u] = GRAY
        path.append(u)
        
        for v in range(n):
            if adjacency[u][v] != 0:  # Há aresta de u para v
                if color[v] == WHITE:
                    result = dfs_visit(v, path.copy())
                    if result:
                        return result
                elif color[v] == GRAY:  # Back edge - ciclo detectado
                    cycle = path[path.index(v):] + [v]
                    return cycle
        
        color[u] = BLACK
        path.pop()
        return None
    
    # Tenta DFS de cada vértice não visitado
    for start in range(n):
        if color[start] == WHITE:
            cycle = dfs_visit(start, [])
            if cycle:
                return cycle
    
    return None


def topological_sort(n: int, adjacency: List[List[int]], filename: str = "", original_line_numbers: Optional[List[int]] = None) -> List[int]:
    """Gera uma ordenação topológica para um grafo direcionado acíclico.

    Utiliza algoritmo de Kahn.

    Parameters
    ----------
    n : int
        Número de vértices.
    adjacency : List[List[int]]
        Matriz de adjacência com pesos. Um valor 0 indica ausência de aresta.

    Returns
    -------
    List[int]
        Lista de vértices em ordem topológica.

    Raises
    ------
    ValueError
        Se o grafo contiver ciclo (não DAG).
    """
    from collections import deque

    indegree = [0] * n
    for u in range(n):
        for v in range(n):
            if adjacency[u][v] != 0:
                indegree[v] += 1
    q = deque([u for u in range(n) if indegree[u] == 0])
    topo_order: List[int] = []
    while q:
        u = q.popleft()
        topo_order.append(u)
        for v in range(n):
            if adjacency[u][v] != 0:
                indegree[v] -= 1
                if indegree[v] == 0:
                    q.append(v)
    if len(topo_order) != n:
        # Detecta e mostra o ciclo específico
        cycle = detect_cycle_dfs(n, adjacency)
        if cycle:
            cycle_str = " → ".join(map(str, cycle))
            print(f"\nERRO DE GRAFO: Ciclo detectado!")
            print(f"Ciclo encontrado: {cycle_str}")
            print(f"Problema: Este arquivo contém um grafo Cíclico, mas o algoritmo/enunciado da questão exige grafos Acíclicos (DAG)")
            
            # Mostra detalhes das arestas do ciclo
            print(f"Detalhes das arestas do ciclo:")
            for i in range(len(cycle) - 1):
                u, v = cycle[i], cycle[i + 1]
                weight = adjacency[u][v]
                print(f"   • Vértice {u} → Vértice {v} (peso: {weight})")
            
            # Identifica a aresta problemática (a que fecha o ciclo)
            last_u, first_v = cycle[-2], cycle[0]
            problem_weight = adjacency[last_u][first_v]
            print(f"\nSUGESTÃO DE CORREÇÃO:")
            print(f"   Para quebrar o ciclo, remova a aresta que o fecha:")
            
            # Calcula linha real do arquivo (matriz começa na linha 2 das linhas válidas)
            if original_line_numbers:
                real_line = original_line_numbers[last_u + 1]  # +1 porque matriz começa na posição 1
                print(f"   No arquivo '{filename}', linha {real_line} (linha {last_u + 1} da matriz), posição {first_v + 1}")
            else:
                print(f"   No arquivo '{filename}', linha {last_u + 1}, posição {first_v + 1}")
            print(f"   Substitua o valor '{problem_weight}' por '0'")
            print(f"   Isso removerá a aresta {last_u} → {first_v} e tornará o grafo acíclico")
            
            raise ValueError(f"Grafo contém ciclo: {cycle_str}")
        else:
            raise ValueError("O grafo possui ciclos e não pode ser ordenado topologicamente.")
    return topo_order


def longest_path_dag(
    n: int, adjacency: List[List[int]], origin: int, destination: int, filename: str = "", original_line_numbers: Optional[List[int]] = None
) -> Tuple[Optional[List[int]], Optional[int]]:
    """Calcula o caminho simples de peso máximo entre origem e destino em um DAG.

    Parameters
    ----------
    n : int
        Número de vértices do grafo.
    adjacency : List[List[int]]
        Matriz de adjacência com pesos. Valor 0 indica ausência de aresta.
    origin : int
        Índice da origem.
    destination : int
        Índice do destino.

    Returns
    -------
    Tuple[Optional[List[int]], Optional[int]]
        Uma tupla contendo o caminho (lista de vértices) e o peso total. Se não
        houver caminho, retorna (None, None).
    """
    try:
        topo = topological_sort(n, adjacency, filename, original_line_numbers)
    except ValueError as e:
        raise ValueError(str(e))

    # Inicializa distâncias: None indica distância -infinito
    dist: List[Optional[int]] = [None] * n
    pred: List[Optional[int]] = [None] * n
    dist[origin] = 0

    # Processa vértices na ordem topológica
    for u in topo:
        # Se a distância é None, vértice inatingível até aqui
        if dist[u] is None:
            continue
        for v in range(n):
            w = adjacency[u][v]
            if w != 0:
                # se o vértice destino ainda não tem distância, tratamos como -inf
                current_dist_u = dist[u]
                if current_dist_u is not None:
                    current_dist_v = dist[v]
                    if current_dist_v is None or current_dist_u + w > current_dist_v:
                        dist[v] = current_dist_u + w
                        pred[v] = u

    # Se destino inatingível
    if dist[destination] is None:
        return None, None

    # Reconstrói caminho de destination até origin
    path = []
    current = destination
    while current is not None:
        path.append(current)
        if current == origin:
            break
        current = pred[current]
    path.reverse()
    if path[0] != origin:
        # origem não foi alcançada
        return None, None
    return path, dist[destination]

def main():
    import sys
    # Determina arquivo de entrada
    input_file = sys.argv[1] if len(sys.argv) >= 2 else "entrada.txt"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_file}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo {input_file}: {e}")
        sys.exit(1)

    try:
        n_vertices, adjacency, origin, destination, original_line_numbers = parse_input(lines, input_file)
    except Exception as e:
        print(f"Erro ao processar o arquivo {input_file}: {e}")
        sys.exit(1)

    # Imprime matriz de adjacência após processar o arquivo
    print("\nMatriz adjacência:")
    print()
    for row in adjacency:
        print(' '.join(str(x) for x in row))

    print(f"\nOrigem: {origin}")
    print(f"Destino: {destination}")

    try:
        path, total_weight = longest_path_dag(n_vertices, adjacency, origin, destination, input_file, original_line_numbers)
    except Exception as e:
        sys.exit(1)

    print("\nResultado:")
    print()
    if path is None:
        print("  • Não há caminho entre a origem e o destino.")
    else:
        # Formatação adaptativa: simples para caminhos curtos, quebrada para extensos
        if len(path) <= 10:
            print("  • Caminho máximo: {}".format(path))
        else:
            print("  • Caminho máximo:")
            vertices_per_line = 15
            for i in range(0, len(path), vertices_per_line):
                line_vertices = path[i:i + vertices_per_line]
                if i == 0:
                    # Primeira linha: abre colchete
                    print("    [{}{}".format(", ".join(map(str, line_vertices)), "," if i + vertices_per_line < len(path) else "]"))
                elif i + vertices_per_line >= len(path):
                    # Última linha: fecha colchete
                    print("    {}]".format(", ".join(map(str, line_vertices))))
                else:
                    # Linhas do meio: apenas vírgulas
                    print("    {},".format(", ".join(map(str, line_vertices))))
        print("  • Peso total: {}".format(total_weight))


if __name__ == "__main__":
    main()