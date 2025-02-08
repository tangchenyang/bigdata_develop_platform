from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, TableDescriptor, Schema, DataTypes

words = ["hello", "world", "hello", "flink", "hello", "pyflink"]

if __name__ == '__main__':
    execution_env = StreamExecutionEnvironment.get_execution_environment()
    table_env = StreamTableEnvironment.create(stream_execution_environment=execution_env)

    table_env.create_temporary_table(
        'words',
        TableDescriptor.for_connector('datagen')
        .schema(Schema.new_builder()
                .column('word_id', DataTypes.INT())
                .build())
        .option('fields.word_id.kind', 'random')
        .option('fields.word_id.min', '0')
        .option('fields.word_id.max', str(len(words) - 1))
        .option('rows-per-second', '5')
        .build())

    words_table = table_env.from_path("words")
    word_data_stream = table_env.to_data_stream(words_table)


    def id_to_word(r):
        # word_id is the first column of the input row
        return words[r[0]]


    word_counts = (
        word_data_stream.map(id_to_word)
        .map(lambda i: (i, 1), output_type=Types.TUPLE([Types.STRING(), Types.INT()]))
        .key_by(lambda i: i[0])
        .reduce(lambda i, j: (i[0], i[1] + j[1])))

    word_counts.print()

    execution_env.execute()
