// 16.1
let notDivisible n m = m % n = 0

// 16.2
let prime n =
  if n = 1 || n = 2 then true
  elif n % 2 = 0 then false
  else
    let mutable isPrime = true
    for i in 3 .. 2 .. n / 2 do
      if n % i = 0 then isPrime <- false
    isPrime