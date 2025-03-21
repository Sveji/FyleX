import { useState } from "react"
import ReactModal from "react-modal"
import { IoClose } from "react-icons/io5";

const PopUp = ({ children, classes, shown, onClose }) => {
    return (
        <ReactModal
            isOpen={shown}
            onRequestClose={onClose}
            overlayClassName="screen-overlay"
            closeTimeoutMS={300}
            className={{
                base: `pop-up-container ${classes}`,
                beforeClose: "pop-up-closed"
            }}
        >
            {children}

            <IoClose onClick={onClose} className="pop-up-icon" />
        </ReactModal>
    )
}

export default PopUp