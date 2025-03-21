import { LuFileText } from "react-icons/lu";

import './yourdocuments.less'
import { useContext } from "react";
import { DataContext } from "../../context/DataContext";


const Documents = ({ document }) => {
    // Gets global data from the context
    const { navigate } = useContext(DataContext)

    console.log(document)


    return (
        <>
            <div className="file-container" onClick={() => navigate(`/document/${document.id}`)}>
                <div className="file">
                    <LuFileText className="icon" size={32} color={"#000000"} fill={"#7E4F83"} />
                    <div className="file-title">
                        <p className="title">{document.name}</p>
                    </div>

                </div>

            </div>
        </>
    )
}

export default Documents