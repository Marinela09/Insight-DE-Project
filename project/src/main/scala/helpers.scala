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



object helpers{

  def parse_S3config(filename: String): Map[String,String] = {
      val s3configString = Source.fromFile(filename).getLines.mkString
      val array = s3configString.split("\\s+")
      return Map((array(0) -> array(1)), (array(2) -> array(3)), (array(4) -> array(5)), (array(6) -> array(7)))
  }

}
