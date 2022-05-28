install.packages('animation')
require(animation)
set.seed(42)
balls <- 200
layers<- 15
ani.options(nmax = balls + layers - 2, 2)
galton.sim = quincunx(balls = balls,col.balls = rainbow(layers))
barplot(galton.sim, space = 0)
