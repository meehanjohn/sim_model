import pandas as pd
import numpy as np
import scipy.stats as stats

class machine:
    def __init__(self, type, i, **kwargs):
        self.type = type
        self.id = type+str(i)
        self.facility = kwargs.get('facility')
        self.queue = pd.DataFrame(
            {
            'Color':None,
            'Size':None,
            'Flavor':None,
            'Rem':0
            },
            index=[1]
        )

    def __repr__(self):
        return(self.id)

    @property
    def available(self):
        if (self.queue.Rem == 0).all():
            return True
        else:
            return False

    def get_rate(self, **kwargs):
        def fixed_rate(filename, facility):
            rates = pd.read_csv('files/classifier_rate.csv')
            rate = int(rates[rates['Site'] == facility]['Processing_Rate'])
            return(rate)

        def random_rate(filename, facility, **kwargs):
            # Locate historical rate data for a given location, flavor, and size
            jb_size = kwargs.get('jb_size')
            jb_flavor = kwargs.get('jb_flavor')
            package_type = kwargs.get('package_type')
            hist_rate = pd.read_csv(filename)

            if jb_flavor:
                diff_var = 'Flavor'
            elif package_type:
                diff_var = 'Packaging_Type'
            else:
                raise KeyError('Not enough arguments supplied to look up rate')

            mask = (
                (hist_rate.Site == facility)
                & (hist_rate.Size == jb_size)
                & (hist_rate[diff_var] == (jb_flavor or package_type))
            )

            hist_rate = hist_rate[mask]['Processing_Rate']

            # Determine sample mean and standard deviation
            s_mean = np.mean(hist_rate)
            s_sd = np.std(hist_rate)

            # Simulate processing rate using random variable
            # Following sample normal distribution
            rate = s_sd*stats.norm.ppf(np.random.random())+s_mean
            return(rate)

        if self.type == 'classifier':
            filename = 'files/classifier_rate.csv'
            self.rate = fixed_rate(filename, self.facility)

        elif self.type == 'pfo':
            filename = 'files/pfo_rate.csv'
            self.rate = random_rate(filename, self.facility, **kwargs)

        elif self.type == 'packaging':
            filename = 'files/packaging.csv'
            self.rate = random_rate(filename, self.facility, **kwargs)

        else:
            raise ValueError('Invalid Machine Type')

        return(self.rate)


    def load(self, **kwargs):
        self.jb_color = kwargs.get('jb_color')
        self.jb_size = kwargs.get('jb_size')
        self.jb_flavor = kwargs.get('jb_flavor')
        self.package_type = kwargs.get('package_type')

    def process(self, amount, **kwargs):
        if self.type == 'classifier':
            split = pd.read_csv('files/classifier_split.csv')
            split = split[split['Color'] == self.jb_color]
            split['Rem'] = split.apply(
                lambda x: int(amount*x.Percentage/100),
                axis=1
            )
            self.queue = split

        else:
            self.queue = pd.DataFrame(
                {
                'Color':self.jb_color,
                'Size':self.jb_size,
                'Flavor':self.jb_flavor,
                'Rem':amount
                },
                index=[1]
            )

        rate = self.get_rate(
            jb_color=self.jb_color,
            jb_size=self.jb_size,
            jb_flavor=self.jb_flavor,
            package_type = self.package_type
        )
        process_time = amount/rate
        return(process_time)

    def unload(self, amount):
        out = self.queue.copy()
        out.Rem = out.Rem.apply(
            lambda x: min(x, amount)
        )
        self.queue.Rem = self.queue.Rem.apply(
            lambda x: max(0, x-amount)
        )
        return(out)
