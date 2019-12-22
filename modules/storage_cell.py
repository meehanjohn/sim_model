from modules.storage_drum import storage_drum
import pandas as pd

class storage_cell:
    def __init__(self, type, **kwargs):
        self.type = type
        self.num_drums = kwargs.get('num_drums')
        self.facility = kwargs.get('facility')
        self.init_drums(**kwargs)

    def __repr__(self):
        return("{0} Storage Cell".format(self.type))

    def init_drums(self, **kwargs):
        if self.type == 'rmi':
            filename = 'files/rmi_inventory_level.csv'

        elif self.type == 'pfi':
            filename = 'files/pfi_drum.csv'

        elif self.type == 'pi':
            filename = 'files/pi_drum.csv'

        drum_df = pd.read_csv(filename, thousands=',')
        drum_df = drum_df[drum_df['Site'] == self.facility]

        if 'Start Amount' not in drum_df.columns:
            drum_df['Start Amount'] = None
        if 'Color' not in drum_df.columns:
            drum_df['Color'] = None

        drums = [
            storage_drum(
                type,
                id=row['Drum Number'],
                capacity=row['Capacity'],
                contents=row['Start Amount'],
                jb_color=row['Color']
            )
            for index, row in drum_df.iterrows()
        ]

        self.drums = drums
        self.empty_drums = [drum for drum in drums if drum.is_empty == True]
        self.full_drums = [drum for drum in drums if drum not in self.empty_drums]

    def order_drums(self):
        pass

    def fill_drums(self, queue):
        if len(queue) > len(self.empty_drums):
            print('Not enough drums')
        else:
            for index, row in queue.iterrows():
                drum = self.empty_drums.pop()
                drum.contents = row.Queue
                drum.jb_color = row.Color
                if 'Size' in queue.columns:
                    drum.jb_size = row.Size
                if 'Flavor' in queue.columns:
                    drum.flavor = row.Flavor
                drum.is_empty = False
                self.full_drums.append(drum)


    def empty_drums(self):
        pass
