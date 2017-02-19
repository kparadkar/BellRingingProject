<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Success!</title>
</head>
<body>
<h2>Information entered successfully</h2>
<img src="images/thumbs-up.png" alt="Bell" style="width:100px;height:100px;">
<br /><br />
<h3>Customer Name: ${name}</h3>
<h3>Deal Size: ${deal}</h3>
<br />
<button type="button" onclick="location = 'index.jsp'">Home</button><br />
<form action="history" method="post">
<input type="submit" name="history", value="Show history">
</body>
</html>
