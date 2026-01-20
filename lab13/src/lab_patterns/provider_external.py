class ExternalShippingApi:
    """
    Simula un proveedor externo.
    Imagina que este SDK lo hicieron otros y no lo controlas.
    """

    def quote(self, zip_code: str, weight_kg: float) -> dict:
        # Simulación: el proveedor responde con un dict raro
        return {"zip": zip_code, "cost_mxn": round(50 + weight_kg * 10, 2)}
