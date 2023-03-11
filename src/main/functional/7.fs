// 20.3.1
let vat n (x : float) = (float (100 + n) / 100.0) * x

// 20.3.2
let unvat n (x : float) = x / (float (n + 100) / 100.0)

// 20.3.3
let min f =
  let rec next = function
    | x when f x = 0 -> x
    | x -> next(x + 1)
  next 1