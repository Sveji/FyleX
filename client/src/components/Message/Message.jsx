import '../../globalStyling/variables.less'
import '../../globalStyling/components.less'

const Message = ({ message, type = "out" }) => {
    return (
        <div className={`message-box ${type}`}>
            <p>{message}</p>
        </div>
    )
}

export default Message