import argparse
import logging
import os
import sys

from tasks.valenco_translator_task import ValencoTranslatorTask

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input', required=False, help='Input file to process.')
    parser.add_argument('--output', dest='output', required=False, help='Output file to write results to.')
    parser.add_argument('--source_topic', dest='source_topic', required=False, help='source_topic')
    parser.add_argument('--sink_topic', dest='sink_topic', required=False, help='sink_topic')
    parser.add_argument('--kafka_brokers', dest='kafka_brokers', required=False, help='kafka_brokers')

    known_args, _ = parser.parse_known_args(sys.argv[1:])

    kafka_source_config = None
    if known_args.kafka_brokers and known_args.source_topic:
        kafka_source_config = {'bootstrap_servers': known_args.kafka_brokers, 'topic': known_args.source_topic}

    kafka_sink_config = None
    if known_args.kafka_brokers and known_args.sink_topic:
        kafka_sink_config = {'bootstrap_servers': known_args.kafka_brokers, 'topic': known_args.sink_topic}

    kafka_translator_task = ValencoTranslatorTask(
        jars_to_add=[f"file:///{os.path.dirname(os.path.realpath(__file__))}/connectors/flink-sql-connector-kafka-1.16.0.jar"],
        input_file=known_args.input,
        output_file=known_args.output,
        kafka_source_config=kafka_source_config,
        kafka_sink_config=kafka_sink_config
    )
    kafka_translator_task.translate()
