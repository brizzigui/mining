data(faithful)
print(head(faithful))
library(caret)
inTrain = createDataPartition(y = faithful$waiting, p=0.5, list=FALSE)
trainfaith = faithful[inTrain,]
testfaith = faithful[-inTrain,]

print(nrow(trainfaith))
print(nrow(testfaith))


model = lm(eruptions ~ waiting, data=trainfaith)
print(predict(model, data.frame(waiting = 100)))
plot(trainfaith$waiting, trainfaith$eruptions, pch = 9, col="red")
lines(trainfaith$waiting, model$fitted.values, lwd=5)