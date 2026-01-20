import json  #Convierte texto Json a objetos Python
import re  #Regula expresiones-Se usa para buscar patrones en strings
import sys  #Lee argumentos y salida del programa con codigo


def read_json_file(path): #Esta funcion cumple el manejo robusto de errores
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"No existe el archivo: {path}")
        sys.exit(2)
    except PermissionError:
        print(f"Sin permisos para leer: {path}")
        sys.exit(2)

    try:
        data = json.loads(text) #convierte el string a estructuras Python
    except json.JSONDecodeError as e: #Si el Json está mal formado cae aqui
        print(f"JSON inválido. Línea {e.lineno}, columna {e.colno}: {e.msg}")
        sys.exit(3)

    if not isinstance(data, list): #Asegura que data sea lista
        print("El JSON debe ser una LISTA de objetos.")
        sys.exit(3)

    return data


def is_valid_record(item): #Verifica si un registro tiene la estructura mínima
    match item:
        case {
            "name": str(),
            "email": str(),
            "role": str(),
            "active": bool(),
            "amount": _,
        }:
            return True
        case _:
            return False


#Toma la liosta de registros y aplica filtros opcionales
def filter_records(records, active_only, role, email_domain, name_regex):
    filtered = []

    # Compilamos regex si se pide
    name_re = re.compile(name_regex, re.IGNORECASE) if name_regex else None
    domain_re = (
        re.compile(r"@" + re.escape(email_domain) + r"$", re.IGNORECASE)
        if email_domain
        else None
    )

    for item in records:
        if not is_valid_record(item):
            # ignoramos registros que no cumplan estructura
            continue

        if active_only and item["active"] is False:
            continue

        if role and item["role"].lower() != role.lower():
            continue

        if domain_re and not domain_re.search(item["email"]):
            continue

        if name_re and not name_re.search(item["name"]):
            continue

        filtered.append(item) #Si pasó todos los filtros se guarda

    return filtered


def aggregate(records): #Agrega datos: conteos y sumas
    total = len(records)
    active = 0
    amount_sum = 0.0
    by_role = {}  # dict para agrupar

    for item in records:
        if item["active"]:
            active += 1

        # convertimos amount a float por si viene como int o string numérico
        try:
            amount = float(item["amount"])
        except (ValueError, TypeError):
            amount = 0.0  # si viene mal, lo tomamos como 0

        amount_sum += amount

        role = item["role"].lower()
        if role not in by_role:
            by_role[role] = {"count": 0, "amount_sum": 0.0}

        by_role[role]["count"] += 1
        by_role[role]["amount_sum"] += amount

    inactive = total - active

    return {
        "total": total,
        "active": active,
        "inactive": inactive,
        "amount_sum": round(amount_sum, 2),
        "by_role": by_role,
    }


def print_report(summary):
    print("=== Reporte ===")
    print("Total:", summary["total"])
    print("Activos:", summary["active"])
    print("Inactivos:", summary["inactive"])
    print("Suma amount:", summary["amount_sum"])
    print("\nPor rol:")
    for role, info in summary["by_role"].items():
        print(
            f"  - {role}: {info['count']} (amount_sum={round(info['amount_sum'], 2)})"
        )


def main():
    # Uso: python main.py data.json [opciones simples]
    # Para no complicarlo con argparse, usamos argumentos simples.
    # Ej:
    #   python main.py data.json
    #   python main.py data.json active
    #   python main.py data.json role=admin
    #   python main.py data.json domain=gmail.com
    #   python main.py data.json name=^A

    if len(sys.argv) < 2:
        print(
            "Uso: python main.py <archivo.json> [active] [role=...] "
            "[domain=...] [name=...]"
        )
        sys.exit(1)

    path = sys.argv[1]
    args = sys.argv[2:]

    active_only = "active" in args

    role = None
    email_domain = None
    name_regex = None

    for a in args:
        if a.startswith("role="):
            role = a.split("=", 1)[1]
        elif a.startswith("domain="):
            email_domain = a.split("=", 1)[1]
        elif a.startswith("name="):
            name_regex = a.split("=", 1)[1]

    records = read_json_file(path)  #Lee
    filtered = filter_records(records, active_only, role, email_domain, name_regex)  #Filtra
    summary = aggregate(filtered)  #Agrega
    print_report(summary)  #Muestra


if __name__ == "__main__":
    main()
