"""
Gerenciador de Tarefas 

Projeto: Cadastrar tarefas, visualizar, concluir,
remover e pesquisar por palavra-chave.

Autor: Luiz Renato Tulio
Curso: Análise e Desenvolvimento de Sistemas
"""

import os


def limpar_tela():
    """Limpa a tela."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa e volta ao menu."""
    input("\nPressione ENTER para voltar ao menu...")


def gerar_proximo_id(tarefas):
    """Gera um ID."""
    if not tarefas:
        return 1
    return max(t["id"] for t in tarefas) + 1


def adicionar_tarefa(tarefas):
    """Ler dados e adicionar tarefa."""
    print("\n=== Adicionar tarefa ===")
    descricao = input("Descrição da tarefa: ").strip()

    if descricao == "":
        print("Você não digitou nenhuma descrição.")
        pausar()
        return

    prioridade_txt = input("Prioridade (1=baixa, 2=média, 3=alta) [2]: ").strip()
    if prioridade_txt == "":
        prioridade = 2
    else:
        try:
            prioridade = int(prioridade_txt)
            if prioridade not in (1, 2, 3):
                print("Prioridade inválida, usando média.")
                prioridade = 2
        except ValueError:
            print("Prioridade inválida, usando média.")
            prioridade = 2

    vencimento = input("Data de vencimento (dd/mm/aaaa) [opcional]: ").strip()

    tarefa = {
        "id": gerar_proximo_id(tarefas),
        "descricao": descricao,
        "prioridade": prioridade,
        "vencimento": vencimento,
        "concluida": False
    }
    tarefas.append(tarefa)
    print(f"Tarefa adicionada. ID: {tarefa['id']}")
    pausar()


def status_txt(concluida):
    return "Concluída" if concluida else "Pendente"


def prioridade_txt(pri):
    if pri == 3:
        return "Alta"
    if pri == 1:
        return "Baixa"
    return "Média"


def listar_tarefas(tarefas):
    """Mostrar tarefas cadastradas."""
    print("\n=== Lista de tarefas ===")
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        pausar()
        return

    for t in tarefas:
        venc = t["vencimento"] if t["vencimento"] else "-"
        print(f"[{t['id']}] {t['descricao']} | {status_txt(t['concluida'])} | "
              f"Prioridade: {prioridade_txt(t['prioridade'])} | Venc.: {venc}")

    pausar()


def encontrar_por_id(tarefas, id_busca):
    """Procura e retorna uma tarefa pelo ID. Se não achar, devolve None."""
    for t in tarefas:
        if t["id"] == id_busca:
            return t
    return None


def marcar_concluida(tarefas):
    """Marcar tarefa como concluída a partir do ID."""
    print("\n=== Concluir tarefa ===")
    if not tarefas:
        print("Não há tarefas para concluir.")
        pausar()
        return

    try:
        id_tarefa = int(input("Digite o ID da tarefa: ").strip())
    except ValueError:
        print("ID inválido.")
        pausar()
        return

    tarefa = encontrar_por_id(tarefas, id_tarefa)
    if tarefa is None:
        print("Não encontrei nenhuma tarefa com esse ID.")
        pausar()
        return

    if tarefa["concluida"]:
        print("Essa tarefa já está concluída.")
    else:
        tarefa["concluida"] = True
        print("Tarefa concluída.")

    pausar()


def remover_tarefa(tarefas):
    """Remove tarefa da lista a partir do ID."""
    print("\n=== Remover tarefa ===")
    if not tarefas:
        print("Não há tarefas para remover.")
        pausar()
        return

    try:
        id_tarefa = int(input("Digite o ID da tarefa: ").strip())
    except ValueError:
        print("ID inválido.")
        pausar()
        return

    tarefa = encontrar_por_id(tarefas, id_tarefa)
    if tarefa is None:
        print("Não encontrei nenhuma tarefa com esse ID.")
        pausar()
        return

    tarefas.remove(tarefa)
    print("Tarefa removida da lista.")
    pausar()


def pesquisar_tarefas(tarefas):
    """Pesquisa por palavra-chave na descrição."""
    print("\n=== Pesquisar tarefas ===")
    if not tarefas:
        print("Não há tarefas para pesquisar.")
        pausar()
        return

    chave = input("Digite uma palavra (ou parte) da descrição: ").strip().lower()
    if chave == "":
        print("Pesquisa vazia.")
        pausar()
        return

    achou = False
    for t in tarefas:
        if chave in t["descricao"].lower():
            venc = t["vencimento"] if t["vencimento"] else "-"
            print(f"[{t['id']}] {t['descricao']} | {status_txt(t['concluida'])} | "
                  f"Prioridade: {prioridade_txt(t['prioridade'])} | Venc.: {venc}")
            achou = True

    if not achou:
        print("Nenhuma tarefa encontrada.")

    pausar()


# Recursão:
# Ordenação recursiva, lista por prioridade e descrição.
def ordenar_recursivo(tarefas):
    """Retorna lista de tarefas ordenada por prioridade e descrição."""
    if len(tarefas) <= 1:
        return tarefas[:]

    meio = len(tarefas) // 2
    esquerda = ordenar_recursivo(tarefas[:meio])
    direita = ordenar_recursivo(tarefas[meio:])

    return _merge(esquerda, direita)


def _chave_ord(t):
    return (-t["prioridade"], t["descricao"].lower())


def _merge(a, b):
    resultado = []
    i = j = 0
    while i < len(a) and j < len(b):
        if _chave_ord(a[i]) <= _chave_ord(b[j]):
            resultado.append(a[i])
            i += 1
        else:
            resultado.append(b[j])
            j += 1
    resultado.extend(a[i:])
    resultado.extend(b[j:])
    return resultado


def listar_ordenado(tarefas):
    """Lista tarefas ordenadas."""
    print("\n=== Lista ordenada (prioridade) ===")
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        pausar()
        return

    ordenadas = ordenar_recursivo(tarefas)
    for t in ordenadas:
        venc = t["vencimento"] if t["vencimento"] else "-"
        print(f"[{t['id']}] {t['descricao']} | {status_txt(t['concluida'])} | "
              f"Prioridade: {prioridade_txt(t['prioridade'])} | Venc.: {venc}")

    pausar()


def mostrar_menu():
    print("\n==============================")
    print("      GERENCIADOR DE TAREFAS")
    print("==============================")
    print("1) Adicionar tarefa")
    print("2) Ver lista de tarefas")
    print("3) Concluir tarefa")
    print("4) Remover tarefa")
    print("5) Pesquisar tarefa")
    print("6) Ver lista ordenada (prioridade)")
    print("0) Sair")


def main():
    tarefas = []

    while True:
        limpar_tela()
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_tarefa(tarefas)
        elif opcao == "2":
            listar_tarefas(tarefas)
        elif opcao == "3":
            marcar_concluida(tarefas)
        elif opcao == "4":
            remover_tarefa(tarefas)
        elif opcao == "5":
            pesquisar_tarefas(tarefas)
        elif opcao == "6":
            listar_ordenado(tarefas)
        elif opcao == "0":
            print("Encerrando o programa... até mais!")
            break
        else:
            print("Opção inválida. Digite um número de 0 a 6.")
            pausar()


if __name__ == "__main__":
    main()
