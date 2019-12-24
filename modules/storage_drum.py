class storage_drum:
    def __init__(self, type, id, capacity, **kwargs):
        self.id = id
        self.type = type
        self.capacity = capacity
        self.contents = (kwargs.get('contents') or 0)
        self.jb_color = kwargs.get('jb_color')
        self.jb_size = kwargs.get('jb_size')
        self.jb_flavor = kwargs.get('jb_flavor')

        if type in ['pfi', 'pi']:
            self.fill_times = []
            self.empty_times = []
        else:
            self.fill_time = kwargs.get('time')
            self.empty_time = kwargs.get('time')

    def __repr__(self):
        return(str(self.id))

    @property
    def is_empty(self):
        if self.contents is None or self.contents == 0:
            return True
        else:
            return False

    def fill(self, amount, **kwargs):
        if amount <= self.capacity:
            time = kwargs.get('time')
            if type in ['pfi', 'pi']:
                self.fill_times.append(time)
            else:
                self.fill_time = time
            self.contents = amount
            self.jb_color = kwargs.get('jb_color')
            self.jb_size = kwargs.get('jb_size')
            self.jb_flavor = kwargs.get('jb_flavor')
        else:
            raise ValueError('Amount exceeds capacity')

    def empty(self, **kwargs):
        time = kwargs.get('time')
        if type in ['pfi', 'pi']:
            self.empty_times.append(time)
        else:
            self.empty_time = time
        contents = self.contents
        self.contents = 0
        return(
            contents,
            self.jb_color,
            self.jb_size,
            self.jb_flavor
        )
