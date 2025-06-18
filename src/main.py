from textual.app import App
from gui.login import LoginPage
from textual.widgets import Footer
from textual.binding import Binding


class ArcanumApp(App):

    CSS_PATH = "assets/main.tcss"

    # Key binds for actions
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
    ]

    def compose(self):
        yield Footer()

    # When the application is created show the login page
    def on_mount(self) -> None:
        # Setup variable
        self.logged_in_user_id = 0

    def on_ready(self) -> None:
        # Show the login page first
        self.push_screen(LoginPage())


if __name__ == "__main__":
    app = ArcanumApp()
    app.run()
