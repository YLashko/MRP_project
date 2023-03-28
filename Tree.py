from GHP import GHP
from MRP import MRP
import csv
from html_layout import layout


class MRPTree:
    def __init__(self):
        self.ghp: GHP = None

    def get_item(self, item: list[int]) -> MRP:
        root = self.ghp
        n = 0
        while len(item) > 0:
            try:
                n = item.pop(0)
                root = root.get_children()[n]
            except IndexError as e:
                print(f"Can't get child {n} of {root.name}: {e}")
        return root

    def calculate_all(self):
        self.calculate_recursive(self.ghp)

    def calculate_recursive(self, root: GHP | MRP):
        root.setup_tables()
        root.compute_timestamps()
        root.setup_children()
        for child in root.get_children():
            self.calculate_recursive(child)

    def get_tree(self):
        return list(self.get_tree_recursive(self.ghp, []))

    def get_tree_recursive(self, root, tree_list):
        tree_list += [root]
        for child in root.get_children():
            self.get_tree_recursive(child, tree_list)
        return tree_list

    def set_ghp(self, ghp: GHP):
        self.ghp = ghp

    def add_mrp(self, tree_coords: list[int], mrp: MRP, prod_multiplier: int):
        self.get_item(tree_coords).add_child_MRP(mrp, prod_multiplier)


class Convert:
    @staticmethod
    def ghp_to_rows(ghp):
        return [
            [ghp.name] + ["" for n in range(ghp.timestamps)],
            ["Okres"] + [str(n + 1) for n in range(ghp.timestamps)],
            ["Przewidywany popyt"] + ghp.demand_table,
            ["Produkcja"] + ghp.production_table,
            ["Dostępne"] + ghp.in_stock_table
        ]

    @staticmethod
    def mrp_to_rows(mrp):
        return [
            [mrp.name] + ["" for n in range(mrp.timestamps)],
            ["Okres"] + [str(n + 1) for n in range(mrp.timestamps)],
            ["Całkowite zapotrzebowanie"] + mrp.demand_table,
            ["Planowane przyjęcia"] + mrp.intake_table,
            ["Przewidywane na stanie"] + mrp.in_stock_table,
            ["Zapotrzebowanie netto"] + [abs(el) for el in mrp.net_demand_table],
            ["Planowane zamówienia"] + mrp.planned_orders_table,
            ["Planowane przyjęcie zamówień"] + mrp.orders_intake_table
        ]


class Save:
    @staticmethod
    def to_csv(tree: MRPTree, filename):
        csv_list = []
        for element in tree.get_tree():
            if isinstance(element, GHP):
                csv_list += Convert.ghp_to_rows(element)
            elif isinstance(element, MRP):
                csv_list += Convert.mrp_to_rows(element)
        with open(filename, "w", encoding="utf-8", newline='') as f:
            csv.writer(f).writerows(csv_list)

    @staticmethod
    def to_html_table(tree: MRPTree, filename):
        table = "<table>"
        element_rows = []
        for element in tree.get_tree():
            if isinstance(element, GHP):
                element_rows = Convert.ghp_to_rows(element)
            elif isinstance(element, MRP):
                element_rows = Convert.mrp_to_rows(element)
            for row in element_rows:
                table += "<tr>"
                for cell in row:
                    table += f"<td>{cell}</td>"
                table += "</tr>"
        table += "</table>"
        with open(filename, "w", encoding='utf-8') as file:
            file.write(layout(table))
