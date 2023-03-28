def layout(content: str) -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        table {
            border: 2px solid black;
            border-spacing: 0;
            border-collapse: collapse;
        }
        td {
            border: 1px solid #888888;
        }
    </style>
</head>
<body>
    """ + content + """
</body>
</html> 
"""
