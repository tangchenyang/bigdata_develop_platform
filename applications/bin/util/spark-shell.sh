#!/bin/bash
# spark-shell

# concat jars
for jar in $(ls $APPLICATIONS_HOME/lib)
do
    jars="$jars$APPLICATIONS_HOME/lib/$jar,"
done

spark-shell --master yarn --deploy-mode client \
  	    --jars $jars 
  
