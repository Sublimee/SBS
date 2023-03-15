let curry f = function x -> (function y -> f(x, y))

let uncurry f = function (x, y) -> f x y