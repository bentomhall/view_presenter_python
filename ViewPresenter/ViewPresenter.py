import ui

class BaseViewModel(object):
    ''' 
    Base class for presenting and managing ui.Views.
    Methods:
        bind_actions(self, actions): associates callback functions with ui elements. Actions should be a dictionary of {<element_name>:<callback_function>}
        present(self, view_name, style=None): presents the named view with the style named. If style is None, use the default presentation style (fullscreen).
        close_view(self, view_name): Closes the named view.
        set_element_contents(self, element_name, text): Sets the selected element's text or title attribute (whichever it has) to the supplied text.
        get_element_contents(self, element_name): returns the text (or title) associated with the supplied element information.
        set_element_identifiers(self): called from derived class constructor AFTER loading views with ui.load_view(). Returns a mapping of unique element names to tuple (view_name, element_name).
        on_close(self): closes all views (generally called by a quit button\'s callback function)
    Attributes:
        views: dictionary of {<view_name>:<ui.View>} controlled by this ViewModel. All access to ui is through this mapping. Must be set in derived class constructor!
        _elements: internal dictionary of {<unique_element_name>: <ui.View>} to look-up the view containing the element
    '''

    def __init__(self):
        self.views = {}
        self._elements = {}
        return

    def bind_actions(self, actions):
        '''
        Binds ui element actions (button presses, etc) to methods. No return value. Should not be overriden.
        Parameters:
           dictionary actions: {<unique_element_name>:<callback_function>}  
        '''
        for element_name, callback in actions.items():
            view = self._elements[element_name]
            view[element_id].action = callback
        return

    def present(self, view_name, style=None):
        '''Presents a view identified by name with given style. Should not be overriden.'''
        try:
            self.views[view_name].present(style)
        except TypeError:
            self.views[view_name].present()
        return

    def close_view(self, view_name):
        '''Closes the named view. Should not be overriden.'''
        self.views[view_name].close()
        return

    def set_element_contents(self, element_name, value, override=False):
        view= self._elements[element_name]
        e = view[element]
        if isinstance(e, ui.TableView):
            if override:
                e.data_source.items = value
            else:
                e.data_source.items.extend(value)
        elif isinstance(e, ui.ImageView):
            e.image = value
        elif isinstance(e, ui.Slider):
            e.value = value
        else:
            try:
                e.text = value
            except TypeError:
                e.title = value
        return

    def on_close(self):
        for name in self.views.keys():
            self.close_view(name)
        return

    def get_element_contents(self, element_name):
        view = self._elements[element_name]
        e = view[element]
        if isinstance(e, ui.TableView):
            value = e.data_source.items
        elif isinstance(e, ui.ImageView):
            value = e.image
        elif isinstance(e, ui.Slider):
            value = e.value
        else:
            try:
                value = e.text
            except TypeError:
                value = e.title
        return value

    def set_element_identifiers(self):
        elements = {}
        for key, value in self.views:
            for subview in value.subviews:
                name = subview.name
                if name in elements:
                    raise ValueError('UI element names must be unique: duplicate identifier {} found'.format(name))
                elements[name] = self.views[value]
        return

class SingleViewModel(BaseViewModel):
    """Specialization of BaseViewModel for the case of a single view"""
    def __init__(self, view_name):
        self.views = {view_name:ui.load_view(view_name)}
        self._elements = self.set_element_identifiers()
        return

class MultipleViewModel(BaseViewModel):
    """Specialization of BaseViewModel for the case of multiple views"""
    def __init__(self, view_names):
        self.views = {name:ui.load_view(name) for name in view_names}
        self._elements = self.set_element_identifiers()
        return