import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
import csv

def main():
    # Read CSV
    with open("acoes_close2019.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        labels = next(reader)
        data = np.array([[float(x) for x in row] for row in reader])

    # === Equivalent to: cor(t(acoes_fecha2019)) in R ===
    corr = np.corrcoef(data.T)

    # === Equivalent to: as.dist(1 - cor(...)) ===
    dist_matrix = 1 - corr

    condensed_dist = squareform(dist_matrix, checks=False)

    # === Equivalent to: hclust(..., method="complete") ===
    Z = linkage(condensed_dist, method="complete")

    # === Equivalent to: plot(..., ylab="Altura", xlab="Grupos de ações") ===
    plt.figure(figsize=(10, 5))
    dendrogram(Z, labels=labels, orientation='top')
    plt.xlabel("Grupos de ações")
    plt.ylabel("Altura")
    plt.title("")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
