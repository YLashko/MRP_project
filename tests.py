from GHP import GHP
from MRP import MRP


def test_zad1():
    stol = GHP(
        name="Stół",
        prod_time=1,
        in_stock=2
    )
    blaty = MRP(
        name="Blaty",
        prod_time=3,
        level=1,
        batch_size=40,
        in_stock=22
    )
    plyta = MRP(
        name="Plyta",
        prod_time=1,
        level=2,
        batch_size=50,
        in_stock=10
    )
    nogi = MRP(
        name="Nogi",
        prod_time=2,
        level=1,
        batch_size=120,
        in_stock=40
    )
    stol.set_demand_table([0, 0, 0, 0, 20, 0, 40, 0, 10, 0])
    stol.setup_tables()
    stol.set_production_table([0, 0, 0, 0, 28, 0, 30, 0, 0, 0])
    stol.compute_in_stock()
    stol.add_child_MRP(blaty, 1)
    stol.add_child_MRP(nogi, 4)
    blaty.add_child_MRP(plyta, 1)
    stol.setup_children()
    blaty.compute_timestamps()
    nogi.compute_timestamps()
    blaty.setup_children()
    plyta.compute_timestamps()
    print_mrp(blaty)
    print_mrp(nogi)
    print_mrp(plyta)


def print_mrp(mrp):
    print(mrp.name)
    print(mrp.demand_table)
    print(mrp.in_stock_table)
    print(mrp.net_demand_table)
    print(mrp.planned_orders_table)
    print(mrp.orders_intake_table)


test_zad1()
