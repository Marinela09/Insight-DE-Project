from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'Marinela',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'BatchScheduler', default_args=default_args, schedule_interval=timedelta(days=30))

bash_command_template = ''' cd; cd /home/ubuntu/project;
		  spark-submit --jars /home/ubuntu/project/postgresql-42.2.5.jar
		   --class rankingsmall --master spark://ec2-34-239-206-246.compute-1.amazonaws.com:7077
	           --executor-memory 6G /home/ubuntu/project/target/scala-2.11/rankingsmall_2.11-1.0.jar
                   /home/ubuntu/project/config/'''

t1 = BashOperator(
    task_id='Compute_Jan',
    bash_command=bash_command_template + 's3bucketJanuary.config',
    dag=dag)

t2 = BashOperator(
    task_id='Compute_Feb',
    bash_command=bash_command_template + 's3bucketFebruary.config',
    dag=dag)

t3 = BashOperator(
    task_id='Compute_Mar',
    bash_command=bash_command_template + 's3bucketMarch.config',
    dag=dag)

t4 = BashOperator(
    task_id='Compute_Apr',
    bash_command=bash_command_template + 's3bucketApril.config',
    dag=dag)

t5 = BashOperator(
    task_id='Compute_May',
    bash_command=bash_command_template + 's3bucketMay.config',
    dag=dag)

t6 = BashOperator(
    task_id='Compute_Jun',
    bash_command=bash_command_template + 's3bucketJune.config',
    dag=dag)

t7 = BashOperator(
    task_id='Compute_Jul',
    bash_command=bash_command_template + 's3bucketJuly.config',
    dag=dag)

t8 = BashOperator(
    task_id='Compute_Aug',
    bash_command=bash_command_template + 's3bucketAugust.config',
    dag=dag)

t9 = BashOperator(
    task_id='Compute_Sep',
    bash_command=bash_command_template + 's3bucketSeptember.config',
    dag=dag)

t10 = BashOperator(
    task_id='Compute_Oct',
    bash_command=bash_command_template + 's3bucketOctober.config',
    dag=dag)

t11 = BashOperator(
    task_id='Compute_Nov',
    bash_command=bash_command_template + 's3bucketNovember.config',
    dag=dag)

t12 = BashOperator(
    task_id='Compute_Dec',
    bash_command=bash_command_template + 's3bucketDecember.config',
    dag=dag)


