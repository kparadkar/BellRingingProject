package com.mapr.demo;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.json.JSONException;

import java.util.Properties;

public class Producer {

    private KafkaProducer<String, String> localProducer = null;
    private static String topic = "/bell-project:notify";

    public Producer() {
        Properties props = new Properties();
        props.put("key.serializer",
                "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer",
                "org.apache.kafka.common.serialization.StringSerializer");
        localProducer = new KafkaProducer<String, String>(props);
    }

    public void produce(String key, String value) throws JSONException {
        localProducer.send(new ProducerRecord<String, String>(
                topic, key, value));
        localProducer.flush();
    }

    public void close() {
        localProducer.close();
    }
}
