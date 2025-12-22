square :: Int -> Int
square x = x * x

add :: Int -> Int -> Int
add x y = x + y

absolute :: Int -> Int
absolute x = if x >= 0 then x else -x

grade :: Int -> String
grade score
    | score >= 90 = "Excellent"
    | score >= 75 = "Good"
    | score >= 60 = "Satisfactory"
    | otherwise = "Fail"

main = do
    print (square 10)
    print (add 10 15)
    print (absolute 100)
    putStrLn (grade 95) 