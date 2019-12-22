from modules.machine import machine

class processing_cell:
    def __init__(self, type, **kwargs):
        self.type = type
        if type == 'packaging':
            self.num_machines = (
                kwargs.get('boxing_machines'),
                kwargs.get('bagging_machines')
            )
        else:
            self.num_machines = kwargs.get('num_machines')
        self.facility = kwargs.get('facility')
        self.machines = [
            machine(type, i, **kwargs) for i in range(num_machines)
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
                queue = m.empty()
                queue.Queue = queue.Queue - amount
                m.queue = queue
                return(queue)
