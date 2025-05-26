from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Log, Header, Footer, Label
from textual_mqtt import MqttClient, MqttMessageSubscription, MqttConnectionSubscription

class MqttViewer(Container):
    def compose(self) -> ComposeResult:
        yield Log()
        yield MqttMessageSubscription("test")

    @on(MqttMessageSubscription.MqttMessageEvent)
    def mqtt_message_handler(self, evt: MqttMessageSubscription.MqttMessageEvent) -> None:
        self.query_one(Log).write_line(evt.topic + " " + evt.payload)

class MqttDemo(App):

    CSS='''
    #new_footer {
        height: 1;
        dock: bottom;
    }
    '''

    def compose(self) -> ComposeResult:
        yield Header()
        yield MqttClient()
        yield MqttViewer()
        with Horizontal(id="new_footer"):
            with Horizontal(id="new_inner"):
                yield Footer()
            yield Label("🔴 MQTT Disconnected", id="mqtt_status")
        yield MqttConnectionSubscription()

    @on(MqttConnectionSubscription.MqttConnected)
    def on_mqtt_connect(self, evt: MqttConnectionSubscription.MqttConnected):
        self.query_one("#mqtt_status", Label).update("🟢 MQTT Connected")

    @on(MqttConnectionSubscription.MqttDisconnected)
    def on_mqtt_disconnect(self, evt: MqttConnectionSubscription.MqttDisconnected):
        self.query_one("#mqtt_status", Label).update("🔴 MQTT Disconnected")

if __name__ == "__main__":
    MqttDemo().run()