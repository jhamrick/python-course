import numpy as np

class GaussianRV(object):
    """Gaussian-distributed random variable, parameterized by 'mu'
    (the mean) and 'sigma' (the standard deviation).  Includes methods
    for sampling, evaluation, and transformation (e.g., multiplying
    with another Gaussian).

    """

    def __init__(self, mu, sigma, seed=0):
        self.seed = seed
        self.rand = np.random.RandomState(self.seed)
        self.set_mu(mu)
        self.set_sigma(sigma)

    def _calc_Z(self):
        """Calculate the constant for the logpdf"""
        self._Z = -0.5 * np.log(2 * np.pi * self._var)

    def set_mu(self, mu):
        """Set the value of mu"""
        self.mu = mu
    def set_sigma(self, sigma):
        """Set the value of sigma"""
        self.sigma = sigma
        # Also calculate the variance and the Z constant
        self._var = self.sigma ** 2
        self._calc_Z()

    def sample(self, num=1):
        """Draw samples from the distribution"""
        samples = self.rand.normal(
            self.mu, self.sigma, size=num)
        return samples

    def logpdf(self, vals):
        """Evaluate the the logpdf at 'vals'"""
        logpdf = self._Z - (((vals - self.mu) ** 2) / (2 * self._var))
        return logpdf

    def pdf(self, vals):
        """Evaluate the pdf at 'vals'"""
        pdf = np.exp(self.logpdf(vals))
        return pdf

    def plot(self):
        # draw some samples
        samps = self.sample(100000)
        # create a range of values spanning 4 standard deviations on
        # either side of mu
        X = self.mu + np.linspace(-4*self.sigma, 4*self.sigma, 1000)
        # calculate the pdf for these values
        pdf = self.pdf(X)
        # plot a histogram of the samples
        plt.hist(samps,
                 normed=True, bins=100,
                 histtype='stepfilled',
                 label='samples (mu=%s, sigma=%s)' % (self.mu, self.sigma))
        # plot the pdf on top of the histogram
        plt.plot(X, pdf, 'r-', linewidth=2,
                 label='pdf (mu=%s, sigma=%s)' % (self.mu, self.sigma))

    def __str__(self):
        """String representation of the GaussianRV"""
        mytype = type(self).__name__
        s = "<%s; mu=%s; sigma=%s>" % (mytype, self.mu, self.sigma)
        return s

    def __add__(self, other):
        """Create a new GaussianRV with mu=mu+other"""
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu + other,
                self.sigma,
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv

    def __iadd__(self, other):
        """Shift mu=mu+other"""
        if isinstance(other, (int, float)):
            self.set_mu(self.mu + other)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self

    def __sub__(self, other):
        """Create a new GaussianRV with mu=mu-other"""
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu - other,
                self.sigma,
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv

    def __isub__(self, other):
        """Shift mu=mu-other"""
        if isinstance(other, (int, float)):
            self.set_mu(self.mu - other)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self

    def __mul__(self, other):
        """Create a new GaussianRV, either by multiplying the mean and
        standard deviation by 'other' or by computing the product of
        two Gaussians:

        https://ccrma.stanford.edu/~jos/sasp/Product_Two_Gaussian_PDFs.html

        """
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu*other,
                self.sigma*other,
                seed=self.seed)
        elif isinstance(other, GaussianRV):
            m0 = float(self.mu)
            m1 = float(other.mu)
            v0 = float(self._var)
            v1 = float(other._var)
            new_m = (m0 * v1 + m1 * v0) / (v0 + v1)
            new_v = v0 * v1 / (v0 + v1)
            new_rv = GaussianRV(
                new_m,
                np.sqrt(new_v),
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv
        
    def __imul__(self, other):
        """Multiply the mean and standard deviation by 'other' or
        compute the product of two Gaussians:

        https://ccrma.stanford.edu/~jos/sasp/Product_Two_Gaussian_PDFs.html

        """
        if isinstance(other, (int, float)):
            self.set_mu(self.mu * other)
            self.set_sigma(self.sigma * other)
        elif isinstance(other, GaussianRV):
            m0 = float(self.mu)
            m1 = float(other.mu)
            v0 = float(self._var)
            v1 = float(other._var)
            new_m = (m0 * v1 + m1 * v0) / (v0 + v1)
            new_v = v0 * v1 / (v0 + v1)
            self.set_mu(new_m)
            self.set_sigma(np.sqrt(new_v))
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self

    def __div__(self, other):
        """Create a new GaussianRV by dividing the mean and variance
        by 'other'.

        """
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu / other,
                self.sigma / other,
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv

    def __idiv__(self, other):
        """Divide the mean and standard deviation by 'other'."""
        if isinstance(other, (int, float)):
            self.set_mu(self.mu / other)
            self.set_sigma(self.sigma / other)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self


class StandardNormalRV(GaussianRV):
    """Standard normal random variable, i.e. zero-mean and unit
    standard deviation.  Includes methods for sampling, evaluation,
    and transformation (e.g., multiplying with another Gaussian).

    """

    def __init__(self, seed=0):
        GaussianRV.__init__(self, 0, 1, seed=seed)
        self.set_mu = None
        self.set_sigma = None
        self.__iadd__ = None
        self.__isub__ = None
        self.__imul__ = None
        self.__idiv__ = None
