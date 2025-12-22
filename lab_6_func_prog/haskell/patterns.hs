import Control.Arrow (Arrow(second))
addVectors :: (Double, Double) -> (Double, Double) -> (Double, Double)
addVectors (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)

first' :: (a, b, c) -> a
first' (x, _, _) = x

second' :: (a, b, c) -> b
second' (_, y, _) = y

third' :: (a, b, c) -> c
third' (_, _, z) = z

describeList :: [a] -> String
describeList xs = case xs of
    [] -> "Empty list"
    [x] -> "Singleton list"
    xs -> "Long list"

main = do
    print(addVectors (1, 5) (5, 10))
    print(first' (1, 2, 3))
    print(second' (1, 2, 3))
    print(third' (1, 2, 3))