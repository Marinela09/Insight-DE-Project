import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.sql._
import org.apache.spark.sql.types._
import org.apache.spark.sql.SQLContext
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.mapreduce.Job
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat
import org.apache.hadoop.io.{Text, LongWritable}
import org.postgresql.Driver
import scala.io.Source
import java.io.{FileNotFoundException, IOException}
import java.util.Arrays
import org.apache.spark.sql.functions.lit
import org.apache.spark.sql.SaveMode
import java.time.LocalDateTime

import helpers._

object rankingsmall{
    def main(args: Array[String]) : Unit = {

        // get and process configurations for s3 bucket
        val s3config = helpers.parse_S3config(args(0))

        // set up spark context
        val credfile = "credentials"
        val creditems = Source.fromFile(credfile).getLines.toArray
        val conf = new SparkConf().setMaster(creditems(0)).setAppName("Ranking")
        val sc = new SparkContext(conf)

        val awsAccessKeyId = sys.env("AWS_ACCESS_KEY_ID")
        val awsSecretAccessKey = sys.env("AWS_SECRET_ACCESS_KEY")

        sc.hadoopConfiguration.set("fs.s3.awsAccessKeyId", awsAccessKeyId)
        sc.hadoopConfiguration.set("fs.s3.awsSecretAccessKey", awsSecretAccessKey)
        sc.hadoopConfiguration.set("fs.s3.endpoint", "s3.us-east-1.amazonaws.com")
        sc.hadoopConfiguration.set("fs.s3.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")

        // create context text file
        val crawlDir = s3config("list_of_paths")
        val files = sc.textFile(crawlDir) 
        val arr = files.collect()
        var l = 5000

	var endPoint = arr.length
	while (l < endPoint){
	  val p = scala.util.Random.nextInt(endPoint)
	  arr(p) = arr(endPoint-1)
	  endPoint -= 1 
	}
	
	sc.hadoopConfiguration.set("textinputformat.record.delimiter", "WARC-Target-URI:")

        // form an array of file paths to be searched and create an rdd from them
        val arr2 = Array.ofDim[String](l)
        for (i <- 0 to l-1){
           arr2(i) = "s3://commoncrawl/" + arr(i)
        }

	val filenames = arr2.mkString(",")
        val rdd0 = sc.textFile(filenames)
        val rdd = rdd0.coalesce(12)

        // define a set of categories to be ranked
        val categories = Set("MySQL", "Amazon Redshift", "Apache Cassandra", "Apache Druid", "Redis", "Oracle Database", "PostgreSQL", "Riak",
        "HBase", "DynamoDB", "MongoDB", "Apache Solr", "Couchbase", "Neo4j", "OrientDB", "ArangoDB", "JanusGraph",
        "InfluxDB", "Memcached", "Hazelcast")


        // compute the frequencies for the categories
        val pageCountsCollection =  rdd.map(record =>  count(record, categories))
        val t0 = pageCountsCollection.filter(notEmpty)
        val t1 = t0.flatMap(x => x.map(y => (y._1, y._2))).reduceByKey((x,y) => (x+y))

        // create sql context and convert the rdd to a dataframe
        val sqlContext : SQLContext = new SQLContext(sc)
        import sqlContext.implicits._
        val colNames = Seq("name", "frequency")
        val df = t1.toDF(colNames:_*)
        val df2 = df.withColumn("month", lit(s3config("month")))


        //postgres connection and write results
        val prop = new java.util.Properties
        prop.setProperty("driver", "org.postgresql.Driver")
        prop.setProperty("user", creditems(1))
        prop.setProperty("password", creditems(2))
        val url = "jdbc:postgresql://" + creditems(3) + "/postgres"
        val table = "results" + s3config("month")
        df2.write.jdbc(url, table, prop)
    }


    def count(record : String, cat : Set[String]) : collection.mutable.Map[String, Int] = {
        val m = collection.mutable.Map[String, Int]()
        for (categ <- cat) {
            if (record.contains(categ) == true)
                {m += (categ -> 1)}
        }
        return m
    }

    def notEmpty(record: collection.mutable.Map[String,Int]) : Boolean = {
        return !record.isEmpty
    }

    def time[R](block: => R): R = {
        val t0 = System.nanoTime()
        val result = block    // call-by-name
        val t1 = System.nanoTime()
        println("Elapsed time: " + (t1 - t0)/1000000.0 + "ms")
        result
    }


}

