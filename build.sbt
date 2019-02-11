name := "rankingsmall"

version := "1.0"

scalaVersion := "2.11.8"

libraryDependencies ++= Seq(
"org.apache.spark" %% "spark-core" % "2.2.1" % "provided",
"org.apache.spark" %% "spark-sql" % "2.2.1",
"org.postgresql" % "postgresql" % "42.2.5"
)
