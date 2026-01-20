import csv
import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def setup_logger(level: str) -> logging.Logger:
    """
    Configura logging con distintos niveles.
    level: "DEBUG", "INFO", "WARNING", "ERROR"
    """
    logger = logging.getLogger("lab-io")
    logger.setLevel(level.upper())

    # Evita duplicar handlers si lo corres varias veces
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def parse_amount(value: str) -> float | None:
    """Convierte string a float, si falla regresa None."""
    try:
        return float(value)
    except ValueError:
        return None


def ingest_csv(csv_path: Path, logger: logging.Logger) -> dict:
    """
    Lee el CSV y devuelve métricas.
    Maneja filas inválidas con WARNING.
    """
    if not csv_path.exists():
        logger.error("El archivo no existe: %s", csv_path)
        raise FileNotFoundError(csv_path)

    total_rows = 0
    valid_rows = 0
    invalid_rows = 0

    total_amount = 0.0
    category_totals: dict[str, float] = defaultdict(float)
    category_counts: dict[str, int] = defaultdict(int)

    logger.info("Leyendo CSV: %s", csv_path)

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        required_cols = {"date", "category", "amount"}
        if reader.fieldnames is None or not required_cols.issubset(
            set(reader.fieldnames)
        ):
            logger.error(
                "Columnas requeridas: %s. Encontradas: %s",
                required_cols,
                reader.fieldnames,
            )
            raise ValueError("CSV no tiene columnas requeridas")

        for row in reader:
            total_rows += 1

            date_str = (row.get("date") or "").strip()
            category = (row.get("category") or "").strip()
            amount_str = (row.get("amount") or "").strip()

            # Validaciones simples
            if not category:
                invalid_rows += 1
                logger.warning(
                    "Fila %s inválida: category vacía -> %s", total_rows, row
                )
                continue

            amount = parse_amount(amount_str)
            if amount is None:
                invalid_rows += 1
                logger.warning(
                    "Fila %s inválida: amount no numérico -> %s", total_rows, row
                )
                continue

            # Validación de fecha (opcional)
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                invalid_rows += 1
                logger.warning(
                    "Fila %s inválida: date mal formato -> %s", total_rows, row
                )
                continue

            # Si pasa todo:
            valid_rows += 1
            total_amount += amount
            category_totals[category] += amount
            category_counts[category] += 1

    avg_amount = round(total_amount / valid_rows, 2) if valid_rows else 0.0

    # Top 3 categorías por total
    top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[
        :3
    ]

    report = {
        "source_file": str(csv_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rows": {
            "total": total_rows,
            "valid": valid_rows,
            "invalid": invalid_rows,
        },
        "metrics": {
            "total_amount": round(total_amount, 2),
            "avg_amount": avg_amount,
        },
        "by_category": {
            cat: {
                "count": category_counts[cat],
                "total": round(category_totals[cat], 2),
            }
            for cat in sorted(category_totals.keys())
        },
        "top_categories": [
            {"category": c, "total": round(t, 2)} for c, t in top_categories
        ],
    }

    logger.info("Ingesta terminada. Válidas=%s, inválidas=%s", valid_rows, invalid_rows)
    return report


def export_json(report: dict, output_path: Path, logger: logging.Logger) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    logger.info("Reporte JSON exportado a: %s", output_path)


def main() -> None:
    # Rutas con pathlib
    base_dir = Path(__file__).parent
    csv_path = base_dir / "data" / "sales.csv"
    out_path = base_dir / "out" / "report.json"

    logger = setup_logger(level="INFO")

    try:
        report = ingest_csv(csv_path, logger)
        export_json(report, out_path, logger)
    except Exception as e:
        logger.error("Falló el proceso: %s", e)
        raise


if __name__ == "__main__":
    main()
