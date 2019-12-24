from modules.machine import machine

class processing_cell:
    def __init__(self, type, **kwargs):
        self.type = type
        self.facility = kwargs.get('facility')

        if type == 'packaging':
            self.num_machines = {
                'boxing_machines':kwargs.get('boxing_machines'),
                'bagging_machines':kwargs.get('bagging_machines')
            }
            self.machines = [
                machine(type, i=1, **dict(key=value), **kwargs)
                for key,value in self.num_machines.items()
            ]
        else:
            self.num_machines = kwargs.get('num_machines')
            self.machines = [
                machine(type, i, **kwargs) for i in range(self.num_machines)
            ]

    def __repr__(self):
        return("{0} Processing Cell".format(self.type))

    def load_machines(self, amount, **kwargs):
        for m in self.machines:
            if m.available:
                m.load(**kwargs)
                m.process(amount, **kwargs)

    def empty_machines(self, amount):
        for m in self.machines:
            if m.available:
                raise Exception('Machine is already empty.')
            else:
                out = m.unload(amount)
                return(out)
