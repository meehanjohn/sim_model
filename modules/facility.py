from modules.storage_cell import storage_cell
from modules.processing_cell import processing_cell
import pandas as pd

class facility:
    def __init__(self, id, **kwargs):
        self.id = id
        equipment = pd.read_csv('files/equipment.csv')
        equipment = equipment[equipment.facility == id]

        self.rmi = self.initialize(
            'storage',
            'rmi',
            num_drums=int(equipment.rmi_drums),
            facility=id
        )
        self.cfr = self.initialize(
            'process',
            'classifier',
            num_machines=1,
            facility=id
        )
        self.pfi = self.initialize(
            'storage',
            'pfi',
            num_drums=int(equipment.pfi_drums),
            facility=id
        )
        self.pfo = self.initialize(
            'process',
            'pfo',
            num_machines=int(equipment.pfo_tanks),
            facility=id
        )
        self.pis = self.initialize(
            'storage',
            'pi',
            num_drums=int(equipment.pi_drums),
            facility=id
        )
        self.pck = self.initialize(
            'process',
            'packaging',
            boxing_machines=int(equipment.bagging_machines),
            bagging_machines=int(equipment.boxing_machines),
            facility=id
        )

    def initialize(self, category, type, **kwargs):
        print("Initializing {0} Cell".format(type))

        if category == 'storage':
            return(storage_cell(type, **kwargs))

        else:
            return(processing_cell(type, **kwargs))
