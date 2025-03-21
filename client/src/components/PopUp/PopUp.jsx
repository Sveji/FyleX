import { useState } from "react"
import ReactModal from "react-modal"
import { IoClose } from "react-icons/io5";

const PopUp = ({ children, classes }) => {
    const [shown, setShown] = useState(true)

    return (
        <ReactModal
            isOpen={shown}
            onRequestClose={() => setShown(false)}
            overlayClassName="screen-overlay"
            closeTimeoutMS={300}
            className={{
                base: `pop-up-container ${classes}`,
                beforeClose: "pop-up-closed"
            }}
        >
            {children}

            <IoClose onClick={() => setShown(false)} className="pop-up-icon" />
        </ReactModal>
    )
}

export default PopUp