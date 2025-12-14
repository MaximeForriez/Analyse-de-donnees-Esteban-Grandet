import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform, binom, poisson, zipf, norm, lognorm, chi2, pareto

# -----------------------------
# 1. Visualisation des lois
# -----------------------------

def plot_discrete_distribution(x, pmf, title):
    plt.figure()
    plt.stem(x, pmf, basefmt=" ")
    plt.title(title)
    plt.xlabel("Valeurs")
    plt.ylabel("PMF")
    plt.grid(True)
    plt.show()

def plot_continuous_distribution(x, pdf, title):
    plt.figure()
    plt.plot(x, pdf)
    plt.title(title)
    plt.xlabel("Valeurs")
    plt.ylabel("PDF")
    plt.grid(True)
    plt.show()

# Loi de Dirac (delta de Dirac en version discrète)
def dirac_distribution(a=0, x_range=np.arange(-5,6)):
    pmf = np.zeros_like(x_range, dtype=float)
    pmf[x_range == a] = 1.0
    plot_discrete_distribution(x_range, pmf, f"Loi de Dirac centrée en {a}")
    return x_range, pmf

# Loi uniforme discrète
def uniform_discrete(n=10):
    x = np.arange(n)
    pmf = np.ones(n) / n
    plot_discrete_distribution(x, pmf, "Loi uniforme discrète")
    return x, pmf

# Loi binomiale
def binomial_distribution(n=20, p=0.4):
    x = np.arange(n+1)
    pmf = binom.pmf(x, n, p)
    plot_discrete_distribution(x, pmf, "Loi binomiale")
    return x, pmf

# Loi de Poisson (discrète)
def poisson_distribution(lam=5):
    x = np.arange(0, 20)
    pmf = poisson.pmf(x, lam)
    plot_discrete_distribution(x, pmf, "Loi de Poisson (discrète)")
    return x, pmf

# Loi de Zipf-Mandelbrot
def zipf_mandelbrot_distribution(a=2.0, size=20):
    x = np.arange(1, size+1)
    pmf = zipf.pmf(x, a)
    plot_discrete_distribution(x, pmf, "Loi de Zipf-Mandelbrot")
    return x, pmf

# -----------------------------
# Lois continues
# -----------------------------

def poisson_continuous(lam=5):
    x = np.linspace(0, 20, 400)
    pdf = poisson.pmf(np.round(x), lam)  # approximation
    plot_continuous_distribution(x, pdf, "Loi de Poisson (approx. continue)")
    return x, pdf

def normal_distribution(mu=0, sigma=1):
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 400)
    pdf = norm.pdf(x, mu, sigma)
    plot_continuous_distribution(x, pdf, "Loi Normale")
    return x, pdf

def lognormal_distribution(mean=0, sigma=1):
    x = np.linspace(0.001, 10, 400)
    pdf = lognorm.pdf(x, sigma, scale=np.exp(mean))
    plot_continuous_distribution(x, pdf, "Loi Log-Normale")
    return x, pdf

def uniform_continuous(a=0, b=1):
    x = np.linspace(a, b, 400)
    pdf = uniform.pdf(x, a, b-a)
    plot_continuous_distribution(x, pdf, "Loi Uniforme Continue")
    return x, pdf

def chi2_distribution(df=3):
    x = np.linspace(0, 20, 400)
    pdf = chi2.pdf(x, df)
    plot_continuous_distribution(x, pdf, "Loi du Chi2")
    return x, pdf

def pareto_distribution(alpha=3):
    x = np.linspace(1, 10, 400)
    pdf = pareto.pdf(x, alpha)
    plot_continuous_distribution(x, pdf, "Loi de Pareto")
    return x, pdf

# -----------------------------
# 2. Fonctions moyenne et écart-type
# -----------------------------

def compute_mean(x, p):
    return np.sum(x * p)

def compute_std(x, p):
    mean = compute_mean(x, p)
    return np.sqrt(np.sum(p * (x - mean)**2))

# Exemple d'utilisation pour test :
if __name__ == "__main__":
    x, p = binomial_distribution()
    print("Moyenne =", compute_mean(x, p))
    print("Écart-type =", compute_std(x, p))

