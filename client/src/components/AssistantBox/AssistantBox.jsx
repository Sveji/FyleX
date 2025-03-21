import Message from "./components/Message/Message"
import './assistant.less'
import { useContext, useEffect, useRef, useState } from "react"
import { TbSend } from "react-icons/tb";
import { DataContext } from "../../context/DataContext";
import { useParams } from "react-router-dom";

const AssistantBox = () => {
    // Gets global data from the context
    const { access } = useContext(DataContext)



    // Gets parameters from the url
    const { id } = useParams()



    // Placeholder before connecting the backend
    // const messages = [
    //     {
    //         message: "Can you please explain clause 4 to me?",
    //         type: "out"
    //     },
    //     {
    //         message: "I don't really understand what's going on with that clause.",
    //         type: "out"
    //     },
    //     {
    //         message: "Lorem ipsum dolor sit amet consectetur. Lorem habitasse ullamcorper ac nullam mi dictum nulla. Risus ut at eu at integer sit. Magna aliquet pharetra arcu aliquet integer. Etiam adipiscing vulputate ut eros. Egestas orci pretium augue donec turpis mi tortor venenatis. Rutrum vel diam cursus ultricies id. In turpis nec nec lacinia fringilla nibh.",
    //         type: "in"
    //     },
    //     {
    //         message: "Lorem ipsum dolor sit amet consectetur. Lorem habitasse ullamcorper ac.",
    //         type: "in"
    //     },
    //     {
    //         message: "I hope I was helpful ;)",
    //         type: "in"
    //     },
    //     {
    //         message: "Can you please explain clause 4 to me?",
    //         type: "out"
    //     },
    //     {
    //         message: "I don't really understand what's going on with that clause.",
    //         type: "out"
    //     },
    //     {
    //         message: "Lorem ipsum dolor sit amet consectetur. Lorem habitasse ullamcorper ac nullam mi dictum nulla. Risus ut at eu at integer sit. Magna aliquet pharetra arcu aliquet integer. Etiam adipiscing vulputate ut eros. Egestas orci pretium augue donec turpis mi tortor venenatis. Rutrum vel diam cursus ultricies id. In turpis nec nec lacinia fringilla nibh.",
    //         type: "in"
    //     },
    //     {
    //         message: "Lorem ipsum dolor sit amet consectetur. Lorem habitasse ullamcorper ac.",
    //         type: "in"
    //     },
    //     {
    //         message: "I hope I was helpful ;)",
    //         type: "in"
    //     },
    //     {
    //         message: "Can you please explain clause 4 to me?",
    //         type: "out"
    //     },
    //     {
    //         message: "I don't really understand what's going on with that clause.",
    //         type: "out"
    //     },
    //     {
    //         message: "Lorem ipsum dolor sit amet consectetur. Lorem habitasse ullamcorper ac nullam mi dictum nulla. Risus ut at eu at integer sit. Magna aliquet pharetra arcu aliquet integer. Etiam adipiscing vulputate ut eros. Egestas orci pretium augue donec turpis mi tortor venenatis. Rutrum vel diam cursus ultricies id. In turpis nec nec lacinia fringilla nibh.",
    //         type: "in"
    //     },
    //     {
    //         message: "Lorem ipsum dolor sit amet consectetur. Lorem habitasse ullamcorper ac.",
    //         type: "in"
    //     },
    //     {
    //         message: "I hope I was helpful ;)",
    //         type: "in"
    //     }
    // ]

    const [messages, setMessages] = useState([])


    const socketRef = useRef(null)

    // Creates a web socket connection
    useEffect(() => {
        if(access && id) {
            socketRef.current = new WebSocket(`ws://localhost:8000/ws/chatapp/?token=${access}&document_id=${id}`)

            socketRef.current.onopen = () => {
                console.log('connected to web socket')
            }

            socketRef.current.onclose = () => {
                console.log('closed web socket')
            }

            socketRef.current.onmessage = (e) => {
                const data = JSON.parse(e.data)

                if(data && data.action === "succses") {
                    console.log(data)
                    
                }
            }

            return () => {
                socketRef.current.close()
            }
        }
    }, [access])



    // Holds the state for the current message
    const [currMessage, setCurrMessage] = useState("")



    // Sends a message to the chat bot
    const handleSendMessage = () => {
        socketRef.current.send(JSON.stringify({
            action: "send_message",
            question: currMessage
        }))
    }



    return (
        <div className="assistant-box">
            <div className="title-box">
                <h1>AI Assistant</h1>
            </div>

            <div className="chat-container">
                {
                    messages && messages.length > 0 &&
                    <div className="messages-container">
                        <div className="no-more">
                            <div className="line"></div>
                            <p>No more messages</p>
                            <div className="line"></div>
                        </div>
                        {
                            messages.map((message, i) => (
                                <Message
                                    key={i}
                                    message={message.message}
                                    type={message.type}
                                />
                            ))
                        }
                    </div>
                }

                <div className="input-container">
                    <input
                        type="text"
                        placeholder="Consult with our AI model..."
                        value={currMessage}
                        onChange={(e) => setCurrMessage(e.target.value)}
                    />

                    <button onClick={handleSendMessage} className="send-btn">
                        <TbSend className="icon" />
                    </button>
                </div>
            </div>
        </div>
    )
}

export default AssistantBox