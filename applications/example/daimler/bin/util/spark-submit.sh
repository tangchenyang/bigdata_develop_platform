# concat jars

current_dir=$(cd `dirname $0` && pwd)

libDir=$current_dir/../../libs
# shellcheck disable=SC2045
for jar in $(ls $libDir)
do
    jars="$jars${libDir}/$jar,"
done

spark-submit --master yarn --deploy-mode client \
             --jars $jars \
             --class $@