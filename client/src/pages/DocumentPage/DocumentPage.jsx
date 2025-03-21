import { useContext, useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { DataContext } from "../../context/DataContext"
import AnalysisBox from "../../components/AnalysisBox/AnalysisBox"
import AssistantBox from "../../components/AssistantBox/AssistantBox"
import './documentPage.less'

const DocumentPage = () => {
    // Gets global data from the context
    const { crud } = useContext(DataContext)



    // Gets id from the url
    const { id } = useParams()



    // Stores the analysis
    const [analysis, setAnalysis] = useState([])



    // Gets the document from the backend
    useEffect(() => {
        const handleGetDocument = async () => {
            const response = await crud({
                url: `/api/document/?id=${id}`,
                method: 'get'
            })

            console.log(response)

            if(response.status == 200) {
                setAnalysis(response.data.analysis)
            }
        }

        if(id) handleGetDocument()
    }, [id])



    return (
        <div className="result-container">
            <AnalysisBox
                sentences={analysis}
            />
            <AssistantBox />
        </div>
    )
}

export default DocumentPage