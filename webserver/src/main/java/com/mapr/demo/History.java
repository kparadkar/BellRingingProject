package com.mapr.demo;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.json.JSONArray;

@WebServlet("/history")
public class History extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Preprocess request: we actually don't need to do anything here, so just display JSP.

        request.getRequestDispatcher("/history.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Process all messages from stream

        // consume all msgs from stream notify topic
        Consumer consumer = new Consumer();
        JSONArray records = null;

        try {
            records = consumer.consumeAll();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            consumer.close();
        }

        request.setAttribute("records", records);
        request.getRequestDispatcher("/history.jsp").forward(request, response);
    }
}