import { LuFileText } from "react-icons/lu";

import './yourdocuments.less'


const Documents = () => {


    return (
        <>
            <div className="file-container">
                <div className="file">
                    <LuFileText size={32} color={"#000000"} fill={"#7E4F83"} />
                    <div className="file-title">
                        <p>MikiEPrasence.pdf</p>
                        <div classname="p1" >32 TB</div>
                    </div>

                </div>

            </div>
        </>
    )
}

export default Documents