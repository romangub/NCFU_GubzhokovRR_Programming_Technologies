countEven :: [Int] -> Int
countEven [] = 0
countEven (x:xs)
    | even x    = 1 + countEven xs
    | otherwise = countEven xs

positiveSquares :: [Int] -> [Int]
positiveSquares [] = []
positiveSquares (x:xs)
    | x >= 0    = x^2 : positiveSquares xs
    | otherwise = positiveSquares xs

bubbleSort :: [Int] -> [Int]
bubbleSort xs = iterate bubblePass xs !! length xs
  where
    bubblePass [] = []
    bubblePass [x] = [x]
    bubblePass (x:y:ys)
        | x > y = y : bubblePass (x:ys)
        | otherwise = x : bubblePass (y:ys)


main = do
    print (countEven [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    print (positiveSquares [-1, -2, -3, 5, 6, 7])
    print (bubbleSort [1,5,6,3,9,3,0])