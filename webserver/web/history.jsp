<%@ page import="org.json.JSONArray"%>
<%@ page import="org.json.JSONObject" %>

<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>history</title>
</head>
<body>
<h2 id="top"> Overall history </h2>
<div align="center">
    <table border="1" cellpadding="5">
        <tr>
            <th>Customer Name</th>
            <th>Deal Size</th>
        </tr>
        <%
            JSONArray records = (JSONArray) request.getAttribute("records");
            for (int i=0; i < records.length(); i++) {
                JSONObject json = (JSONObject) records.get(i);
                String key = (String) json.get("name");
                String value = (String) json.get("size");
        %>
            <tr>
                <td><%=key%></td>
                <td><%=value%></td>
            </tr>
            <% }
        %>
    </table>
</div>
<a href="#top">Go to top</a><br />
<div><button type="button" onclick="location = 'index.jsp'" >Go to home</button></div>
</body>
</html>
