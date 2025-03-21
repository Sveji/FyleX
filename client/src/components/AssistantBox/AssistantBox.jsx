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
                    let newArr = [{message: data.question, type: "out"}]
                    if(data.response_data.answer) newArr = [...newArr, {message: data.response_data.answer.answer, type: "in"}]
                    setMessages(prev => [...prev, ...newArr])
                    setCurrMessage("")
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



    // Stores the chat box
    const chatRef = useRef()



    // Maintains the scroll position when we load more messages
    const prevHeightRef = useRef(0)
    useEffect(() => {
        if(messages.length) {
            chatRef.current.scrollTop += chatRef.current.scrollHeight - prevHeightRef.current
            prevHeightRef.current = chatRef.current.scrollHeight
        }
    }, [messages.length])



    return (
        <div className="assistant-box">
            <div className="title-box">
                <h1>Questions & Answers</h1>
            </div>

            <div className="chat-container">
                <div className="messages-container" ref={chatRef}>
                    <div className="no-more">
                        <div className="line"></div>
                        <p>No more messages</p>
                        <div className="line"></div>
                    </div>
                    {
                        messages && messages.length > 0 &&
                        messages.map((message, i) => (
                            <Message
                                key={i}
                                message={message.message}
                                type={message.type}
                            />
                        ))
                    }
                </div>

                <div className="input-container">
                    <input
                        type="text"
                        placeholder="Ask questions based on the document..."
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