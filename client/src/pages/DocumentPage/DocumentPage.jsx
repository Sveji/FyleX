import { useContext, useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { DataContext } from "../../context/DataContext"
import AnalysisBox from "../../components/AnalysisBox/AnalysisBox"
import Highlight from "../Highlight/Highlight"
import AssistantBox from "../../components/AssistantBox/AssistantBox"
import './documentPage.less'
import Documents from '../YourDocuments/Documents'

const DocumentPage = () => {
    // Gets global data from the context
    const { crud, access } = useContext(DataContext)



    // Gets id from the url
    const { id } = useParams()



    // Stores the analysis
    const [analysis, setAnalysis] = useState([])

    //Stores the url
    const [pdfUrl, setPdfUrl] = useState(null)

    //Stores the highlites
    const [keywords, setKeywords] = useState(null)



    // Gets the document from the backend
    useEffect(() => {
        const handleGetDocument = async () => {
            const response = await crud({
                url: `/api/document/?id=${id}`,
                method: 'get',
                body: {
                    user: access
                }
            })

            console.log(response)

            if (response.status == 200) {
                const analysis = response.data.analysis.map((text) => {
                    return text.trim()
                })
                setAnalysis(response.data.analysis)
                setPdfUrl(response.data.document)
                setKeywords(analysis)
                console.log(analysis)
                console.log(response.data.document)
            }
        }

        if (id) handleGetDocument()
    }, [id])



    // Gets the summarization
    const handleSummarize = async () => {
        const response = await crud({
            url: `/api/document/summary/?document_id=${id}/`,
            method: 'get'
        })

        console.log(response)
    }



    return (
        <div className="result-container">
            <div className="document-box">
                <div className="btn-container">
                    <Documents />
                    <button onClick={() => handleSummarize()} className="btn">Summarize</button>
                </div>

                {pdfUrl && <Highlight pdfUrl={pdfUrl} keywords={keywords} />}
            </div>

            <div className="boxes">
                <AnalysisBox
                    sentences={analysis}
                />
                <AssistantBox />
            </div>




        </div>
    )
}

export default DocumentPage 