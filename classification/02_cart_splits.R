set.seed(212)
library("rpart")

# Let's "cheat" and simulate a dataset where the tree model structure is
# actually the truth ... so this is where we should do very well!
df <- data.frame(x = c(runif(20, 0, 0.4), runif(40, 0.4, 0.65), runif(30, 0.65, 1)),
                 y = c(rnorm(20, 1.5),    rnorm(40, 0),         rnorm(30, 2)))

plot(df$x, df$y)

fit <- rpart(y ~ x, df)
plotcp(fit)
fitp <- prune(fit, 0.052)
fitp
plot(fitp, margin = 0.1)
text(fitp, cex=0.5)

plot(df$x, df$y)
x <- data.frame(x = seq(0,1,len=200))
y <- dplyr::case_when(x < 0.4 ~ 1.5,
                      x < 0.65 ~ 0,
                      TRUE ~ 2)
lines(x$x, predict(fit,x), col = "red", lwd = 3)
lines(x$x, predict(fitp,x), col = "blue", lwd = 3)
lines(x$x, y, col = "green", lwd = 3)


################################################################################

# Let's repeat with loads of data and see that we actually don't overfit or need
# to prune.
df <- data.frame(x = c(runif(200, 0, 0.4), runif(400, 0.4, 0.65), runif(300, 0.65, 1)),
                 y = c(rnorm(200, 1.5),    rnorm(400, 0),         rnorm(300, 2)))

plot(df$x, df$y)

fit <- rpart(y ~ x, df)
plotcp(fit)
plot(fit, margin = 0.1)
text(fit, cex=0.5)

plot(df$x, df$y)
x <- data.frame(x = seq(0,1,len=200))
y <- dplyr::case_when(x < 0.4 ~ 1.5,
                      x < 0.65 ~ 0,
                      TRUE ~ 2)
lines(x$x, predict(fit,x), col = "blue", lwd = 3)
lines(x$x, y, col = "green", lwd = 3)
