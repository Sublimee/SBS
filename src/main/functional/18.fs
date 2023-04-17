let f n =  
   let mutable result = 1 
   let mutable i = 1 
   while i <= n do 
     result <- result * i 
     i <- i + 1 
   result

let fibo n =
  let mutable a = 0
  let mutable b = 1
  for i in 0 .. n - 1 do
    let c = a + b
    a <- b
    b <- c
  a
