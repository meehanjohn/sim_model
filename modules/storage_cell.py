from modules.storage_drum import storage_drum
import pandas as pd

class storage_cell:
    def __init__(self, type, **kwargs):
        self.type = type
        self.num_drums = kwargs.get('num_drums')
        self.init_drums(**kwargs)

    def __repr__(self):
        return("{0} Storage Cell".format(self.type))

    def init_drums(self, **kwargs):
        if self.type == 'rmi':
            filename = 'files/rmi_inventory_level.csv'

        elif self.type == 'pfi':
            filename = 'files/pfi_rate.csv'

        elif self.type == 'pi':
            filename = 'files/pi_drum.csv'

        drum_df = pd.read_csv(filename)
        self.drums = [
            storage_drum(type, id, **kwargs) for id in drum_list
        ]
        self.empty_drums = self.drums

    def order_drums(self):
        pass

    def fill_drums(self):
        for d in drums:
            if d.is_empty:
                pass

    def empty_drums(self):
        pass
