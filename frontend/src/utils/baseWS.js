import API_DOMAIN from '../constants/api'


class BaseWebsocket {    

    constructor(token, endpoint) {
        this.websocket = null
        this.WEBSOCKET_PATH = `ws://${API_DOMAIN}${endpoint}?token=${token}`
    }

    connect() {
        try {
            this.websocket = new WebSocket(this.WEBSOCKET_PATH)
        } catch (error) {
            console.log("PUK")
        }


        this.websocket.onmessage = (event) => this.handleJSON(event, {})

        this.websocket.onclose = () => {

        }
        this.websocket.onerror = (error) => {
            this.websocket?.close()
            console.log(error)
        }
    }

    handleJSON(event, data) {
        if (data.type == "ping") {
            this.websocket?.send(JSON.stringify({ type: 'pong' }))
        }
    }

    disconnect() {
        this.websocket?.close()
    }

}


export default BaseWebsocket
