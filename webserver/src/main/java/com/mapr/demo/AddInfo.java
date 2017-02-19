package com.mapr.demo;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.mapr.demo.Producer;

@WebServlet("/addInfo")
public class AddInfo extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Preprocess request: we actually don't need to do anything here, so just display JSP.
        request.getRequestDispatcher("/index.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Postprocess request: gather and validate submitted data and display the result in the same JSP.

        // Prepare messages.
        Map<String, String> messages = new HashMap<String, String>();
        request.setAttribute("messages", messages);

        // Get and validate name.
        String name = request.getParameter("name");
        if (name == null || name.trim().isEmpty()) {
            messages.put("name", "Please enter name");
        } else if (!name.matches("\\p{Alnum}+")) {
            messages.put("name", "Please enter alphanumeric characters only");
        }

        // Get and validate Deal info.
        String deal = request.getParameter("deal");
        if (deal == null || deal.trim().isEmpty()) {
            messages.put("deal", "Please enter deal info");
        } else if (!deal.matches("\\p{Alnum}+")) {
            messages.put("deal", "Please enter numeric/alphanumeric characters only");
        }

        // Put info to stream
        if (messages.isEmpty()) {
            messages.put("success", String.format("Information entered successfully!"));

            addInfoToStream(name, deal);

            request.setAttribute("name", name);
            request.setAttribute("deal", deal);
            request.getRequestDispatcher("/success.jsp").forward(request, response);
        } else {
            request.getRequestDispatcher("/index.jsp").forward(request, response);
        }
    }

    private void addInfoToStream(String name, String dealSize) {
        Producer producer = new Producer();
        try {
            producer.produce(name, dealSize);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (producer != null)
                producer.close();
        }
    }
}