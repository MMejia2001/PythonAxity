from lab_solid.repos import FakeSqlOrderRepo, InMemoryOrderRepo
from lab_solid.service import OrderService


def run_demo(repo, name: str) -> None:
    svc = OrderService(repo)
    svc.create_order(1, "Marco", 123.456)
    print(name, "=>", svc.get_order(1))


def main() -> None:
    run_demo(InMemoryOrderRepo(), "MEM")
    run_demo(FakeSqlOrderRepo(), "SQL")


if __name__ == "__main__":
    main()
