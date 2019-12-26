from modules.storage_drum import storage_drum
import pandas as pd

class storage_cell:
    def __init__(self, type, **kwargs):
        self.type = type
        self.num_drums = kwargs.get('num_drums')
        self.facility = kwargs.get('facility')
        self.init_drums()

    def __repr__(self):
        return("{0} Storage Cell".format(self.type))

    def init_drums(self):
        if self.type == 'rmi':
            filename = 'files/rmi_inventory_level.csv'

        elif self.type == 'pfi':
            filename = 'files/pfi_drum.csv'

        elif self.type == 'pi':
            filename = 'files/pi_drum.csv'

        drum_df = pd.read_csv(filename, thousands=',')
        drum_df = drum_df[drum_df.facility == self.facility]
        drum_kwargs_list = drum_df.to_dict('records')
        drums = [
            storage_drum(type, **drum_kwargs)
            for drum_kwargs in drum_kwargs_list
        ]

        self.drums = drums

    @property
    def empty_drums(self):
        return [drum for drum in self.drums if drum.is_empty == True]

    @property
    def full_drums(self):
        return [drum for drum in self.drums if drum not in self.empty_drums]

    def order_drums(self):
        pass

    def load_drums(self, queue, time):
        queue_kwargs_list = queue.to_dict('records')

        if len(queue_kwargs_list) <= len(self.empty_drums):
            for queue_kwargs in queue_kwargs_list:
                drum = self.empty_drums[0]
                drum.load(time=time, **queue_kwargs)
        else:
            print('Not enough drums')

    def unload_drums(self):
        for drum in self.full_drums:
            yield drum.unload()
