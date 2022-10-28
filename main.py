import argparse
import logging
import os
import sys

from pyflink.common import Duration
from pyflink.common import SimpleStringSchema, Encoder
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment, OutputTag
from pyflink.datastream.connectors import DeliveryGuarantee
from pyflink.datastream.connectors.file_system import FileSource, StreamFormat, FileSink, OutputFileConfig, \
    RollingPolicy
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, KafkaSink, \
    KafkaRecordSerializationSchema

from Functions.valenco_translator import ValencoTranslator

observations_output_tag = OutputTag("translated-observations", Types.STRING())
obsCollections_output_tag = OutputTag("translated-obsCollections", Types.STRING())


def valenco_translate(input_path, output_path, isKafka):
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    kafka_jar = f"file:///{os.path.dirname(os.path.realpath(__file__))}/connectors/flink-sql-connector-kafka-1.16.0.jar"
    env.add_jars(kafka_jar)

    stream = define_source(env, input_path, isKafka).process(ValencoTranslator())

    emit_results(
        stream.get_side_output(observations_output_tag),
        output_path,
        isKafka
    )
    emit_results(
        stream.get_side_output(obsCollections_output_tag),
        output_path,
        isKafka
    )
    env.execute()


def define_source(env, input_path, is_kafka):
    if input_path is not None:
        ds = env.from_source(
            source=FileSource.for_record_stream_format(StreamFormat.text_line_format(), input_path).
            process_static_file_set().build(),
            watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
            source_name="file_source"
        )
    elif is_kafka:
        kafka_props = {'bootstrap.servers': 'localhost:9092', 'group.id': 'pyflink-e2e-source'}
        kafka_consumer = FlinkKafkaConsumer("source_topic", SimpleStringSchema(), kafka_props)
        watermark_strategy = WatermarkStrategy.for_bounded_out_of_orderness(Duration.of_seconds(5))
        kafka_consumer.set_start_from_earliest()
        ds = env.add_source(kafka_consumer).assign_timestamps_and_watermarks(watermark_strategy)

    return ds


def emit_results(ds, output_path, is_kafka):
    if output_path is not None:
        ds.sink_to(
            sink=FileSink.for_row_format(base_path=output_path, encoder=Encoder.simple_string_encoder("utf-8"))
            .with_output_file_config(
                OutputFileConfig.builder()
                .with_part_prefix("prefix")
                .with_part_suffix(".ext")
                .build())
            .with_rolling_policy(RollingPolicy.default_rolling_policy())
            .build()
        )
    else:
        print("Printing result to stdout. Use --output to specify output path.")
        ds.print()
        if is_kafka:
            sink = KafkaSink.builder() \
                .set_bootstrap_servers('localhost:9092') \
                .set_record_serializer(
                KafkaRecordSerializationSchema.builder().set_topic("dest_topic").set_value_serialization_schema(
                    SimpleStringSchema()).build()
            ) \
                .set_delivery_guarantee(DeliveryGuarantee.AT_LEAST_ONCE) \
                .build()

            ds.sink_to(sink)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input', required=False, help='Input file to process.')
    parser.add_argument('--output', dest='output', required=False, help='Output file to write results to.')
    parser.add_argument('--isKafka', dest='isKafka', required=False, help='isKafka')
    known_args, _ = parser.parse_known_args(sys.argv[1:])

    valenco_translate(known_args.input, known_args.output, known_args.isKafka)
