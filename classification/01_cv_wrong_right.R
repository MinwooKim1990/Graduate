library("dplyr")
library("rsample")

set.seed(1234)

genes <- data.frame(as.data.frame(matrix(rnorm(1000*200), nrow = 200)),
                    y = sample(c("cancer", "not"), 200, replace = TRUE))

## WRONG WAY!!
p_vals <- rep(1, 1000)
for(i in 1:1000) {
  p_vals[i] <- t.test(genes %>%
                        filter(y == "cancer") %>%
                        pull(i),
                      genes %>%
                        filter(y == "not") %>%
                        pull(i))$p.value
}
vars <- order(p_vals)[1:20]

cv <- vfold_cv(genes, v = 10)
acc <- rep(0, 10)
for(k in 1:10) {
  fit <- glm(y ~ .,
             binomial,
             analysis(cv$splits[[k]]) %>%
               select(vars, y))

  pred <- predict(fit, assessment(cv$splits[[k]]), type = "response")

  pred <- ifelse(pred < 0.5, levels(genes$y)[1], levels(genes$y)[2])

  acc[k] <- mean(I(assessment(cv$splits[[k]])$y == pred))
}
mean(acc)

## RIGHT WAY!!
# We actually use the same folds to prove the point that it is not a more lucky
# fold selection that gives the correct estimate.
#cv <- vfold_cv(genes, v = 10)
acc2 <- rep(0, 10)
for(k in 1:10) {
  cat(glue::glue("Fold {k} computing ... "))
  p_vals <- rep(1, 1000)
  for(i in 1:1000) {
    p_vals[i] <- t.test(analysis(cv$splits[[k]]) %>%
                          filter(y == "cancer") %>%
                          pull(i),
                        analysis(cv$splits[[k]]) %>%
                          filter(y == "not") %>%
                          pull(i))$p.value
  }
  vars <- order(p_vals)[1:20]

  fit <- glm(y ~ .,
             binomial,
             analysis(cv$splits[[k]]) %>%
               select(vars, y))

  pred <- predict(fit, assessment(cv$splits[[k]]), type = "response")

  pred <- ifelse(pred < 0.5, levels(genes$y)[1], levels(genes$y)[2])

  acc2[k] <- mean(I(assessment(cv$splits[[k]])$y == pred))
  cat(glue::glue("{acc2[k]*100}% accuracy this fold\n\n"))
}
mean(acc2)
