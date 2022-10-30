from pyflink.common import Duration
from pyflink.common import SimpleStringSchema, Encoder
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment, OutputTag
from pyflink.datastream.connectors import DeliveryGuarantee
from pyflink.datastream.connectors.file_system import FileSource, StreamFormat, FileSink, OutputFileConfig, \
    RollingPolicy
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, KafkaSink, KafkaRecordSerializationSchema

from functions.valenco_translator import ValencoTranslator

observations_output_tag = OutputTag("translated-observations", Types.STRING())
obsCollections_output_tag = OutputTag("translated-obsCollections", Types.STRING())


class ValencoTranslatorTask:
    def __init__(self, **kwargs):
        self.__input_file = kwargs.get('input_file')
        self.__output_file = kwargs.get('output_file')
        self.__kafka_source_config = kwargs.get('kafka_source_config')
        self.__kafka_sink_config = kwargs.get('kafka_sink_config')
        self.__jars_to_add = kwargs.get('jars_to_add', [])

    def translate(self):
        env = StreamExecutionEnvironment.get_execution_environment()
        env.set_parallelism(1)
        env.add_jars(*self.__jars_to_add)

        stream = self.define_source(env).process(ValencoTranslator())

        self.emit_results(stream.get_side_output(observations_output_tag), 'observations')
        self.emit_results(stream.get_side_output(obsCollections_output_tag), 'observation_collections')
        env.execute()

    def define_source(self, env: StreamExecutionEnvironment):
        if self.__input_file is not None:
            ds = env.from_source(
                source=FileSource.for_record_stream_format(
                    StreamFormat.text_line_format(), self.__input_file
                ).process_static_file_set().build(),
                watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
                source_name="file_source"
            )
        if self.__kafka_source_config:
            kafka_props = {'bootstrap.servers': self.__kafka_source_config['bootstrap_servers']}
            kafka_consumer = FlinkKafkaConsumer(self.__kafka_source_config['topic'], SimpleStringSchema(), kafka_props)
            watermark_strategy = WatermarkStrategy.for_bounded_out_of_orderness(Duration.of_seconds(5))
            kafka_consumer.set_start_from_earliest()
            ds = env.add_source(kafka_consumer).assign_timestamps_and_watermarks(watermark_strategy)

        return ds

    def emit_results(self, ds, normalized_data_type):
        ds.print()

        if self.__output_file is not None:
            ds.sink_to(
                sink=FileSink.for_row_format(
                    base_path=self.__output_file,
                    encoder=Encoder.simple_string_encoder("utf-8")
                ).with_output_file_config(
                    OutputFileConfig.builder().with_part_prefix("prefix").with_part_suffix(".ext").build()
                )
                .with_rolling_policy(RollingPolicy.default_rolling_policy())
                .build()
            )
        # ''
        if self.__kafka_sink_config:
            sink = KafkaSink.builder() \
                .set_bootstrap_servers(self.__kafka_sink_config['bootstrap_servers']) \
                .set_property('data_type', normalized_data_type) \
                .set_record_serializer(
                KafkaRecordSerializationSchema
                .builder()
                .set_topic(self.__kafka_sink_config['topic'])
                .set_value_serialization_schema(SimpleStringSchema()).build()
            ) \
                .set_delivery_guarantee(DeliveryGuarantee.AT_LEAST_ONCE) \
                .build()

            ds.sink_to(sink)
