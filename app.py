from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Integration Success</title>
        <style>
            body {
                background-color: #121212;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
            }
            .glow {
                font-size: 3rem;
                color: #0066ff;
                text-align: center;
                text-shadow: 0 0 10px #0066ff, 0 0 20px #0066ff, 0 0 30px #0066ff;
                animation: glow-animation 1.5s ease-in-out infinite alternate;
            }
            @keyframes glow-animation {
                from {
                    text-shadow: 0 0 5px #0066ff, 0 0 10px #0066ff;
                }
                to {
                    text-shadow: 0 0 10px #0066ff, 0 0 20px #0066ff, 0 0 30px #0066ff;
                }
            }
        </style>
    </head>
    <body>
        <div class="glow">
            Successfully Integrated:<br>
            Jenkins | Ansible | Docker<br>
            Web App Deployed
            LinkedIn: Harshwardhan jadhav!
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
