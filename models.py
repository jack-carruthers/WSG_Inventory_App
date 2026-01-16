class InventoryItem:
    def __init__(self, item_id, name, quantity, batch, location, status):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.batch = batch
        self.location = location
        self.status = status

    def __str__(self):
        return f"{self.name} ({self.quantity}) - {self.status}"
