from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode

words = ["hello", "world", "hello", "flink", "hello", "pyflink"]

if __name__ == '__main__':
    execution_env = StreamExecutionEnvironment.get_execution_environment()
    execution_env.set_runtime_mode(RuntimeExecutionMode.BATCH)

    word_data_stream = execution_env.from_collection(words)

    word_counts = (
        word_data_stream
        .map(lambda i: (i, 1), output_type=Types.TUPLE([Types.STRING(), Types.INT()]))
        .key_by(lambda i: i[0])
        .reduce(lambda i, j: (i[0], i[1] + j[1])))

    word_counts.print()

    execution_env.execute()
