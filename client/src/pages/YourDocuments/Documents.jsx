import { LuFileText } from "react-icons/lu";
import { IoCloseOutline } from "react-icons/io5";

import './yourdocuments.less'
import { useContext } from "react";
import { DataContext } from "../../context/DataContext";


const Documents = ({ document, deleteFunc }) => {
    // Gets global data from the context
    const { navigate, crud } = useContext(DataContext)


    return (
        <>
            <div className="file-container">
                <div className="file" onClick={() => navigate(`/document/${document.id}`)}>
                    <LuFileText className="icon" size={32} color={"#000000"} fill={"#7E4F83"} />
                    <p className="title">{document.name}</p>
                </div>
                <IoCloseOutline onClick={deleteFunc} className="close-icon" />

            </div>
        </>
    )
}

export default Documents