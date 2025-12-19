import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform, binom, poisson, zipf, norm, lognorm, chi2, pareto

# -----------------------------
# Création du dossier images
# -----------------------------

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# -----------------------------
# Fonctions de tracé
# -----------------------------

def plot_discrete_distribution(x, pmf, title, filename):
    plt.figure()
    plt.stem(x, pmf, basefmt=" ")
    plt.title(title)
    plt.xlabel("Valeurs")
    plt.ylabel("PMF")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, filename))
    plt.close()

def plot_continuous_distribution(x, pdf, title, filename):
    plt.figure()
    plt.plot(x, pdf)
    plt.title(title)
    plt.xlabel("Valeurs")
    plt.ylabel("PDF")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, filename))
    plt.close()

# -----------------------------
# Lois discrètes
# -----------------------------

def dirac_distribution(a=0, x_range=np.arange(-5, 6)):
    pmf = np.zeros_like(x_range, dtype=float)
    pmf[x_range == a] = 1.0
    plot_discrete_distribution(
        x_range, pmf,
        f"Loi dégénérée (Dirac discret) en {a}",
        "dirac.png"
    )
    return x_range, pmf

def uniform_discrete(n=10):
    x = np.arange(n)
    pmf = np.ones(n) / n
    plot_discrete_distribution(
        x, pmf,
        "Loi uniforme discrète",
        "uniforme_discrete.png"
    )
    return x, pmf

def binomial_distribution(n=20, p=0.4):
    x = np.arange(n + 1)
    pmf = binom.pmf(x, n, p)
    plot_discrete_distribution(
        x, pmf,
        "Loi binomiale",
        "binomiale.png"
    )
    return x, pmf

def poisson_distribution(lam=5):
    x = np.arange(0, 20)
    pmf = poisson.pmf(x, lam)
    plot_discrete_distribution(
        x, pmf,
        "Loi de Poisson",
        "poisson.png"
    )
    return x, pmf

def zipf_distribution(a=2.0, size=20):
    x = np.arange(1, size + 1)
    pmf = zipf.pmf(x, a)
    plot_discrete_distribution(
        x, pmf,
        "Loi de Zipf",
        "zipf.png"
    )
    return x, pmf

# -----------------------------
# Lois continues
# -----------------------------

def normal_distribution(mu=0, sigma=1):
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 400)
    pdf = norm.pdf(x, mu, sigma)
    plot_continuous_distribution(
        x, pdf,
        "Loi normale",
        "normale.png"
    )
    return x, pdf

def lognormal_distribution(mean=0, sigma=1):
    x = np.linspace(0.001, 10, 400)
    pdf = lognorm.pdf(x, sigma, scale=np.exp(mean))
    plot_continuous_distribution(
        x, pdf,
        "Loi log-normale",
        "lognormale.png"
    )
    return x, pdf

def uniform_continuous(a=0, b=1):
    x = np.linspace(a, b, 400)
    pdf = uniform.pdf(x, a, b - a)
    plot_continuous_distribution(
        x, pdf,
        "Loi uniforme continue",
        "uniforme_continue.png"
    )
    return x, pdf

def chi2_distribution(df=3):
    x = np.linspace(0, 20, 400)
    pdf = chi2.pdf(x, df)
    plot_continuous_distribution(
        x, pdf,
        "Loi du Chi²",
        "chi2.png"
    )
    return x, pdf

def pareto_distribution(alpha=3):
    x = np.linspace(1, 10, 400)
    pdf = pareto.pdf(x, alpha)
    plot_continuous_distribution(
        x, pdf,
        "Loi de Pareto",
        "pareto.png"
    )
    return x, pdf

# -----------------------------
# Moyenne et écart-type (discret)
# -----------------------------

def compute_mean(x, p):
    return np.sum(x * p)

def compute_std(x, p):
    mean = compute_mean(x, p)
    return np.sqrt(np.sum(p * (x - mean) ** 2))

# -----------------------------
# Exécution
# -----------------------------

if __name__ == "__main__":
    dirac_distribution()
    uniform_discrete()
    x, p = binomial_distribution()
    poisson_distribution()
    zipf_distribution()
    normal_distribution()
    lognormal_distribution()
    uniform_continuous()
    chi2_distribution()
    pareto_distribution()

    print("Moyenne binomiale :", compute_mean(x, p))
    print("Écart-type binomial :", compute_std(x, p))

