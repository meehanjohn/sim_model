class storage_drum:
    def __init__(self, type, id, capacity, **kwargs):
        self.id = id
        self.type = type
        self.capacity = capacity
        self.contents = (kwargs.get('contents') or 0)
        self.jb_color = kwargs.get('jb_color')
        self.jb_size = kwargs.get('jb_size')
        self.jb_flavor = kwargs.get('jb_flavor')

        '''
        if type in ['pfi', 'pi']:
            self.load_times = []
            self.unload_times = []
        else:
            self.load_time = kwargs.get('time')
            self.unload_time = kwargs.get('time')
        '''
        
    def __repr__(self):
        return(str(self.id))

    @property
    def is_empty(self):
        if self.contents is None or self.contents == 0:
            return True
        else:
            return False

    def load(self, **kwargs):
        amount = kwargs.get('amount')
        if amount <= self.capacity:
            '''
            time = kwargs.get('time')
            if type in ['pfi', 'pi']:
                self.load_times.append(time)
            else:
                self.load_time = time
            '''
            self.contents = amount
            self.jb_color = kwargs.get('jb_color')
            self.jb_size = kwargs.get('jb_size')
            self.jb_flavor = kwargs.get('jb_flavor')
            return(self.id)
        else:
            raise ValueError('Amount exceeds capacity')

    def unload(self, **kwargs):
        time = kwargs.get('time')
        '''
        if type in ['pfi', 'pi']:
            self.unload_times.append(time)
        else:
            self.unload_time = time
        '''
        contents = self.contents
        self.contents = 0
        return(
            self.id,
            {
            'amount':contents,
            'jb_color':self.jb_color,
            'jb_size':self.jb_size,
            'jb_flavor':self.jb_flavor
            }
        )
