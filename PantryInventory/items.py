from PantryInventory import unit_registry, q_

class ConversionFactory(object):
    @staticmethod
    def convert(old_quantity, new_unit):
        return unit_registry.convert(old_quantity, old_quantity.units, new_unit)

class PantryItem(object):
    def __init__(self):
        self._stock = 0 * unit_registry('cc')
        return
    
    def add_quantity(self, amount):
        pass

    @property
    def stock(self):
        return self._stock

class VolumePantryItem(PantryItem):
    def __init__(self, name, **kwargs):
        self.units = unit_registry('

