from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def cluster_and_plot(data: list, k: int) -> None:
    kmeans = KMeans(n_clusters = k, random_state=0)
    kmeans.fit(data)

    cluster_labels = kmeans.labels_
    cluster_centroids = kmeans.cluster_centers_


    plt.scatter([v[0] for v in data], [v[1] for v in data], c=cluster_labels, cmap='viridis')
    plt.scatter(cluster_centroids[:, 0], cluster_centroids[:, 1], marker='X', s=200, color='red')
    plt.title("K-Means Clustering")
    plt.xlabel("Gamma")
    plt.ylabel("Alpha")
    plt.show()


def read() -> list:
    data = []
    with open("./fakeBannerData.csv") as file:
        file.readline()
        for line in file:
            vals = tuple(map(float, line.split(",")[1:]))
            data.append(vals)

    return data

def main() -> None:
    data = read()
    cluster_and_plot(data, 5)
    cluster_and_plot(data, 6)


if __name__ == "__main__":
    main()