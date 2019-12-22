class storage_drum:
    def __init__(self, type, id, capacity, **kwargs):
        self.id = id
        self.type = type
        self.capacity = capacity
        self.contents = kwargs.get('contents')
        self.jb_color = kwargs.get('jb_color')
        self.jb_size = kwargs.get('jb_size')
        self.jb_flavor = kwargs.get('jb_flavor')

        if self.contents is None or self.contents == 0:
            self.is_empty = True
        else:
            self.is_empty = False

    def __repr__(self):
        return(str(self.id))
