from microapi.app import App
from handlers import echo_handler, user_agent_handler, get_file_handler, post_file_handler, empty_handler

if __name__ == "__main__":
    app = App(host="localhost", port=4221)
    app.add_route("GET", r"/echo/.*", echo_handler)
    app.add_route("GET", r"/", empty_handler)
    app.add_route("GET", r"/user-agent", user_agent_handler)
    app.add_route("GET", r"/files/.*", get_file_handler)
    app.add_route("POST", r"/files/.*", post_file_handler)
    app.start()