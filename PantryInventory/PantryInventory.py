import ViewPresenter as vp
import ui
import shelve

class ItemError(Exception):
    pass

class Item(object):
    def __init__(self, name:string, amount:float, units:string):
        self.name = name
        self.amount = amount
        self.units = units
        return

    def __eq__(self, other):
        return self.name == other.name

    def merge(self, other:Item):
        if not self == other:
            raise ItemError('Can\'t merge unlike items')
        new_amount = self.amount + other.amount
        return Item(self.name, self.amount, self.units)

    def __str__(self):
        return '{}: {} {}'.format(self.name, self.amount, self.units)

class ItemRepository(object):
    def __init__(self, shelf_name):
        self.name = shelf_name
        self.items = self.load()
        self.key = 'item_list'
        self.has_changed = True
        return

    def open_shelf(self):
        if self.closed:
            self.closed = False
            return shelve.open(self.name)
        else:
            return self.shelf

    def load(self):
        self.shelf = self.open_shelf()
        return self.shelf.get(self.key, [])

    def save(self):
        self.shelf = self.open_shelf()
        self.shelf[self.key] = self.items
        self.has_changed = False
        return

    def delete_item(self, index):
        try:
            for indx in index:
                del self.items[indx]
        except TypeError:
            del self.items[index]
        self.has_changed = True
        return self.count

    def add_item(self, item_name, item_quantity, item_unit):
        item = Item(item_name, item_quantity, item_unit)
        try:
            indx = self.items.index(item)
            self.items[indx].merge(item)
        except ValueError:
            self.items.append(item)
        self.has_changed = True
        return self.count

    def close(self):
        self.shelf.close()
        self.closed = True
        return

    @property
    def count(self):
        return len(self.items)

    def __str__(self):
        item_strings = [str(item) for item in self.items]
        return '\n'.join(item_strings)

class PantryInventory(object):
    def __init__(self):
        self.view_names = ['PantryInventory', 'detail_subview', 'add_item_popup']
        self.vm = vp.MultipleViewModel(self.view_names)
        
        self.items = ItemRepository('pantry')

        main_actions = {'save_button':self.save_button_tapped,
                        'quit_button':self.quit_button_tapped,
                        'add_item_button':self.add_item_tapped,
                        'remove_item_button':self.remove_item_tapped}
        self.vm.bind_actions(main_actions)
        return

    def save_button_tapped(self, sender):
        pass

    def quit_button_tapped(self, sender):
        pass

    def add_item_tapped(self, sender):
        pass

    def remove_item_tapped(self, sender):
        pass
