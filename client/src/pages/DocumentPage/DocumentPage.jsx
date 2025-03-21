import { useContext, useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { DataContext } from "../../context/DataContext"
import AnalysisBox from "../../components/AnalysisBox/AnalysisBox"
import Highlight from "../Highlight/Highlight"
import { div } from "three/tsl"
import AssistantBox from "../../components/AssistantBox/AssistantBox"
import './documentPage.less'

const DocumentPage = () => {
    // Gets global data from the context
    const { crud } = useContext(DataContext)



    // Gets id from the url
    const { id } = useParams()



    // Stores the analysis
    const [analysis, setAnalysis] = useState([])

    //Stores the url
    const [pdfUrl, setPdfUrl] = useState(null)



    // Gets the document from the backend
    useEffect(() => {
        const handleGetDocument = async () => {
            const response = await crud({
                url: `/api/document/?id=${id}`,
                method: 'get'
            })

            console.log(response)

            if (response.status == 200) {
                setAnalysis(response.data.analysis)
                setPdfUrl(response.data.document)
                console.log(response.data.document)
            }
        }

        if (id) handleGetDocument()
    }, [id])



    return (
        <div className="result-container">
            <AnalysisBox
                sentences={analysis}
            />
        </div>
    )
}

export default DocumentPage 