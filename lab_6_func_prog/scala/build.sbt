name := "scala-fp-lab"

version := "1.0"

scalaVersion := "2.13.10"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "3.4.0",
  "org.apache.spark" %% "spark-sql" % "3.4.0"
)

// Для компиляции без Spark (закомментируйте зависимости выше и используйте это)
// scalaVersion := "2.13.10"


