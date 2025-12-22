factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

sumList :: [Int] -> Int
sumList = sum

length' :: [a] -> Int
length' [] = 0
length' (_:xs) = 1 + length' xs

fibonacci :: Int -> Int
fibonacci 0 = 0
fibonacci 1 = 1
fibonacci n = fibonacci (n-1) + fibonacci (n-2)

main = do
    print (factorial 15)
    print (sumList [1..99])
    print (length'[1..99])
    print (fibonacci 15)
