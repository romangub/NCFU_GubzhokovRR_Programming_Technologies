map' :: (a -> b) -> [a] -> [b]
map' _ [] = []
map' f (x:xs) = f x : map' f xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' _ [] = []
filter' p (x:xs)
    | p x       = x: filter' p xs
    | otherwise = filter' p xs

foldl' :: (b -> a -> b) -> b -> [a] -> b
foldl' _ acc [] = acc
foldl' f acc (x:xs) = foldl' f (f acc x) xs

compose :: (b -> c) -> (a -> b) -> a -> c
compose f g x = f (g x)

main = do
    print(map' (subtract 3) [10, 9, 8, 7, 6])
    print(filter' odd [10, 9, 8, 7, 6])
    print(foldl' (*) 10 [1.5, 0.5, 2])
    print(compose even (*3) 4)