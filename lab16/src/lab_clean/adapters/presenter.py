from lab_clean.domain.entities import Order


class OrderPresenter:
    def to_dict(self, order: Order) -> dict:
        return {
            "order_id": order.order_id,
            "customer": order.customer,
            "subtotal": order.subtotal,
            "tax": order.tax,
            "total": order.total,
            "items": [
                {
                    "sku": i.sku,
                    "unit_price": i.unit_price,
                    "qty": i.qty,
                    "line_total": i.line_total,
                }
                for i in order.items
            ],
        }
