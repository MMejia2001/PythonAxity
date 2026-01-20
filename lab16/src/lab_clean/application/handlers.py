from lab_clean.domain.events import OrderCreated


class PrintOrderCreatedHandler:
    def handle(self, event: OrderCreated) -> None:
        # En real: mandar email, HTTP, message queue, etc.
        print(f"[EVENT] OrderCreated id={event.order_id} total={event.total}")
