package com.mapr.demo;

import java.util.Properties;
import java.util.Arrays;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class Consumer {

    private KafkaConsumer<String, String> localConsumer = null;

    public Consumer() {

        String topic = "/bell-project:notify";

        Properties props = new Properties();
        props.put("auto.offset.reset", "earliest");
        props.put("group.id", "demo");
        props.put("key.deserializer",
                "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer",
                "org.apache.kafka.common.serialization.StringDeserializer");
        localConsumer = new KafkaConsumer<String, String>(props);

        if (localConsumer == null)
            throw new InternalError("Consumer initialization failed!");

        localConsumer.subscribe(Arrays.asList(topic));
    }

    public JSONArray consumeAll() throws JSONException {

        JSONArray jsonArr = new JSONArray();

        System.out.println("Consuming all the messages: ...");

        ConsumerRecords<String, String> records = localConsumer.poll(1000);
        for (ConsumerRecord<String, String> record : records) {

            if (record.key().isEmpty() || record.key().isEmpty())
                continue;

            JSONObject json = new JSONObject();
            json.put("name", record.key());
            json.put("size", record.value());

            //System.out.println("Name: " + record.key() + " , Deal size: " + record.value());

            jsonArr.put(json);
        }
        return jsonArr;
    }

    public void close() {
        localConsumer.close();
    }
}
