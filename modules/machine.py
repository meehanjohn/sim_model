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
            'jb_color':None,
            'jb_size':None,
            'jb_flavor':None,
            'amount':0
            },
            index=[1]
        )

    def __repr__(self):
        return(self.id)

    @property
    def available(self):
        if (self.queue.amount == 0).all():
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

            if 'Flavor' in hist_rate.columns:
                diff_var = 'Flavor'
                diff_val = jb_flavor
            else:
                diff_var = 'Packaging_Type'
                diff_val = package_type
            ## TODO: figure out how to mask dataframe on
            ## either flavor OR package type
            mask = (
                (hist_rate.Site == facility)
                & (hist_rate.Size == jb_size)
                & (hist_rate[diff_var] == diff_val)
            )

            hist_rate = hist_rate[mask]['Processing_Rate']

            # Determine sample mean and standard deviation
            s_mean = np.mean(hist_rate)
            s_sd = np.std(hist_rate)

            # Simulate processing rate using random variable
            # Following sample normal distribution
            rate = s_sd*stats.norm.ppf(np.random.random())+s_mean
            # Rate units are pounds/hour
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
            split = split[split.jb_color == self.jb_color]
            split['amount'] = split.apply(
                lambda x: int(amount*x.percentage/100),
                axis=1
            )
            self.queue = split[['jb_color', 'jb_size', 'percentage', 'amount']]

        else:
            self.queue = pd.DataFrame(
                {
                'jb_color':self.jb_color,
                'jb_size':self.jb_size,
                'jb_flavor':self.jb_flavor,
                'amount':amount
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
        # Process time in hours
        return(process_time)

    def unload(self, amount):
        out = self.queue.copy()
        out.amount = out.amount.apply(
            lambda x: min(x, amount)
        )
        self.queue.amount = self.queue.amount.apply(
            lambda x: max(0, x-amount)
        )
        return(out)
