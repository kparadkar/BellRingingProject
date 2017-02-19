<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html lang="en">
<head>
    <title>Bell Project</title>
    <style>.error { color: red; } .success { color: green; }</style>
</head>
<body>
<h1> Welcome to Bell Project </h1>
<center><img src="images/bell.png" alt="Bell" style="width:250px;height:150px;"></center>
<br />

<form action="addInfo" method="post">
    <h1>Enter Customer Deal info:</h1>
    <p>
        <label for="name">Customer name: </label>
        <input id="name" name="name" value="${param.name}">
        <span class="error">${messages.name}</span>
    </p>
    <p>
        <label for="deal">Deal size: </label>
        <input id="deal" name="deal" value="${param.deal}">
        <span class="error">${messages.deal}</span>
    </p>
    <p>
        <input type="submit">
        <span class="success">${messages.success}</span>
    </p>
</form>

<br /><br />
<form action="history" method="post">
<input type="submit" name="history", value="Show history">
</form>

</body>
</html>
