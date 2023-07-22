type F = 
  | AM
  | PM

type TimeOfDay = { hours : int; minutes : int; f: F }

let format x =
    if x.f = PM then (x.hours + 12) * 60 + x.minutes
    else x.hours * 60 + x.minutes

let (.>.) x y = format(x) > format(y)
