data("iris")
print(head(iris))

cluster = kmeans(iris[, c(3, 4)], 3)
plot(iris[, c(3, 4)], col = cluster$cluster, pch = 20, cex = 1)
points(cluster$centers, pch = 4, cex = 4, lwd = 4)