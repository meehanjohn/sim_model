from modules.machine import machine

class processing_cell:
    def __init__(self, type, **kwargs):
        self.type = type
        self.facility = kwargs.get('facility')

        if type == 'packaging':
            self.num_machines = {
                'boxing_machine':kwargs.get('boxing_machines'),
                'bagging_machine':kwargs.get('bagging_machines')
            }
            self.machines = [
                machine(type=key, i=1, **dict(key=value), **kwargs)
                for key,value in self.num_machines.items()
            ]
        else:
            self.num_machines = kwargs.get('num_machines')
            self.machines = [
                machine(type, i, **kwargs) for i in range(self.num_machines)
            ]

    def __repr__(self):
        return("{0} Processing Cell".format(self.type))

    @property
    def avail_mach(self):
        return [m for m in self.machines if m.available == True]

    @property
    def unavail_mach(self):
        return [m for m in self.machines if m.available == False]

    def load_machines(self, **kwargs):
        for m in self.avail_mach:
            m.load(**kwargs)
            return(m.process(**kwargs))

    def unload_machines(self, amount):
        for m in self.unavail_mach:
            yield m.unload(amount)
