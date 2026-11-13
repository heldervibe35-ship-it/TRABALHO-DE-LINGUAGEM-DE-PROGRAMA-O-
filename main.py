
"""
Questão 5 - Sistema de Registo de Nascimentos e Identificação de Recém-Nascidos
Unidade hospitalar - nascimentos do mês de OUTUBRO

Funcionalidades:
 1. Registar nascimento (dados da mãe e do recém-nascido, médico responsável)
 2. Número sequencial automático para cada nascimento (RN-0001, RN-0002, ...)
 3. Identificador próprio para cada mãe (MAE-001, MAE-002, ...)
 4. Mãe consulta o registo do(s) seu(s) filho(s) com o seu identificador
 5. Profissional de saúde autorizado consulta todos os dados (com código de acesso)
 6. Relatório: total de nascimentos, distribuição por género e médico responsável
"""

import json
import os
from datetime import datetime

FICHEIRO = "nascimentos_outubro.json"
CODIGO_PROFISSIONAL = "saude2026"   # código de acesso dos profissionais (exemplo)
MES_PERMITIDO = 10


# -------------------------------------------------------
# Persistência
# -------------------------------------------------------
def carregar_dados():
    if os.path.exists(FICHEIRO):
        with open(FICHEIRO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"maes": {}, "nascimentos": []}


def guardar_dados(dados):
    with open(FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


# ---------------------------------------------------------
# Funções auxiliares de entrada
# ---------------------------------------------------------
def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("  ! Este campo não pode ficar vazio.")


def ler_inteiro(mensagem, minimo, maximo):
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo <= valor <= maximo:
                return valor
            print(f"  ! Introduza um valor entre {minimo} e {maximo}.")
        except ValueError:
            print("  ! Valor inválido. Introduza um número inteiro.")


def ler_decimal(mensagem, minimo, maximo):
    while True:
        try:
            valor = float(input(mensagem).strip().replace(",", "."))
            if minimo <= valor <= maximo:
                return valor
            print(f"  ! Introduza um valor entre {minimo} e {maximo}.")
        except ValueError:
            print("  ! Valor inválido. Introduza um número.")


def ler_genero():
    while True:
        g = input("Género do bebé (M - Masculino / F - Feminino): ").strip().upper()
        if g in ("M", "F"):
            return "Masculino" if g == "M" else "Feminino"
        print("  ! Introduza apenas M ou F.")


def ler_data_outubro():
    """Pede a data de nascimento (dd/mm/aaaa) e garante que é em outubro."""
    while True:
        texto = input("Data de nascimento (dd/mm/aaaa, mês de outubro): ").strip()
        try:
            data = datetime.strptime(texto, "%d/%m/%Y")
        except ValueError:
            print("  ! Data inválida. Use o formato dd/mm/aaaa.")
            continue
        if data.month != MES_PERMITIDO:
            print("  ! Este sistema só regista nascimentos ocorridos em outubro.")
            continue
        if data > datetime.now():
            print("  ! A data não pode estar no futuro.")
            continue
        return data.strftime("%d/%m/%Y")


# ------------------------------------------------------
# Geração de identificadores
# -----------------------------------------------------
def proximo_numero_nascimento(dados):
    return f"RN-{len(dados['nascimentos']) + 1:04d}"


def obter_ou_criar_mae(dados):
    """Procura a mãe pelo nº do BI; se não existir, cria-a com novo identificador."""
    bi = ler_texto("Nº do Bilhete de Identidade da mãe: ").upper()

    for id_mae, mae in dados["maes"].items():
        if mae["bi"] == bi:
            print(f"  Mãe já registada: {mae['nome']} (Identificador: {id_mae})")
            return id_mae

    nome = ler_texto("Nome completo da mãe: ")
    idade = ler_inteiro("Idade da mãe: ", 10, 60)
    telefone = ler_texto("Telefone da mãe: ")
    id_mae = f"MAE-{len(dados['maes']) + 1:03d}"
    dados["maes"][id_mae] = {
        "nome": nome,
        "bi": bi,
        "idade": idade,
        "telefone": telefone,
    }
    print(f"  Nova mãe registada. Identificador: {id_mae}")
    return id_mae


# ---------------------------------------------------
# Operações principais
# --------------------------------------------------
def registar_nascimento(dados):
    print("\n=== REGISTO DE NASCIMENTO ===")
    id_mae = obter_ou_criar_mae(dados)

    nome_bebe = input("Nome do recém-nascido (Enter se ainda não tiver): ").strip()
    if not nome_bebe:
        nome_bebe = "Sem nome atribuído"
    genero = ler_genero()
    data = ler_data_outubro()
    peso = ler_decimal("Peso ao nascer (kg): ", 0.3, 7.0)
    tipo_parto = ""
    while tipo_parto not in ("normal", "cesariana"):
        tipo_parto = input("Tipo de parto (normal / cesariana): ").strip().lower()
    medico = ler_texto("Nome do médico responsável pelo parto: ")

    registo = {
        "numero": proximo_numero_nascimento(dados),
        "id_mae": id_mae,
        "nome_bebe": nome_bebe,
        "genero": genero,
        "data_nascimento": data,
        "peso_kg": peso,
        "tipo_parto": tipo_parto,
        "medico": medico,
        "registado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    dados["nascimentos"].append(registo)
    guardar_dados(dados)

    print("\n  Nascimento registado com sucesso!")
    print(f"  Número do recém-nascido : {registo['numero']}")
    print(f"  Identificador da mãe    : {id_mae} (guarde para consultas futuras)")


def mostrar_nascimento(dados, n):
    mae = dados["maes"][n["id_mae"]]
    print("-" * 50)
    print(f"Nº do recém-nascido : {n['numero']}")
    print(f"Nome                : {n['nome_bebe']}")
    print(f"Género              : {n['genero']}")
    print(f"Data de nascimento  : {n['data_nascimento']}")
    print(f"Peso ao nascer      : {n['peso_kg']:.2f} kg")
    print(f"Tipo de parto       : {n['tipo_parto']}")
    print(f"Médico responsável  : Dr(a). {n['medico']}")
    print(f"Mãe                 : {mae['nome']} ({n['id_mae']})")


def consulta_mae(dados):
    print("\n=== CONSULTA DA MÃE ===")
    id_mae = ler_texto("Identificador da mãe (ex.: MAE-001): ").upper()

    if id_mae not in dados["maes"]:
        print("  ! Identificador não encontrado.")
        return

    bi = ler_texto("Confirme o nº do Bilhete de Identidade: ").upper()
    if bi != dados["maes"][id_mae]["bi"]:
        print("  ! Dados de confirmação incorretos. Acesso negado.")
        return

    filhos = [n for n in dados["nascimentos"] if n["id_mae"] == id_mae]
    print(f"\nOlá, {dados['maes'][id_mae]['nome']}.")
    if not filhos:
        print("Não existem registos de recém-nascidos associados ao seu identificador.")
        return
    for n in filhos:
        mostrar_nascimento(dados, n)
    print("-" * 50)


def acesso_profissional():
    codigo = input("Código de acesso do profissional de saúde: ").strip()
    if codigo != CODIGO_PROFISSIONAL:
        print("  ! Código inválido. Acesso negado.")
        return False
    return True


def mostrar_completo(dados, n):
    mostrar_nascimento(dados, n)
    mae = dados["maes"][n["id_mae"]]
    print(f"Dados da mãe        : BI {mae['bi']} | {mae['idade']} anos | Tel. {mae['telefone']}")


def consulta_profissional(dados):
    print("\n=== CONSULTA - PROFISSIONAL DE SAÚDE ===")
    if not acesso_profissional():
        return
    if not dados["nascimentos"]:
        print("Ainda não há nascimentos registados.")
        return

    print("1 - Listar todos os nascimentos")
    print("2 - Procurar por número do recém-nascido")
    opcao = ler_inteiro("Opção: ", 1, 2)

    if opcao == 1:
        for n in dados["nascimentos"]:
            mostrar_completo(dados, n)
        print("-" * 50)
    else:
        numero = ler_texto("Número do recém-nascido (ex.: RN-0001): ").upper()
        for n in dados["nascimentos"]:
            if n["numero"] == numero:
                mostrar_completo(dados, n)
                print("-" * 50)
                return
        print("  ! Número não encontrado.")


def relatorio(dados):
    print("\n=== RELATÓRIO DE NASCIMENTOS - OUTUBRO ===")
    if not acesso_profissional():
        return

    nascimentos = dados["nascimentos"]
    total = len(nascimentos)
    masculino = sum(1 for n in nascimentos if n["genero"] == "Masculino")
    feminino = total - masculino

    print(f"\nTotal de nascimentos em outubro: {total}")
    pm = f" ({masculino / total * 100:.1f}%)" if total else ""
    pf = f" ({feminino / total * 100:.1f}%)" if total else ""
    print(f"  Masculino: {masculino}{pm}")
    print(f"  Feminino : {feminino}{pf}")

    print("\nNascimentos por médico responsável:")
    por_medico = {}
    for n in nascimentos:
        por_medico.setdefault(n["medico"], []).append(n)
    if not por_medico:
        print("  (sem registos)")
    for medico, lista in sorted(por_medico.items()):
        numeros = ", ".join(n["numero"] for n in lista)
        print(f"  Dr(a). {medico}: {len(lista)} nascimento(s) -> {numeros}")


# ---------------------------------------------------------
# Menu principal
# --------------------------------------------------------
def main():
    dados = carregar_dados()
    while True:
        print("\n" + "=" * 50)
        print(" REGISTO DE NASCIMENTOS - MÊS DE OUTUBRO")
        print("=" * 50)
        print("1 - Registar novo nascimento")
        print("2 - Consultar registo do meu filho (mãe)")
        print("3 - Consultar registos (profissional de saúde)")
        print("4 - Relatório: total e distribuição por género/médico")
        print("0 - Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            registar_nascimento(dados)
        elif opcao == "2":
            consulta_mae(dados)
        elif opcao == "3":
            consulta_profissional(dados)
        elif opcao == "4":
            relatorio(dados)
        elif opcao == "0":
            print("Programa terminado. Obrigado!")
            break
        else:
            print("  ! Opção inválida.")


if __name__ == "__main__":
    main()


